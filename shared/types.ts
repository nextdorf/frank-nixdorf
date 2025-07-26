export interface TextPromptRequest {
  prompt: string;
  userId?: string;
}

export interface TextPromptResponse {
  response: string;
  error?: string;
}

export interface PluginGenerationRequest {
  description: string;
  userId?: string;
}

export interface PluginGenerationResponse {
  pluginId: string;
  code: string;
  metadata: PluginMetadata;
  error?: string;
}

export interface PluginMetadata {
  name: string;
  description: string;
  version: string;
  type: 'component' | 'utility' | 'widget';
  dependencies?: string[];
}

export interface Plugin {
  id: string;
  metadata: PluginMetadata;
  code: string;
  isActive: boolean;
}

export interface APIResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
}