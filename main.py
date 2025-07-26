from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uuid
import logging

from services.gemini_service import GeminiService
from services.plugin_service import PluginService
from models.requests import TextPromptRequest, PluginGenerationRequest
from models.responses import APIResponse, TextPromptResponse, PluginGenerationResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title='The Anything App Backend', version='1.0.0')

app.add_middleware(
  CORSMiddleware,
  allow_origins=['http://localhost:5173', 'http://localhost:3000'],
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)

gemini_service = GeminiService()
plugin_service = PluginService()

@app.get('/health')
async def health_check():
  return {'status': 'healthy'}

@app.post('/api/prompt/text')
async def handle_text_prompt(request: TextPromptRequest) -> APIResponse[TextPromptResponse]:
  try:
    logger.info(f'Received text prompt: {request.prompt}')
    response = await gemini_service.process_text_prompt(request.prompt, request.userId)
    return APIResponse(success=True, data=TextPromptResponse(response=response))
  except Exception as e:
    logger.error(f'Error processing text prompt: {str(e)}')
    return APIResponse(success=False, error=str(e))

@app.post('/api/plugin/generate')
async def generate_plugin(request: PluginGenerationRequest) -> APIResponse[PluginGenerationResponse]:
  try:
    logger.info(f'Generating plugin for: {request.description}')
    plugin_response = await plugin_service.generate_plugin(request.description, request.userId)
    return APIResponse(success=True, data=plugin_response)
  except Exception as e:
    logger.error(f'Error generating plugin: {str(e)}')
    return APIResponse(success=False, error=str(e))

@app.get('/api/plugin/list')
async def list_plugins() -> APIResponse[List[PluginGenerationResponse]]:
  try:
    plugins = plugin_service.list_all_plugins()
    return APIResponse(success=True, data=plugins)
  except Exception as e:
    logger.error(f'Error listing plugins: {str(e)}')
    return APIResponse(success=False, error=str(e))

@app.get('/api/plugin/serve/{plugin_id}')
async def serve_plugin(plugin_id: str):
  try:
    plugin_code = plugin_service.get_plugin_code(plugin_id)
    if not plugin_code:
      raise HTTPException(status_code=404, detail='Plugin not found')
    return {'code': plugin_code}
  except HTTPException:
    raise  # Re-raise HTTPExceptions (like 404) without catching them
  except Exception as e:
    logger.error(f'Error serving plugin {plugin_id}: {str(e)}')
    raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
  import uvicorn
  uvicorn.run(app, host='0.0.0.0', port=8000)