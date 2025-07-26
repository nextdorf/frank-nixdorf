import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from services.gemini_service import GeminiService
from services.plugin_service import PluginService

@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)

@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Create an async test client for the FastAPI app."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def mock_gemini_service():
    """Mock the Gemini service."""
    service = Mock(spec=GeminiService)
    service.process_text_prompt = AsyncMock(return_value="Mock AI response")
    return service

@pytest.fixture
def mock_plugin_service():
    """Mock the Plugin service."""
    service = Mock(spec=PluginService)
    service.generate_plugin = AsyncMock(return_value={
        'pluginId': 'test-plugin-123',
        'code': 'function TestPlugin() { return <div>Test Plugin</div>; }',
        'metadata': {
            'name': 'Test Plugin',
            'description': 'A test plugin',
            'version': '1.0.0',
            'type': 'component'
        }
    })
    service.list_all_plugins = Mock(return_value=[])
    service.get_plugin_code = Mock(return_value='test code')
    return service

@pytest.fixture(autouse=True)
def mock_services(monkeypatch, mock_gemini_service, mock_plugin_service):
    """Auto-mock services for all tests."""
    monkeypatch.setattr('main.gemini_service', mock_gemini_service)
    monkeypatch.setattr('main.plugin_service', mock_plugin_service)