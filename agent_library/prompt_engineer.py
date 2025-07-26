from typing import Optional, Dict, Any
from .logger import get_logger


class PromptEngineer:
  def __init__(self):
    self.logger = get_logger('prompt_engineer')
    self.prompt_templates = {
      'text_passthrough': '{prompt}',
      'plugin_generation': 'Generate a {plugin_type} plugin that {description}',
      'code_enhancement': 'Improve this code: {code}',
      'documentation': 'Create documentation for: {content}'
    }
    self.logger.debug(f"PromptEngineer initialized with {len(self.prompt_templates)} templates")
  
  def process_text_prompt(self, prompt: str, user_id: Optional[str] = None) -> str:
    self.logger.debug(
      f"Processing text prompt - length: {len(prompt)}, user: {user_id or 'anonymous'}",
      extra={'prompt_length': len(prompt), 'user_id': user_id}
    )
    
    processed = self.prompt_templates['text_passthrough'].format(prompt=prompt)
    
    self.logger.debug("Text prompt processed using text_passthrough template")
    
    return processed
  
  def enhance_prompt_for_plugin_generation(
    self, 
    description: str, 
    plugin_type: str = 'component',
    context: Optional[Dict[str, Any]] = None
  ) -> str:
    self.logger.info(
      f"Enhancing prompt for plugin generation - type: {plugin_type}",
      extra={'plugin_type': plugin_type, 'description_length': len(description)}
    )
    
    enhanced_prompt = self.prompt_templates['plugin_generation'].format(
      plugin_type=plugin_type,
      description=description
    )
    
    if context:
      enhanced_prompt += f'\nContext: {context}'
      self.logger.debug(f"Added context to plugin generation prompt - keys: {list(context.keys())}")
    
    self.logger.debug(f"Plugin generation prompt created - length: {len(enhanced_prompt)}")
    
    return enhanced_prompt
  
  def craft_system_prompt(self, task_type: str) -> str:
    self.logger.debug(f"Crafting system prompt for task type: {task_type}")
    
    system_prompts = {
      'plugin_generation': 'You are a code generation assistant. Create clean, functional React components.',
      'text_processing': 'You are a helpful assistant that processes text requests.',
      'general': 'You are a helpful AI assistant.'
    }
    
    prompt = system_prompts.get(task_type, system_prompts['general'])
    
    if task_type not in system_prompts:
      self.logger.warning(f"Unknown task type '{task_type}', using general system prompt")
    
    self.logger.debug(f"System prompt crafted - length: {len(prompt)}")
    
    return prompt
  
  def add_safety_constraints(self, prompt: str) -> str:
    self.logger.debug("Adding safety constraints to prompt")
    
    safety_suffix = '\n\nEnsure the response is safe, appropriate, and follows best practices.'
    enhanced_prompt = prompt + safety_suffix
    
    self.logger.debug(f"Safety constraints added - new length: {len(enhanced_prompt)}")
    
    return enhanced_prompt
