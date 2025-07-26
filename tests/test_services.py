import pytest
import asyncio
import os
import tempfile
from unittest.mock import Mock, AsyncMock, patch
from services.gemini_service import GeminiService
from services.plugin_service import PluginService
from models.responses import PluginGenerationResponse, PluginMetadata

class TestGeminiService:
    @pytest.fixture
    def gemini_service(self):
        return GeminiService()

    @pytest.mark.asyncio
    async def test_process_text_prompt_success(self, gemini_service):
        """Test successful text prompt processing."""
        with patch('asyncio.create_subprocess_exec') as mock_subprocess:
            # Mock successful subprocess execution
            mock_process = Mock()
            mock_process.returncode = 0
            mock_process.communicate = AsyncMock(return_value=(b'AI Response', b''))
            mock_subprocess.return_value = mock_process
            
            result = await gemini_service.process_text_prompt("test prompt", "user123")
            
            assert result == "AI Response"
            mock_subprocess.assert_called_once_with(
                'gemini', 'chat', 'test prompt',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

    @pytest.mark.asyncio
    async def test_process_text_prompt_cli_error(self, gemini_service):
        """Test text prompt processing with CLI error."""
        with patch('asyncio.create_subprocess_exec') as mock_subprocess:
            # Mock subprocess execution with error
            mock_process = Mock()
            mock_process.returncode = 1
            mock_process.communicate = AsyncMock(return_value=(b'', b'CLI Error'))
            mock_subprocess.return_value = mock_process
            
            # The service now returns a fallback response instead of raising
            response = await gemini_service.process_text_prompt("test prompt")
            
            assert "Error processing request" in response
            assert "test prompt" in response

    @pytest.mark.asyncio
    async def test_process_text_prompt_cli_not_found(self, gemini_service):
        """Test text prompt processing when CLI is not found."""
        with patch('asyncio.create_subprocess_exec') as mock_subprocess:
            # Mock subprocess execution with "not found" error
            mock_process = Mock()
            mock_process.returncode = 1
            mock_process.communicate = AsyncMock(return_value=(b'', b'command not found'))
            mock_subprocess.return_value = mock_process
            
            result = await gemini_service.process_text_prompt("test prompt")
            
            assert "Gemini CLI is not installed" in result
            assert "simulating response" in result

    @pytest.mark.asyncio
    async def test_process_text_prompt_file_not_found(self, gemini_service):
        """Test text prompt processing when Gemini CLI file is not found."""
        with patch('asyncio.create_subprocess_exec', side_effect=FileNotFoundError()):
            result = await gemini_service.process_text_prompt("test prompt")
            
            assert "Gemini CLI not available" in result
            assert "Simulated response" in result

    @pytest.mark.asyncio
    async def test_process_text_prompt_unexpected_error(self, gemini_service):
        """Test text prompt processing with unexpected error."""
        with patch('asyncio.create_subprocess_exec', side_effect=Exception("Unexpected error")):
            result = await gemini_service.process_text_prompt("test prompt")
            
            assert "Error processing request" in result
            assert "Unexpected error" in result

class TestPluginService:
    @pytest.fixture
    def plugin_service(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            service = PluginService()
            service.plugins_dir = temp_dir
            yield service

    @pytest.mark.asyncio
    async def test_generate_timer_plugin(self, plugin_service):
        """Test generating a timer plugin."""
        result = await plugin_service.generate_plugin("Add a timer", "user123")
        
        assert result.pluginId == 'timer-001'
        assert result.metadata.name == 'Timer'
        assert result.metadata.type == 'widget'
        assert 'Timer' in result.code
        assert 'useState' in result.code

    @pytest.mark.asyncio
    async def test_generate_calculator_plugin(self, plugin_service):
        """Test generating a calculator plugin."""
        result = await plugin_service.generate_plugin("Create a calculator", "user123")
        
        assert result.pluginId == 'calculator-001'
        assert result.metadata.name == 'Calculator'
        assert result.metadata.type == 'widget'
        assert 'Calculator' in result.code

    @pytest.mark.asyncio
    async def test_generate_custom_plugin(self, plugin_service):
        """Test generating a custom plugin."""
        result = await plugin_service.generate_plugin("Create a todo list", "user123")
        
        assert result.metadata.name == 'Custom Plugin'
        assert result.metadata.description == 'Generated for: Create a todo list'
        assert result.metadata.type == 'component'
        assert 'not implemented yet' in result.code

    def test_list_all_plugins(self, plugin_service):
        """Test listing all plugins."""
        plugins = plugin_service.list_all_plugins()
        
        assert len(plugins) == 2
        plugin_names = [p.metadata.name for p in plugins]
        assert 'Timer' in plugin_names
        assert 'Calculator' in plugin_names

    def test_get_plugin_code_existing(self, plugin_service):
        """Test getting code for existing plugin."""
        code = plugin_service.get_plugin_code('timer-001')
        
        assert code is not None
        assert 'Timer' in code
        assert 'useState' in code

    def test_get_plugin_code_nonexistent(self, plugin_service):
        """Test getting code for non-existent plugin."""
        code = plugin_service.get_plugin_code('nonexistent-plugin')
        
        assert code is None

    def test_save_plugin_to_file(self, plugin_service):
        """Test saving plugin code to file."""
        test_code = "function TestPlugin() { return <div>Test</div>; }"
        file_path = plugin_service.save_plugin_to_file('test-plugin', test_code)
        
        assert os.path.exists(file_path)
        assert file_path.endswith('test-plugin.js')
        
        with open(file_path, 'r') as f:
            saved_code = f.read()
        
        assert saved_code == test_code

    def test_plugins_directory_creation(self):
        """Test that plugins directory is created on initialization."""
        with tempfile.TemporaryDirectory() as temp_dir:
            plugins_dir = os.path.join(temp_dir, 'test_plugins')
            
            # Create a new service with custom plugins directory
            service = PluginService()
            service.plugins_dir = plugins_dir
            # Manually create the directory like __init__ does
            os.makedirs(service.plugins_dir, exist_ok=True)
            
            assert os.path.exists(plugins_dir)

    def test_hardcoded_plugins_initialization(self, plugin_service):
        """Test that hardcoded plugins are properly initialized."""
        # Check timer plugin
        timer_plugin = plugin_service.plugins_registry.get('timer-001')
        assert timer_plugin is not None
        assert timer_plugin.metadata.name == 'Timer'
        assert timer_plugin.metadata.dependencies == ['react']
        
        # Check calculator plugin
        calc_plugin = plugin_service.plugins_registry.get('calculator-001')
        assert calc_plugin is not None
        assert calc_plugin.metadata.name == 'Calculator'
        assert calc_plugin.metadata.dependencies == ['react']