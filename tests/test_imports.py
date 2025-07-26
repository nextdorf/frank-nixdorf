class TestImports:
    def test_import_all_classes(self):
        """Test that all classes can be imported from the main module."""
        from agent_library import IntentAnalyzer, PromptEngineer, AudioHandler, ImageHandler
        
        # Test that classes can be instantiated
        intent_analyzer = IntentAnalyzer()
        prompt_engineer = PromptEngineer()
        audio_handler = AudioHandler()
        image_handler = ImageHandler()
        
        assert intent_analyzer is not None
        assert prompt_engineer is not None
        assert audio_handler is not None
        assert image_handler is not None

    def test_import_individual_modules(self):
        """Test that individual modules can be imported."""
        from agent_library.intent_analyzer import IntentAnalyzer
        from agent_library.prompt_engineer import PromptEngineer
        from agent_library.media_handlers import AudioHandler, ImageHandler
        from agent_library.main import AgentLibrary
        
        # Test instantiation
        analyzer = IntentAnalyzer()
        engineer = PromptEngineer()
        audio = AudioHandler()
        image = ImageHandler()
        library = AgentLibrary()
        
        assert all([analyzer, engineer, audio, image, library])

    def test___all___exports(self):
        """Test that __all__ contains the expected exports."""
        import agent_library
        
        expected_exports = ['IntentAnalyzer', 'PromptEngineer', 'AudioHandler', 'ImageHandler']
        assert hasattr(agent_library, '__all__')
        assert agent_library.__all__ == expected_exports
        
        # Test that all exported names are actually available
        for export in expected_exports:
            assert hasattr(agent_library, export)
