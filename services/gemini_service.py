import asyncio
import subprocess
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class GeminiService:
  def __init__(self):
    self.gemini_command = 'gemini'
    
  async def process_text_prompt(self, prompt: str, user_id: Optional[str] = None) -> str:
    try:
      logger.info(f'Processing text prompt with Gemini CLI: {prompt[:50]}...')
      
      process = await asyncio.create_subprocess_exec(
        self.gemini_command, 'chat', prompt,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
      )
      
      stdout, stderr = await process.communicate()
      
      if process.returncode != 0:
        error_msg = stderr.decode('utf-8') if stderr else 'Unknown error'
        logger.error(f'Gemini CLI error: {error_msg}')
        
        if 'not found' in error_msg.lower() or 'command not found' in error_msg.lower():
          return 'Gemini CLI is not installed or not in PATH. For now, simulating response: I understand you want to work with "' + prompt + '". This would normally be processed by Gemini AI.'
        
        raise Exception(f'Gemini CLI error: {error_msg}')
      
      response = stdout.decode('utf-8').strip()
      logger.info(f'Received response from Gemini CLI: {response[:100]}...')
      return response
      
    except FileNotFoundError:
      logger.warning('Gemini CLI not found, returning simulated response')
      return f'Gemini CLI not available. Simulated response: I understand you want to work with "{prompt}". In a real setup, this would be processed by Gemini AI.'
    except Exception as e:
      logger.error(f'Error calling Gemini CLI: {str(e)}')
      return f'Error processing request: {str(e)}. Simulated response: I understand you want to work with "{prompt}".'