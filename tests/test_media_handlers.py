import base64
from agent_library.media_handlers import AudioHandler, ImageHandler


class TestAudioHandler:
    def test_init(self):
        """Test AudioHandler initialization."""
        handler = AudioHandler()
        assert handler.supported_formats == ['mp3', 'wav', 'ogg', 'm4a']

    def test_process_audio_default_format(self):
        """Test audio processing with default format."""
        handler = AudioHandler()
        audio_data = b"fake_audio_data"
        result = handler.process_audio(audio_data)
        
        assert result['status'] == 'not_implemented'
        assert result['message'] == 'Audio processing is not implemented yet'
        assert result['supported_formats'] == ['mp3', 'wav', 'ogg', 'm4a']
        assert result['received_format'] == 'wav'

    def test_process_audio_custom_format(self):
        """Test audio processing with custom format."""
        handler = AudioHandler()
        audio_data = b"fake_audio_data"
        result = handler.process_audio(audio_data, format='mp3')
        
        assert result['status'] == 'not_implemented'
        assert result['received_format'] == 'mp3'

    def test_transcribe_audio(self):
        """Test audio transcription (not implemented)."""
        handler = AudioHandler()
        audio_data = b"fake_audio_data"
        result = handler.transcribe_audio(audio_data)
        
        assert result == 'Audio transcription not implemented yet'

    def test_validate_audio_format_valid(self):
        """Test validation of valid audio formats."""
        handler = AudioHandler()
        
        assert handler.validate_audio_format('mp3') is True
        assert handler.validate_audio_format('wav') is True
        assert handler.validate_audio_format('MP3') is True  # Case insensitive

    def test_validate_audio_format_invalid(self):
        """Test validation of invalid audio formats."""
        handler = AudioHandler()
        
        assert handler.validate_audio_format('txt') is False
        assert handler.validate_audio_format('avi') is False
        assert handler.validate_audio_format('') is False


class TestImageHandler:
    def test_init(self):
        """Test ImageHandler initialization."""
        handler = ImageHandler()
        assert handler.supported_formats == ['jpg', 'jpeg', 'png', 'gif', 'webp']

    def test_process_image_default_format(self):
        """Test image processing with default format."""
        handler = ImageHandler()
        image_data = b"fake_image_data"
        result = handler.process_image(image_data)
        
        assert result['status'] == 'not_implemented'
        assert result['message'] == 'Image processing is not implemented yet'
        assert result['supported_formats'] == ['jpg', 'jpeg', 'png', 'gif', 'webp']
        assert result['received_format'] == 'png'

    def test_process_image_custom_format(self):
        """Test image processing with custom format."""
        handler = ImageHandler()
        image_data = b"fake_image_data"
        result = handler.process_image(image_data, format='jpg')
        
        assert result['status'] == 'not_implemented'
        assert result['received_format'] == 'jpg'

    def test_analyze_image(self):
        """Test image analysis (not implemented)."""
        handler = ImageHandler()
        image_data = b"fake_image_data"
        result = handler.analyze_image(image_data)
        
        assert result == 'Image analysis not implemented yet'

    def test_extract_text_from_image(self):
        """Test OCR functionality (not implemented)."""
        handler = ImageHandler()
        image_data = b"fake_image_data"
        result = handler.extract_text_from_image(image_data)
        
        assert result == 'OCR functionality not implemented yet'

    def test_validate_image_format_valid(self):
        """Test validation of valid image formats."""
        handler = ImageHandler()
        
        assert handler.validate_image_format('jpg') is True
        assert handler.validate_image_format('png') is True
        assert handler.validate_image_format('JPEG') is True  # Case insensitive

    def test_validate_image_format_invalid(self):
        """Test validation of invalid image formats."""
        handler = ImageHandler()
        
        assert handler.validate_image_format('txt') is False
        assert handler.validate_image_format('pdf') is False
        assert handler.validate_image_format('') is False

    def test_encode_image_base64(self):
        """Test base64 encoding of image data."""
        handler = ImageHandler()
        image_data = b"test_image_data"
        result = handler.encode_image_base64(image_data)
        
        # Verify it's valid base64
        expected = base64.b64encode(image_data).decode('utf-8')
        assert result == expected
        
        # Verify we can decode it back
        decoded = base64.b64decode(result)
        assert decoded == image_data

    def test_encode_image_base64_empty(self):
        """Test base64 encoding of empty image data."""
        handler = ImageHandler()
        result = handler.encode_image_base64(b"")
        
        expected = base64.b64encode(b"").decode('utf-8')
        assert result == expected
