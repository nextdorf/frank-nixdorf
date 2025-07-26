import logging
import sys
from datetime import datetime
from typing import Any, Dict


class AgentLibraryFormatter(logging.Formatter):
    """Custom formatter for agent library logs with structured output."""
    
    def format(self, record: logging.LogRecord) -> str:
        # Create timestamp
        timestamp = datetime.fromtimestamp(record.created).isoformat()
        
        # Build log entry
        log_entry = {
            'timestamp': timestamp,
            'level': record.levelname,
            'module': record.name,
            'message': record.getMessage(),
        }
        
        # Add extra fields if present
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'duration_ms'):
            log_entry['duration_ms'] = record.duration_ms
        if hasattr(record, 'request_type'):
            log_entry['request_type'] = record.request_type
        if hasattr(record, 'error_code'):
            log_entry['error_code'] = record.error_code
            
        # Format as readable string for container logs
        formatted = f"[{timestamp}] {record.levelname} {record.name}: {record.getMessage()}"
        
        # Add extra context if available
        extras = []
        if hasattr(record, 'request_id'):
            extras.append(f"req_id={record.request_id}")
        if hasattr(record, 'user_id'):
            extras.append(f"user_id={record.user_id}")
        if hasattr(record, 'duration_ms'):
            extras.append(f"duration={record.duration_ms}ms")
        if hasattr(record, 'request_type'):
            extras.append(f"type={record.request_type}")
            
        if extras:
            formatted += f" [{', '.join(extras)}]"
            
        return formatted


def setup_logging(level: str = "INFO") -> logging.Logger:
    """Set up structured logging for the agent library."""
    
    # Create root logger
    logger = logging.getLogger('agent_library')
    logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    
    # Set formatter
    formatter = AgentLibraryFormatter()
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    # Prevent duplicate logs
    logger.propagate = False
    
    logger.info("Agent library logging initialized", extra={'level': level})
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger for a specific module."""
    return logging.getLogger(f'agent_library.{name}')