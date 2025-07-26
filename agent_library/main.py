from .intent_analyzer import IntentAnalyzer
from .prompt_engineer import PromptEngineer
from .media_handlers import AudioHandler, ImageHandler
from .logger import setup_logging, get_logger
from typing import Dict, Any
import time
import uuid
import os


class AgentLibrary:
  def __init__(self):
    # Initialize logging
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    setup_logging(log_level)
    self.logger = get_logger('main')
    
    self.logger.info("Initializing AgentLibrary components")
    
    try:
      self.logger.debug("Creating IntentAnalyzer")
      self.intent_analyzer = IntentAnalyzer()
      
      self.logger.debug("Creating PromptEngineer")
      self.prompt_engineer = PromptEngineer()
      
      self.logger.debug("Creating AudioHandler")
      self.audio_handler = AudioHandler()
      
      self.logger.debug("Creating ImageHandler")
      self.image_handler = ImageHandler()
      
      self.logger.info("AgentLibrary initialization completed successfully")
    except Exception as e:
      self.logger.error(f"Failed to initialize AgentLibrary: {str(e)}", exc_info=True)
      raise
  
  def process_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
    # Generate request ID for tracking
    request_id = str(uuid.uuid4())[:8]
    request_type = request_data.get('type', 'text')
    user_id = request_data.get('user_id', 'anonymous')
    
    start_time = time.time()
    
    self.logger.info(
      f"Processing request", 
      extra={
        'request_id': request_id,
        'request_type': request_type,
        'user_id': user_id
      }
    )
    
    try:
      if request_type == 'text':
        result = self._process_text_request(request_data, request_id)
      elif request_type == 'audio':
        result = self._process_audio_request(request_data, request_id)
      elif request_type == 'image':
        result = self._process_image_request(request_data, request_id)
      else:
        self.logger.warning(
          f"Unsupported request type: {request_type}",
          extra={'request_id': request_id, 'request_type': request_type}
        )
        return {'error': f'Unsupported request type: {request_type}', 'request_id': request_id}
      
      duration_ms = round((time.time() - start_time) * 1000, 2)
      
      self.logger.info(
        f"Request processed successfully",
        extra={
          'request_id': request_id,
          'request_type': request_type,
          'user_id': user_id,
          'duration_ms': duration_ms
        }
      )
      
      # Add request metadata to result
      result['request_id'] = request_id
      result['processing_time_ms'] = duration_ms
      
      return result
      
    except Exception as e:
      duration_ms = round((time.time() - start_time) * 1000, 2)
      
      self.logger.error(
        f"Request processing failed: {str(e)}",
        extra={
          'request_id': request_id,
          'request_type': request_type,
          'user_id': user_id,
          'duration_ms': duration_ms,
          'error_code': 'PROCESSING_ERROR'
        },
        exc_info=True
      )
      
      return {
        'error': f'Processing failed: {str(e)}',
        'request_id': request_id,
        'processing_time_ms': duration_ms
      }
  
  def _process_text_request(self, request_data: Dict[str, Any], request_id: str) -> Dict[str, Any]:
    text = request_data.get('text', '')
    user_id = request_data.get('user_id')
    
    self.logger.debug(
      f"Processing text request: '{text[:100]}{'...' if len(text) > 100 else ''}'",
      extra={'request_id': request_id, 'text_length': len(text)}
    )
    
    try:
      self.logger.debug("Analyzing intent", extra={'request_id': request_id})
      intent_result = self.intent_analyzer.analyze_intent(text)
      
      self.logger.debug("Processing prompt", extra={'request_id': request_id})
      processed_prompt = self.prompt_engineer.process_text_prompt(text, user_id)
      
      self.logger.debug(
        f"Text processing completed - intent: {intent_result.intent if hasattr(intent_result, 'intent') else 'unknown'}",
        extra={'request_id': request_id}
      )
      
      return {
        'processed_prompt': processed_prompt,
        'intent': intent_result.model_dump(),
        'type': 'text'
      }
    except Exception as e:
      self.logger.error(
        f"Text processing failed: {str(e)}",
        extra={'request_id': request_id, 'error_code': 'TEXT_PROCESSING_ERROR'},
        exc_info=True
      )
      raise
  
  def _process_audio_request(self, request_data: Dict[str, Any], request_id: str) -> Dict[str, Any]:
    audio_data = request_data.get('audio_data', b'')
    audio_format = request_data.get('format', 'wav')
    
    self.logger.debug(
      f"Processing audio request - format: {audio_format}, size: {len(audio_data)} bytes",
      extra={'request_id': request_id, 'audio_format': audio_format, 'audio_size_bytes': len(audio_data)}
    )
    
    try:
      result = self.audio_handler.process_audio(audio_data, audio_format)
      self.logger.debug("Audio processing completed", extra={'request_id': request_id})
      return {'audio_result': result, 'type': 'audio'}
    except Exception as e:
      self.logger.error(
        f"Audio processing failed: {str(e)}",
        extra={'request_id': request_id, 'error_code': 'AUDIO_PROCESSING_ERROR'},
        exc_info=True
      )
      raise
  
  def _process_image_request(self, request_data: Dict[str, Any], request_id: str) -> Dict[str, Any]:
    image_data = request_data.get('image_data', b'')
    image_format = request_data.get('format', 'png')
    
    self.logger.debug(
      f"Processing image request - format: {image_format}, size: {len(image_data)} bytes",
      extra={'request_id': request_id, 'image_format': image_format, 'image_size_bytes': len(image_data)}
    )
    
    try:
      result = self.image_handler.process_image(image_data, image_format)
      self.logger.debug("Image processing completed", extra={'request_id': request_id})
      return {'image_result': result, 'type': 'image'}
    except Exception as e:
      self.logger.error(
        f"Image processing failed: {str(e)}",
        extra={'request_id': request_id, 'error_code': 'IMAGE_PROCESSING_ERROR'},
        exc_info=True
      )
      raise


if __name__ == "__main__":
    # Initialize library for testing/debugging
    import json
    
    library = AgentLibrary()
    
    # Test with sample request
    test_request = {
        'type': 'text',
        'text': 'Hello, this is a test message',
        'user_id': 'test_user'
    }
    
    print("Testing AgentLibrary with sample request...")
    result = library.process_request(test_request)
    print(f"Result: {json.dumps(result, indent=2)}")
