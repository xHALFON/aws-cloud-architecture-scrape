from pathlib import Path
from platform import architecture
import re
import json
import yaml
import requests
from typing import Optional, Dict, Any, List, Union
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract
import io
from io import StringIO, BytesIO
from bson import ObjectId
from .model import Architecture, SourceType, Resource
from .geminiApi import gemini_vision_analyze, gemini_analyze_text

class ArchitectureScraper:
    def __init__(self, db):
        self.db = db
        self.collection = db["architectures"]

    async def scrape_and_store(self, url: str) -> Architecture:
        # Main method to scrape and store architecture data
        content, source_type = await self._fetch_content(url)
        architecture = await self._parse_content(url, content, source_type)

        self.collection.insert_one(architecture.to_mongo())
        return architecture

    async def _fetch_content(self, url: str) -> tuple[Union[str, bytes], SourceType]:
        # Fetch content from URL and determine its type
        response = requests.get(url)
        content_type = response.headers.get('content-type', '').lower()
        content = response.text.strip()
        
        if 'image' in content_type:
            if 'svg' in content_type:
                return response.text, SourceType.SVG
            return response.content, SourceType.IMAGE
        
        try:
            parsed_json = json.loads(content)
            if isinstance(parsed_json, dict):
                return content, SourceType.JSON
        except json.JSONDecodeError:
            pass

        if bool(BeautifulSoup(content, "html.parser").find()):
            return content, SourceType.HTML

        # Default
        return content, SourceType.TEXT

    async def _parse_content(self, url: str, content: Union[str, bytes], source_type: SourceType) -> Architecture:
        # Parse the content based on its type and extract architecture information
        parsed_content = {}
        resources = []
        title = None
        description = None
        print("parsing content", source_type)
        
        if source_type == SourceType.IMAGE:
            parsed_content, resources = await self._process_with_ai(content)
            try: # Save image temporarily to disk for OCR backup
                image_bytes = content if isinstance(content, bytes) else str(content).encode()
                image = Image.open(BytesIO(image_bytes))
                text_content = pytesseract.image_to_string(image)
                parsed_content["ocr_text"] = text_content
            except Exception as e:
                print(f"OCR failed: {e}")
                parsed_content["ocr_text"] = None

        elif source_type == SourceType.HTML:
            soup = BeautifulSoup(content, "html.parser")
            title = soup.title.string if soup.title else None
            text_content = soup.get_text() # extract text content
            parsed_content, resources = await self._process_with_ai(text_content)

        elif source_type == SourceType.JSON:
            data = json.loads(content)
            parsed_content = data
            resources = await self._extract_resources_from_structured_data(data)

        else:  # TEXT, SVG
            parsed_content, resources = await self._process_with_ai(content)

        return Architecture(
            source_url=url,
            source_type=source_type,
            title=title,
            description=description,
            resources=resources,
            raw_content="" if isinstance(content, bytes) else str(content),  # Empty string for binary content
            parsed_content=parsed_content
        )

    async def _process_with_ai(
        self, content: Union[str, bytes, Path]
    ) -> tuple[Dict[str, Any], List[Resource]]:
        """
        Process content using AI to extract architecture information.
        Content can be:
        - bytes: raw image data
        - Path: path to image file
        - str: text content
        """
        parsed_content = {}
        resources: List[Resource] = []

        if isinstance(content, (bytes, Path)):
            print("Processing image with Gemini Vision")
            # If it's bytes, we need to save it temporarily
            if isinstance(content, bytes):
                temp_path = Path("temp_image.png")
                with open(temp_path, "wb") as f:
                    f.write(content)
                content = temp_path
                
            try:
                response = await gemini_vision_analyze(content)
                parsed_content = {
                    "summary": response.get("summary", ""),
                    "detected_services": response.get("services", []),
                }
                for i, service in enumerate(parsed_content["detected_services"]):
                    service_type = service.lower().replace(" ", "_")
                    resources.append(Resource(
                        type=service_type,
                        name=f"{service_type}_{i+1}",
                        properties={"source": "gemini_vision"}
                    ))
            finally:
                if isinstance(content, Path) and content.name == "temp_image.png":
                    content.unlink(missing_ok=True)

        elif isinstance(content, str):
            print("Processing text with gemini / Regex")
            try:
                parsed = await gemini_analyze_text(content)
                parsed_content = {
                    "summary": parsed.get("summary", ""),
                    "detected_services": parsed.get("services", [])
                }
                for i, service in enumerate(parsed.get("services", [])):
                    service_type = service.lower().replace(" ", "_")
                    resources.append(Resource(
                        type=service_type,
                        name=f"{service_type}_{i+1}",
                        properties={"source": "gemini_text"}
                    ))
            except Exception as e:
                # fallback to regex if gemini fails
                print("gemini failed, using regex fallback", e)
                # Common AWS service patterns
                service_pattern = r"""
                    \b(aws|amazon)?\s*  # Optional AWS/Amazon prefix
                    (
                        [a-z0-9]+       # Service name start
                        (?:\s*[a-z0-9]+)*  # Additional words in service name
                    )
                    (?:\s+service)?     # Optional "service" suffix
                    \b
                """
                matches = re.finditer(service_pattern, content.lower(), re.VERBOSE)
                detected_services = []
                for i, match in enumerate(matches):
                    service_name = match.group(2).strip()
                    if service_name:
                        service_type = service_name.replace(" ", "_")
                        detected_services.append(service_type)
                        resources.append(Resource(
                            type=service_type,
                            name=f"{service_type}_{i+1}",
                            properties={"detected_text": match.group(0)}
                        ))
                parsed_content = {
                    "summary": "Extracted using regex patterns",
                    "detected_services": detected_services
                }

        return parsed_content, resources

    async def _extract_resources_from_structured_data(self, data: Dict[str, Any]) -> List[Resource]:
        # Extract resources from structured data (YAML/JSON)
        resources = []
        
        def extract_resources(d: Dict[str, Any], parent_key=""):
            for key, value in d.items():
                key_lower = key.lower()
                # Check if this dictionary represents an AWS resource
                if isinstance(value, dict):
                    # Look for AWS service indicators in the key
                    if any(indicator in key_lower for indicator in ["aws", "amazon"]):
                        service_type = key_lower.replace(" ", "_")
                        resources.append(Resource(
                            type=service_type,
                            name=f"{parent_key}_{key}" if parent_key else key,
                            properties=value
                        ))
                    extract_resources(value, key)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            extract_resources(item, key)

        extract_resources(data)
        return resources

    async def get_architectures(self, skip: int = 0, limit: int = 100) -> List[Architecture]:
        # Retrieve stored architectures with pagination, sorted by _id descending (newest first)
        architectures = self.collection.find().sort("_id", -1).skip(skip).limit(limit)
        return [Architecture.from_mongo(doc) for doc in architectures]
