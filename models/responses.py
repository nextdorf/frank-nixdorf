from pydantic import BaseModel, field_validator
from typing import Optional, Generic, TypeVar, List

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
  success: bool
  data: Optional[T] = None
  error: Optional[str] = None

class TextPromptResponse(BaseModel):
  response: str
  error: Optional[str] = None

class PluginMetadata(BaseModel):
  name: str
  description: str
  version: str
  type: str
  dependencies: Optional[List[str]] = None
  
  @field_validator('type')
  @classmethod
  def validate_type(cls, v):
    valid_types = ['component', 'widget', 'utility']
    if v not in valid_types:
      raise ValueError(f'type must be one of {valid_types}')
    return v

class PluginGenerationResponse(BaseModel):
  pluginId: str
  code: str
  metadata: PluginMetadata
  error: Optional[str] = None