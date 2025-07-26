import { describe, it, expect } from 'vitest'
import { server } from '../setup'
import { http, HttpResponse } from 'msw'
import { apiClient } from '../../services/apiClient'

describe('APIClient', () => {
  describe('sendTextPrompt', () => {
    it('successfully sends text prompt', async () => {
      const response = await apiClient.sendTextPrompt({
        prompt: 'Test prompt',
        userId: 'user123'
      })

      expect(response).toEqual({
        response: 'Mock AI response for testing'
      })
    })

    it('handles API error response', async () => {
      server.use(
        http.post('http://localhost:8000/api/prompt/text', () => {
          return HttpResponse.json({
            success: false,
            error: 'API Error'
          })
        })
      )

      await expect(apiClient.sendTextPrompt({ prompt: 'test' }))
        .rejects.toThrow('API Error')
    })

    it('handles network connection error', async () => {
      server.use(
        http.post('http://localhost:8000/api/prompt/text', () => {
          return HttpResponse.error()
        })
      )

      await expect(apiClient.sendTextPrompt({ prompt: 'test' }))
        .rejects.toThrow()
    })
  })

  describe('generatePlugin', () => {
    it('successfully generates plugin', async () => {
      const response = await apiClient.generatePlugin({
        description: 'Test plugin',
        userId: 'user123'
      })

      expect(response).toEqual({
        pluginId: 'test-plugin-123',
        code: 'function TestPlugin() { return <div>Test Plugin</div>; }',
        metadata: {
          name: 'Test Plugin',
          description: 'A test plugin',
          version: '1.0.0',
          type: 'component'
        }
      })
    })

    it('handles plugin generation error', async () => {
      server.use(
        http.post('http://localhost:8000/api/plugin/generate', () => {
          return HttpResponse.json({
            success: false,
            error: 'Plugin generation failed'
          })
        })
      )

      await expect(apiClient.generatePlugin({ description: 'test' }))
        .rejects.toThrow('Plugin generation failed')
    })
  })

  describe('listPlugins', () => {
    it('successfully lists plugins', async () => {
      const mockPlugins = [
        {
          pluginId: 'plugin1',
          code: 'code1',
          metadata: { name: 'Plugin 1', description: 'Desc 1', version: '1.0.0', type: 'component' as const }
        }
      ]

      server.use(
        http.get('http://localhost:8000/api/plugin/list', () => {
          return HttpResponse.json({
            success: true,
            data: mockPlugins
          })
        })
      )

      const response = await apiClient.listPlugins()
      expect(response).toEqual(mockPlugins)
    })

    it('handles empty plugin list', async () => {
      const response = await apiClient.listPlugins()
      expect(response).toEqual([])
    })
  })
})