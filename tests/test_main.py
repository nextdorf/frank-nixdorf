from agent_library.main import AgentLibrary


class TestAgentLibrary:
    def test_init(self):
        """Test AgentLibrary initialization."""
        library = AgentLibrary()
        
        assert library.intent_analyzer is not None
        assert library.prompt_engineer is not None
        assert library.audio_handler is not None
        assert library.image_handler is not None

    def test_process_text_request(self):
        """Test processing text requests."""
        library = AgentLibrary()
        request_data = {
            'type': 'text',
            'text': 'Create a timer',
            'user_id': 'user123'
        }
        
        result = library.process_request(request_data)
        
        assert result['type'] == 'text'
        assert 'processed_prompt' in result
        assert 'intent' in result
        assert result['processed_prompt'] == 'Create a timer'
        assert result['intent']['intent_type'] == 'create_timer'

    def test_process_text_request_no_user_id(self):
        """Test processing text requests without user ID."""
        library = AgentLibrary()
        request_data = {
            'type': 'text',
            'text': 'Hello world'
        }
        
        result = library.process_request(request_data)
        
        assert result['type'] == 'text'
        assert result['processed_prompt'] == 'Hello world'

    def test_process_text_request_empty_text(self):
        """Test processing text requests with empty text."""
        library = AgentLibrary()
        request_data = {
            'type': 'text'
        }
        
        result = library.process_request(request_data)
        
        assert result['type'] == 'text'
        assert result['processed_prompt'] == ''

    def test_process_audio_request(self):
        """Test processing audio requests."""
        library = AgentLibrary()
        request_data = {
            'type': 'audio',
            'audio_data': b'fake_audio',
            'format': 'mp3'
        }
        
        result = library.process_request(request_data)
        
        assert result['type'] == 'audio'
        assert 'audio_result' in result
        assert result['audio_result']['status'] == 'not_implemented'
        assert result['audio_result']['received_format'] == 'mp3'

    def test_process_audio_request_default_format(self):
        """Test processing audio requests with default format."""
        library = AgentLibrary()
        request_data = {
            'type': 'audio',
            'audio_data': b'fake_audio'
        }
        
        result = library.process_request(request_data)
        
        assert result['type'] == 'audio'
        assert result['audio_result']['received_format'] == 'wav'

    def test_process_audio_request_empty_data(self):
        """Test processing audio requests with empty data."""
        library = AgentLibrary()
        request_data = {
            'type': 'audio'
        }
        
        result = library.process_request(request_data)
        
        assert result['type'] == 'audio'
        assert 'audio_result' in result

    def test_process_image_request(self):
        """Test processing image requests."""
        library = AgentLibrary()
        request_data = {
            'type': 'image',
            'image_data': b'fake_image',
            'format': 'jpg'
        }
        
        result = library.process_request(request_data)
        
        assert result['type'] == 'image'
        assert 'image_result' in result
        assert result['image_result']['status'] == 'not_implemented'
        assert result['image_result']['received_format'] == 'jpg'

    def test_process_image_request_default_format(self):
        """Test processing image requests with default format."""
        library = AgentLibrary()
        request_data = {
            'type': 'image',
            'image_data': b'fake_image'
        }
        
        result = library.process_request(request_data)
        
        assert result['type'] == 'image'
        assert result['image_result']['received_format'] == 'png'

    def test_process_image_request_empty_data(self):
        """Test processing image requests with empty data."""
        library = AgentLibrary()
        request_data = {
            'type': 'image'
        }
        
        result = library.process_request(request_data)
        
        assert result['type'] == 'image'
        assert 'image_result' in result

    def test_process_unsupported_request_type(self):
        """Test processing unsupported request types."""
        library = AgentLibrary()
        request_data = {
            'type': 'video',
            'data': 'some_data'
        }
        
        result = library.process_request(request_data)
        
        assert 'error' in result
        assert 'Unsupported request type: video' in result['error']

    def test_process_request_no_type(self):
        """Test processing request with no type (defaults to text)."""
        library = AgentLibrary()
        request_data = {
            'text': 'Hello world'
        }
        
        result = library.process_request(request_data)
        
        assert result['type'] == 'text'
        assert result['processed_prompt'] == 'Hello world'

    def test_private_methods_exist(self):
        """Test that private methods exist and are callable."""
        library = AgentLibrary()
        
        # Test that private methods exist
        assert hasattr(library, '_process_text_request')
        assert hasattr(library, '_process_audio_request')
        assert hasattr(library, '_process_image_request')
        
        # Test that they're callable
        assert callable(library._process_text_request)
        assert callable(library._process_audio_request)
        assert callable(library._process_image_request)
