# Test Suite Instructions

This project now includes comprehensive test suites for both the frontend (React) and backend (FastAPI) components.

## Frontend Tests (React/TypeScript)

### Setup & Installation
```bash
cd frontend
npm install
```

### Running Tests

**Run all tests:**
```bash
npm test
```

**Run tests with UI (interactive mode):**
```bash
npm run test:ui
```

**Run tests with coverage:**
```bash
npm run test:coverage
```

**Run tests in watch mode:**
```bash
npm test -- --watch
```

### Test Structure
- **Location**: `frontend/src/test/`
- **Framework**: Vitest + React Testing Library
- **Setup**: `src/test/setup.ts` configures MSW for API mocking
- **Coverage**: HTML reports generated in `coverage/` directory

### Test Files:
- `App.test.tsx` - Main application component tests
- `services/apiClient.test.ts` - API client functionality tests
- `hooks/usePluginManager.test.ts` - Plugin management hook tests
- `components/CommandBar.test.tsx` - Command bar component tests

### Key Features Tested:
- ✅ App initialization and rendering
- ✅ Command submission and processing
- ✅ Plugin generation and management
- ✅ API client error handling
- ✅ User interactions and state management
- ✅ Loading states and form validation

## Backend Tests (Python/FastAPI)

### Setup & Installation
```bash
cd gemini-backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-test.txt
```

### Running Tests

**Run all tests:**
```bash
pytest
```

**Run tests with coverage:**
```bash
pytest --cov=. --cov-report=html
```

**Run specific test file:**
```bash
pytest tests/test_main.py
```

**Run tests with verbose output:**
```bash
pytest -v
```

### Test Structure
- **Location**: `gemini-backend/tests/`
- **Framework**: pytest + pytest-asyncio
- **Mocking**: unittest.mock for service mocking
- **Coverage**: HTML reports generated in `htmlcov/` directory

### Test Files:
- `conftest.py` - Test configuration and fixtures
- `test_main.py` - FastAPI endpoints integration tests
- `test_services.py` - Service layer unit tests
- `test_models.py` - Pydantic model validation tests

### Key Features Tested:
- ✅ All API endpoints (health, text prompt, plugin generation, plugin list, plugin serve)
- ✅ Service layer functionality (GeminiService, PluginService)
- ✅ Request/response model validation
- ✅ Error handling and edge cases
- ✅ Async functionality
- ✅ Plugin management and storage

## Running Full Test Suite

### Option 1: Run Both Test Suites Separately

**Terminal 1 (Frontend):**
```bash
cd frontend
npm install
npm test
```

**Terminal 2 (Backend):**
```bash
cd gemini-backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-test.txt
pytest
```

### Option 2: Run Tests with Coverage Reports

**Frontend with coverage:**
```bash
cd frontend
npm install
npm run test:coverage
# Open coverage/index.html in browser
```

**Backend with coverage:**
```bash
cd gemini-backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-test.txt
pytest --cov=. --cov-report=html
# Open htmlcov/index.html in browser
```

## Test Coverage

### Frontend Coverage Includes:
- Main App component and all interactions
- API client with success/error scenarios
- Plugin manager hook functionality
- Command bar component behavior
- Service mocking and network simulation

### Backend Coverage Includes:
- All FastAPI endpoints with success/error cases
- Service layer business logic
- Model validation and serialization
- Async operations and error handling
- Plugin generation and management

## Continuous Integration Ready

Both test suites are configured to run in CI/CD environments:

- **Frontend**: Uses jsdom for browser simulation, MSW for API mocking
- **Backend**: Uses pytest fixtures and mocks, supports async testing
- **Coverage**: Both generate coverage reports in standard formats
- **Exit Codes**: Both test suites return proper exit codes for CI/CD

## Troubleshooting

### Frontend Issues:
- If tests fail with import errors, ensure `@shared` alias is working
- If API tests fail, check MSW setup in `src/test/setup.ts`
- For React component tests, ensure proper cleanup with Testing Library

### Backend Issues:
- If import errors occur, check `sys.path` setup in `conftest.py`
- For async test failures, ensure `pytest-asyncio` is installed
- Mock issues usually relate to service injection in `conftest.py`

### Common Solutions:
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Clear Python cache: `find . -name "*.pyc" -delete && find . -name "__pycache__" -delete`
- Ensure Python virtual environment is activated
- Check that all test dependencies are installed

## Next Steps

The test suites are comprehensive and ready for development. Consider:

1. **Adding Integration Tests**: Tests that run both frontend and backend together
2. **E2E Tests**: Using tools like Playwright or Cypress
3. **Performance Tests**: Load testing for the backend API
4. **Visual Regression Tests**: Screenshot comparison for UI components