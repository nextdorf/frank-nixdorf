import '@testing-library/jest-dom'
import { beforeAll, afterEach, afterAll } from 'vitest'
import { setupServer } from 'msw/node'
import { http, HttpResponse } from 'msw'

// Mock API server
export const server = setupServer(
  // Mock text prompt endpoint
  http.post('http://localhost:8000/api/prompt/text', () => {
    return HttpResponse.json({
      success: true,
      data: {
        response: 'Mock AI response for testing'
      }
    })
  }),

  // Mock plugin generation endpoint
  http.post('http://localhost:8000/api/plugin/generate', () => {
    return HttpResponse.json({
      success: true,
      data: {
        pluginId: 'test-plugin-123',
        code: 'function TestPlugin() { return <div>Test Plugin</div>; }',
        metadata: {
          name: 'Test Plugin',
          description: 'A test plugin',
          version: '1.0.0',
          type: 'component'
        }
      }
    })
  }),

  // Mock plugin list endpoint
  http.get('http://localhost:8000/api/plugin/list', () => {
    return HttpResponse.json({
      success: true,
      data: []
    })
  })
)

// Establish API mocking before all tests
beforeAll(() => server.listen())

// Reset any request handlers that we may add during the tests
afterEach(() => server.resetHandlers())

// Clean up after the tests are finished
afterAll(() => server.close())