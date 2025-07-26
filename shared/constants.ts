export const API_ENDPOINTS = {
  TEXT_PROMPT: '/api/prompt/text',
  PLUGIN_GENERATE: '/api/plugin/generate',
  PLUGIN_SERVE: '/api/plugin/serve',
  PLUGIN_LIST: '/api/plugin/list'
} as const;

export const PLUGIN_TYPES = {
  COMPONENT: 'component',
  UTILITY: 'utility',
  WIDGET: 'widget'
} as const;

// export const DEFAULT_BACKEND_URL = 'http://agentic-ai-hackathon-2025-backend-1:8000';
// export const DEFAULT_BACKEND_URL = 'http://backend:8000';
export const DEFAULT_BACKEND_URL = 'http://127.0.0.1:8000';
