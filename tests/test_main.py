import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from unittest.mock import AsyncMock

class TestHealthEndpoint:
    def test_health_check(self, client: TestClient):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

class TestTextPromptEndpoint:
    def test_successful_text_prompt(self, client: TestClient, mock_gemini_service):
        """Test successful text prompt processing."""
        payload = {
            "prompt": "Hello, world!",
            "userId": "test-user"
        }
        
        response = client.post("/api/prompt/text", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["response"] == "Mock AI response"
        
        mock_gemini_service.process_text_prompt.assert_called_once_with(
            "Hello, world!", "test-user"
        )

    def test_text_prompt_without_user_id(self, client: TestClient, mock_gemini_service):
        """Test text prompt without user ID."""
        payload = {"prompt": "Hello, world!"}
        
        response = client.post("/api/prompt/text", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        mock_gemini_service.process_text_prompt.assert_called_once_with(
            "Hello, world!", None
        )

    def test_text_prompt_service_error(self, client: TestClient, mock_gemini_service):
        """Test text prompt with service error."""
        mock_gemini_service.process_text_prompt.side_effect = Exception("Service error")
        
        payload = {"prompt": "Hello, world!"}
        response = client.post("/api/prompt/text", json=payload)
        
        assert response.status_code == 200  # FastAPI returns 200 with error in response
        data = response.json()
        assert data["success"] is False
        assert "Service error" in data["error"]

    def test_text_prompt_invalid_payload(self, client: TestClient):
        """Test text prompt with invalid payload."""
        response = client.post("/api/prompt/text", json={})
        
        assert response.status_code == 422  # Validation error

class TestPluginGenerationEndpoint:
    def test_successful_plugin_generation(self, client: TestClient, mock_plugin_service):
        """Test successful plugin generation."""
        payload = {
            "description": "Create a timer widget",
            "userId": "test-user"
        }
        
        response = client.post("/api/plugin/generate", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["pluginId"] == "test-plugin-123"
        assert data["data"]["metadata"]["name"] == "Test Plugin"
        
        mock_plugin_service.generate_plugin.assert_called_once_with(
            "Create a timer widget", "test-user"
        )

    def test_plugin_generation_without_user_id(self, client: TestClient, mock_plugin_service):
        """Test plugin generation without user ID."""
        payload = {"description": "Create a timer widget"}
        
        response = client.post("/api/plugin/generate", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        mock_plugin_service.generate_plugin.assert_called_once_with(
            "Create a timer widget", None
        )

    def test_plugin_generation_service_error(self, client: TestClient, mock_plugin_service):
        """Test plugin generation with service error."""
        mock_plugin_service.generate_plugin.side_effect = Exception("Plugin generation failed")
        
        payload = {"description": "Create a timer widget"}
        response = client.post("/api/plugin/generate", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "Plugin generation failed" in data["error"]

class TestPluginListEndpoint:
    def test_successful_plugin_list(self, client: TestClient, mock_plugin_service):
        """Test successful plugin listing."""
        mock_plugins = [
            {
                'pluginId': 'plugin1',
                'code': 'code1',
                'metadata': {'name': 'Plugin 1', 'description': 'Desc 1', 'version': '1.0.0', 'type': 'component', 'dependencies': None},
                'error': None
            }
        ]
        mock_plugin_service.list_all_plugins.return_value = mock_plugins
        
        response = client.get("/api/plugin/list")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"] == mock_plugins

    def test_plugin_list_service_error(self, client: TestClient, mock_plugin_service):
        """Test plugin listing with service error."""
        mock_plugin_service.list_all_plugins.side_effect = Exception("List error")
        
        response = client.get("/api/plugin/list")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "List error" in data["error"]

class TestPluginServeEndpoint:
    def test_successful_plugin_serve(self, client: TestClient, mock_plugin_service):
        """Test successful plugin serving."""
        mock_plugin_service.get_plugin_code.return_value = "test plugin code"
        
        response = client.get("/api/plugin/serve/test-plugin-123")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "test plugin code"
        
        mock_plugin_service.get_plugin_code.assert_called_once_with("test-plugin-123")

    def test_plugin_serve_not_found(self, client: TestClient, mock_plugin_service):
        """Test plugin serving when plugin not found."""
        mock_plugin_service.get_plugin_code.return_value = None
        
        response = client.get("/api/plugin/serve/nonexistent")
        
        assert response.status_code == 404
        assert "Plugin not found" in response.json()["detail"]

    def test_plugin_serve_service_error(self, client: TestClient, mock_plugin_service):
        """Test plugin serving with service error."""
        mock_plugin_service.get_plugin_code.side_effect = Exception("Serve error")
        
        response = client.get("/api/plugin/serve/test-plugin")
        
        assert response.status_code == 500
        assert "Serve error" in response.json()["detail"]