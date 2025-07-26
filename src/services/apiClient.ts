import axios from 'axios';
import type { 
  TextPromptRequest, 
  TextPromptResponse, 
  PluginGenerationRequest, 
  PluginGenerationResponse,
  APIResponse 
} from '@shared/types';
import { API_ENDPOINTS, DEFAULT_BACKEND_URL } from '@shared/constants';

class APIClient {
  private baseURL: string;

  constructor(baseURL: string = DEFAULT_BACKEND_URL) {
    this.baseURL = baseURL;
  }

  async sendTextPrompt(request: TextPromptRequest): Promise<TextPromptResponse> {
    try {
      const response = await axios.post<APIResponse<TextPromptResponse>>(
        `${this.baseURL}${API_ENDPOINTS.TEXT_PROMPT}`,
        request
      );
      
      if (response.data.success && response.data.data) {
        return response.data.data;
      } else {
        throw new Error(response.data.error || 'Unknown error occurred');
      }
    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.code === 'ECONNREFUSED') {
          throw new Error('Backend server is not running. Please start the backend service.');
        }
        throw new Error(error.response?.data?.error || error.message);
      }
      throw error;
    }
  }

  async generatePlugin(request: PluginGenerationRequest): Promise<PluginGenerationResponse> {
    try {
      const response = await axios.post<APIResponse<PluginGenerationResponse>>(
        `${this.baseURL}${API_ENDPOINTS.PLUGIN_GENERATE}`,
        request
      );
      
      if (response.data.success && response.data.data) {
        return response.data.data;
      } else {
        throw new Error(response.data.error || 'Unknown error occurred');
      }
    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.code === 'ECONNREFUSED') {
          throw new Error('Backend server is not running. Please start the backend service.');
        }
        throw new Error(error.response?.data?.error || error.message);
      }
      throw error;
    }
  }

  async listPlugins(): Promise<PluginGenerationResponse[]> {
    try {
      const response = await axios.get<APIResponse<PluginGenerationResponse[]>>(
        `${this.baseURL}${API_ENDPOINTS.PLUGIN_LIST}`
      );
      
      if (response.data.success && response.data.data) {
        return response.data.data;
      } else {
        throw new Error(response.data.error || 'Unknown error occurred');
      }
    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.code === 'ECONNREFUSED') {
          throw new Error('Backend server is not running. Please start the backend service.');
        }
        throw new Error(error.response?.data?.error || error.message);
      }
      throw error;
    }
  }
}

export const apiClient = new APIClient();