from agent_library.prompt_engineer import PromptEngineer


class TestPromptEngineer:
    def test_init(self):
        """Test PromptEngineer initialization."""
        pe = PromptEngineer()
        assert pe.prompt_templates is not None
        assert 'text_passthrough' in pe.prompt_templates
        assert 'plugin_generation' in pe.prompt_templates

    def test_process_text_prompt(self):
        """Test basic text prompt processing."""
        pe = PromptEngineer()
        result = pe.process_text_prompt("Hello world")
        
        assert result == "Hello world"

    def test_process_text_prompt_with_user_id(self):
        """Test text prompt processing with user ID."""
        pe = PromptEngineer()
        result = pe.process_text_prompt("Hello world", user_id="user123")
        
        # Currently user_id is not used in processing
        assert result == "Hello world"

    def test_enhance_prompt_for_plugin_generation(self):
        """Test plugin generation prompt enhancement."""
        pe = PromptEngineer()
        result = pe.enhance_prompt_for_plugin_generation("a timer widget", "component")
        
        expected = "Generate a component plugin that a timer widget"
        assert result == expected

    def test_enhance_prompt_for_plugin_generation_with_context(self):
        """Test plugin generation with context."""
        pe = PromptEngineer()
        context = {"framework": "React", "styling": "CSS"}
        result = pe.enhance_prompt_for_plugin_generation(
            "a calculator", 
            "widget", 
            context=context
        )
        
        assert "Generate a widget plugin that a calculator" in result
        assert "Context:" in result
        assert str(context) in result

    def test_craft_system_prompt_plugin_generation(self):
        """Test system prompt for plugin generation."""
        pe = PromptEngineer()
        result = pe.craft_system_prompt("plugin_generation")
        
        expected = "You are a code generation assistant. Create clean, functional React components."
        assert result == expected

    def test_craft_system_prompt_text_processing(self):
        """Test system prompt for text processing."""
        pe = PromptEngineer()
        result = pe.craft_system_prompt("text_processing")
        
        expected = "You are a helpful assistant that processes text requests."
        assert result == expected

    def test_craft_system_prompt_general(self):
        """Test general system prompt."""
        pe = PromptEngineer()
        result = pe.craft_system_prompt("general")
        
        expected = "You are a helpful AI assistant."
        assert result == expected

    def test_craft_system_prompt_unknown_type(self):
        """Test system prompt for unknown task type."""
        pe = PromptEngineer()
        result = pe.craft_system_prompt("unknown_type")
        
        expected = "You are a helpful AI assistant."
        assert result == expected

    def test_add_safety_constraints(self):
        """Test adding safety constraints to prompts."""
        pe = PromptEngineer()
        original_prompt = "Create a simple function"
        result = pe.add_safety_constraints(original_prompt)
        
        assert original_prompt in result
        assert "safe, appropriate, and follows best practices" in result
        assert result.endswith("safe, appropriate, and follows best practices.")

    def test_add_safety_constraints_empty_prompt(self):
        """Test adding safety constraints to empty prompt."""
        pe = PromptEngineer()
        result = pe.add_safety_constraints("")
        
        expected = "\n\nEnsure the response is safe, appropriate, and follows best practices."
        assert result == expected

    def test_prompt_template_formatting(self):
        """Test that prompt templates format correctly."""
        pe = PromptEngineer()
        
        # Test plugin generation template
        template = pe.prompt_templates['plugin_generation']
        result = template.format(plugin_type="widget", description="a clock")
        expected = "Generate a widget plugin that a clock"
        assert result == expected
        
        # Test text passthrough template
        template = pe.prompt_templates['text_passthrough']
        result = template.format(prompt="test message")
        expected = "test message"
        assert result == expected
