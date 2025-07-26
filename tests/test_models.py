import pytest
from pydantic import ValidationError
from models.requests import TextPromptRequest, PluginGenerationRequest
from models.responses import (
    APIResponse, 
    TextPromptResponse, 
    PluginGenerationResponse, 
    PluginMetadata
)

class TestTextPromptRequest:
    def test_valid_request_with_user_id(self):
        """Test valid text prompt request with user ID."""
        request = TextPromptRequest(prompt="Hello world", userId="user123")
        
        assert request.prompt == "Hello world"
        assert request.userId == "user123"

    def test_valid_request_without_user_id(self):
        """Test valid text prompt request without user ID."""
        request = TextPromptRequest(prompt="Hello world")
        
        assert request.prompt == "Hello world"
        assert request.userId is None

    def test_invalid_request_missing_prompt(self):
        """Test invalid request missing prompt."""
        with pytest.raises(ValidationError):
            TextPromptRequest()

    def test_empty_prompt_is_valid(self):
        """Test that empty prompt is valid."""
        request = TextPromptRequest(prompt="")
        
        assert request.prompt == ""

class TestPluginGenerationRequest:
    def test_valid_request_with_user_id(self):
        """Test valid plugin generation request with user ID."""
        request = PluginGenerationRequest(description="Create a timer", userId="user123")
        
        assert request.description == "Create a timer"
        assert request.userId == "user123"

    def test_valid_request_without_user_id(self):
        """Test valid plugin generation request without user ID."""
        request = PluginGenerationRequest(description="Create a timer")
        
        assert request.description == "Create a timer"
        assert request.userId is None

    def test_invalid_request_missing_description(self):
        """Test invalid request missing description."""
        with pytest.raises(ValidationError):
            PluginGenerationRequest()

class TestPluginMetadata:
    def test_valid_metadata(self):
        """Test valid plugin metadata."""
        metadata = PluginMetadata(
            name="Test Plugin",
            description="A test plugin",
            version="1.0.0",
            type="component"
        )
        
        assert metadata.name == "Test Plugin"
        assert metadata.description == "A test plugin"
        assert metadata.version == "1.0.0"
        assert metadata.type == "component"
        assert metadata.dependencies is None

    def test_metadata_with_dependencies(self):
        """Test plugin metadata with dependencies."""
        metadata = PluginMetadata(
            name="React Plugin",
            description="A React plugin",
            version="2.1.0",
            type="widget",
            dependencies=["react", "react-dom"]
        )
        
        assert metadata.dependencies == ["react", "react-dom"]

    def test_invalid_type(self):
        """Test invalid plugin type."""
        with pytest.raises(ValidationError):
            PluginMetadata(
                name="Invalid Plugin",
                description="Invalid type",
                version="1.0.0",
                type="invalid_type"
            )

    def test_valid_types(self):
        """Test all valid plugin types."""
        valid_types = ["component", "utility", "widget"]
        
        for plugin_type in valid_types:
            metadata = PluginMetadata(
                name="Test Plugin",
                description="Test",
                version="1.0.0",
                type=plugin_type
            )
            assert metadata.type == plugin_type

class TestTextPromptResponse:
    def test_valid_response(self):
        """Test valid text prompt response."""
        response = TextPromptResponse(response="AI generated response")
        
        assert response.response == "AI generated response"
        assert response.error is None

    def test_response_with_error(self):
        """Test text prompt response with error."""
        response = TextPromptResponse(response="", error="Something went wrong")
        
        assert response.response == ""
        assert response.error == "Something went wrong"

class TestPluginGenerationResponse:
    def test_valid_response(self):
        """Test valid plugin generation response."""
        metadata = PluginMetadata(
            name="Test Plugin",
            description="A test plugin",
            version="1.0.0",
            type="component"
        )
        
        response = PluginGenerationResponse(
            pluginId="plugin-123",
            code="function TestPlugin() { return <div>Test</div>; }",
            metadata=metadata
        )
        
        assert response.pluginId == "plugin-123"
        assert "TestPlugin" in response.code
        assert response.metadata.name == "Test Plugin"
        assert response.error is None

    def test_response_with_error(self):
        """Test plugin generation response with error."""
        metadata = PluginMetadata(
            name="Failed Plugin",
            description="Failed to generate",
            version="1.0.0",
            type="component"
        )
        
        response = PluginGenerationResponse(
            pluginId="failed-plugin",
            code="",
            metadata=metadata,
            error="Generation failed"
        )
        
        assert response.error == "Generation failed"

class TestAPIResponse:
    def test_successful_response(self):
        """Test successful API response."""
        data = {"message": "Success"}
        response = APIResponse(success=True, data=data)
        
        assert response.success is True
        assert response.data == data
        assert response.error is None

    def test_error_response(self):
        """Test error API response."""
        response = APIResponse(success=False, error="Something went wrong")
        
        assert response.success is False
        assert response.data is None
        assert response.error == "Something went wrong"

    def test_response_with_typed_data(self):
        """Test API response with typed data."""
        text_response = TextPromptResponse(response="AI response")
        api_response = APIResponse[TextPromptResponse](success=True, data=text_response)
        
        assert api_response.success is True
        assert api_response.data.response == "AI response"

    def test_minimal_response(self):
        """Test minimal API response."""
        response = APIResponse(success=True)
        
        assert response.success is True
        assert response.data is None
        assert response.error is None