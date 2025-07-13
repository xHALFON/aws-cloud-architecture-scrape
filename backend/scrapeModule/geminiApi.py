import os
from pathlib import Path
from typing import Dict, Any
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import re
import json

load_dotenv()


key = os.getenv("GEMINI_API_KEY")
if not key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables")
genai.configure(api_key=key)


vision_model = genai.GenerativeModel('gemini-1.5-flash')
text_model = genai.GenerativeModel('gemini-1.5-flash')

def clean_json_response(text: str) -> str:
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    return text.strip()

async def gemini_vision_analyze(image_path: Path) -> Dict[str, Any]:
    """
    Analyze an image using Gemini Vision API to detect AWS architecture components.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Dict containing:
        - summary: A textual description of the architecture
        - services: List of detected AWS services
    """
    try:
        image = Image.open(image_path)

        prompt = """
        Analyze this AWS architecture diagram. Please identify:
        1. All AWS services present in the image
        2. The overall architecture flow and relationships between services
        3. Any security or networking components
        
        Format your response as JSON with these keys:
        {
            "summary": "Brief description of the architecture",
            "services": ["Service1", "Service2", ...],
            "relationships": ["Service1 connects to Service2", ...],
            "security_components": ["Component1", ...]
        }
        
        Only include official AWS service names that match these options:
        - ec2
        - s3
        - rds
        - lambda
        - api_gateway
        - vpc
        - subnet
        - security_group
        - load_balancer
        
        Return ONLY the JSON, without any markdown formatting or additional text.
        """
        
        response = vision_model.generate_content([prompt, image])
        response_text = clean_json_response(response.text)
        
        try:
            result = json.loads(response_text)
        except json.JSONDecodeError:
            # Fallback: Extract services using regex if JSON parsing fails
            services = re.findall(r'(ec2|s3|rds|lambda|api_gateway|vpc|subnet|security_group|load_balancer)', response_text.lower())
            result = {
                "summary": response_text.split('\n')[0],
                "services": list(set(services))
            }
        
        return result
        
    except Exception as e:
        print(f"Error in Gemini Vision analysis: {str(e)}")
        return {"summary": "", "services": []}

async def gemini_analyze_text(content: str) -> Dict[str, Any]:
    """
    Analyze text content using Gemini to identify AWS architecture components.
    
    Args:
        content: Text content to analyze
        
    Returns:
        Dict containing:
        - summary: A processed description of the architecture
        - services: List of detected AWS services
    """
    try:
        prompt = f"""
        Analyze this text for AWS architecture components. The text is:
        
        {content}
        
        Extract all AWS services mentioned and provide a summary. 
        Format your response as JSON with these keys:
        {{
            "summary": "Brief description of the architecture",
            "services": ["Service1", "Service2", ...],
        }}
        
        Only include official AWS service names that match these options:
        - ec2
        - s3
        - rds
        - lambda
        - api_gateway
        - vpc
        - subnet
        - security_group
        - load_balancer
        
        Return ONLY the JSON, without any markdown formatting or additional text.
        """
        
   
        response = text_model.generate_content(prompt)
        response_text = clean_json_response(response.text)
        
        try:
            result = json.loads(response_text)
            print("Successfully parsed JSON response")
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {str(e)}")
            # Extract services using regex if JSON parsing fails
            services = re.findall(r'(ec2|s3|rds|lambda|api_gateway|vpc|subnet|security_group|load_balancer)', response_text.lower())
            result = {
                "summary": response_text.split('\n')[0],
                "services": list(set(services))
            }
            print("Using regex fallback result:", result)
        
        return result
        
    except Exception as e:
        print(f"Error in Gemini text analysis: {str(e)}")
        return {"summary": "", "services": []}