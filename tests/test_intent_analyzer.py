from agent_library.intent_analyzer import IntentAnalyzer, IntentResult


class TestIntentAnalyzer:
    def test_init(self):
        """Test IntentAnalyzer initialization."""
        analyzer = IntentAnalyzer()
        assert analyzer.intent_patterns is not None
        assert 'create_timer' in analyzer.intent_patterns
        assert 'create_calculator' in analyzer.intent_patterns

    def test_analyze_timer_intent(self):
        """Test timer intent detection."""
        analyzer = IntentAnalyzer()
        result = analyzer.analyze_intent("Create a timer for 5 minutes")
        
        assert result.intent_type == 'create_timer'
        assert result.confidence > 0.3
        assert result.requires_plugin is True
        assert result.entities['type'] == 'timer'

    def test_analyze_calculator_intent(self):
        """Test calculator intent detection."""
        analyzer = IntentAnalyzer()
        result = analyzer.analyze_intent("I need a calculator")
        
        assert result.intent_type == 'create_calculator'
        assert result.confidence > 0.3
        assert result.requires_plugin is True
        assert result.entities['type'] == 'calculator'

    def test_analyze_document_intent(self):
        """Test document intent detection."""
        analyzer = IntentAnalyzer()
        result = analyzer.analyze_intent("Create a document for notes")
        
        assert result.intent_type == 'create_document'
        assert result.confidence > 0.3
        assert result.requires_plugin is False

    def test_analyze_general_query(self):
        """Test general query detection."""
        analyzer = IntentAnalyzer()
        result = analyzer.analyze_intent("What is the weather today?")
        
        assert result.intent_type == 'general_query'
        assert result.confidence > 0.3
        assert result.requires_plugin is False

    def test_analyze_unknown_intent(self):
        """Test unknown intent defaults to general query."""
        analyzer = IntentAnalyzer()
        result = analyzer.analyze_intent("Something completely random")
        
        assert result.intent_type == 'general_query'
        assert result.confidence == 0.5
        assert result.requires_plugin is False
        assert result.entities == {}

    def test_countdown_timer_entity_extraction(self):
        """Test countdown timer entity extraction."""
        analyzer = IntentAnalyzer()
        result = analyzer.analyze_intent("Create a countdown timer")
        
        assert result.intent_type == 'create_timer'
        assert result.entities['countdown'] is True

    def test_confidence_calculation(self):
        """Test confidence calculation method."""
        analyzer = IntentAnalyzer()
        
        # Test with multiple keywords
        confidence = analyzer._calculate_confidence("timer countdown", ['timer', 'countdown'])
        assert confidence > 0.8
        
        # Test with single keyword
        confidence = analyzer._calculate_confidence("timer", ['timer', 'countdown'])
        assert 0.3 <= confidence < 0.9

    def test_intent_result_model(self):
        """Test IntentResult pydantic model."""
        result = IntentResult(
            intent_type='create_timer',
            confidence=0.8,
            entities={'type': 'timer'},
            requires_plugin=True
        )
        
        assert result.intent_type == 'create_timer'
        assert result.confidence == 0.8
        assert result.entities == {'type': 'timer'}
        assert result.requires_plugin is True
        
        # Test model dict conversion
        result_dict = result.model_dump()
        assert 'intent_type' in result_dict
        assert 'confidence' in result_dict
