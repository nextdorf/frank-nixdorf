from pydantic import BaseModel
from typing import Optional

class TextPromptRequest(BaseModel):
  prompt: str
  userId: Optional[str] = None

class PluginGenerationRequest(BaseModel):
  description: str
  userId: Optional[str] = None