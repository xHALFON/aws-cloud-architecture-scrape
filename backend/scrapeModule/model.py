from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class SourceType(str, Enum):
    HTML = "html"
    TEXT = "text"
    SVG = "svg"
    YAML = "yaml"
    JSON = "json"
    HCL = "hcl"
    IMAGE = "image"

class Resource(BaseModel):
    type: str 
    name: str
    properties: Dict[str, Any] = Field(default_factory=dict)
    connections: List[str] = Field(default_factory=list)

class Architecture(BaseModel):
    source_url: str
    source_type: SourceType
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    title: Optional[str] = None
    description: Optional[str] = None
    resources: List[Resource] = Field(default_factory=list)
    raw_content: str
    parsed_content: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_mongo(self) -> Dict[str, Any]:
        # Convert the model to a MongoDB-compatible dictionary
        return {
            "source_url": self.source_url,
            "source_type": self.source_type,
            "timestamp": self.timestamp,
            "title": self.title,
            "description": self.description,
            "resources": [resource.dict() for resource in self.resources],
            "raw_content": self.raw_content,
            "parsed_content": self.parsed_content,
            "metadata": self.metadata
        }

    @classmethod
    def from_mongo(cls, data: Dict[str, Any]) -> "Architecture":
        #Create an Architecture instance from MongoDB data
        resources = [Resource(**resource) for resource in data.get("resources", [])]
        return cls(
            source_url=data["source_url"],
            source_type=data["source_type"],
            timestamp=data["timestamp"],
            title=data.get("title"),
            description=data.get("description"),
            resources=resources,
            raw_content=data["raw_content"],
            parsed_content=data.get("parsed_content", {}),
            metadata=data.get("metadata", {})
        )
