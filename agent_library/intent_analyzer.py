from typing import Dict, Any
from pydantic import BaseModel
from .logger import get_logger


class IntentResult(BaseModel):
  intent_type: str
  confidence: float
  entities: Dict[str, Any]
  requires_plugin: bool


class IntentAnalyzer:
  def __init__(self):
    self.logger = get_logger('intent_analyzer')
    self.intent_patterns = {
      'create_timer': ['timer', 'countdown', 'stopwatch', 'time'],
      'create_calculator': ['calculator', 'calc', 'calculate', 'math'],
      'create_document': ['document', 'doc', 'note', 'write'],
      'general_query': ['what', 'how', 'why', 'when', 'where']
    }
    self.logger.debug(f"IntentAnalyzer initialized with {len(self.intent_patterns)} intent patterns")
  
  def analyze_intent(self, text: str) -> IntentResult:
    self.logger.debug(f"Analyzing intent for text: '{text[:50]}{'...' if len(text) > 50 else ''}'")
    
    text_lower = text.lower()
    
    for intent_type, keywords in self.intent_patterns.items():
      matched_keywords = [kw for kw in keywords if kw in text_lower]
      
      if matched_keywords:
        confidence = self._calculate_confidence(text_lower, keywords)
        entities = self._extract_entities(text, intent_type)
        requires_plugin = intent_type in ['create_timer', 'create_calculator']
        
        self.logger.info(
          f"Intent detected: {intent_type} (confidence: {confidence:.2f})",
          extra={
            'intent_type': intent_type,
            'confidence': confidence,
            'matched_keywords': matched_keywords,
            'requires_plugin': requires_plugin,
            'entities_count': len(entities)
          }
        )
        
        return IntentResult(
          intent_type=intent_type,
          confidence=confidence,
          entities=entities,
          requires_plugin=requires_plugin
        )
    
    self.logger.debug("No specific intent detected, defaulting to general_query")
    
    return IntentResult(
      intent_type='general_query',
      confidence=0.5,
      entities={},
      requires_plugin=False
    )
  
  def _calculate_confidence(self, text: str, keywords: list) -> float:
    matches = sum(1 for keyword in keywords if keyword in text)
    return min(0.9, matches / len(keywords) + 0.3)
  
  def _extract_entities(self, text: str, intent_type: str) -> Dict[str, Any]:
    self.logger.debug(f"Extracting entities for intent_type: {intent_type}")
    
    entities = {}
    
    if intent_type == 'create_timer':
      entities['type'] = 'timer'
      if 'countdown' in text.lower():
        entities['countdown'] = True
        self.logger.debug("Detected countdown timer entity")
    elif intent_type == 'create_calculator':
      entities['type'] = 'calculator'
      self.logger.debug("Detected calculator entity")
    
    self.logger.debug(f"Extracted {len(entities)} entities: {list(entities.keys())}")
    
    return entities
