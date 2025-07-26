import { renderHook, act } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import { usePluginManager } from '../../hooks/usePluginManager'
import type { Plugin } from '@shared/types'

const mockPlugin: Plugin = {
  id: 'test-plugin-1',
  metadata: {
    name: 'Test Plugin',
    description: 'A test plugin',
    version: '1.0.0',
    type: 'component'
  },
  code: 'function TestPlugin() { return <div>Test</div>; }',
  isActive: false
}

describe('usePluginManager', () => {
  it('initializes with empty plugins array', () => {
    const { result } = renderHook(() => usePluginManager())
    
    expect(result.current.plugins).toEqual([])
    expect(result.current.activePlugins).toEqual([])
  })

  it('adds a new plugin', () => {
    const { result } = renderHook(() => usePluginManager())
    
    act(() => {
      result.current.addPlugin(mockPlugin)
    })
    
    expect(result.current.plugins).toHaveLength(1)
    expect(result.current.plugins[0]).toEqual(mockPlugin)
  })

  it('updates existing plugin when adding with same id', () => {
    const { result } = renderHook(() => usePluginManager())
    
    act(() => {
      result.current.addPlugin(mockPlugin)
    })
    
    const updatedPlugin = { ...mockPlugin, isActive: true }
    
    act(() => {
      result.current.addPlugin(updatedPlugin)
    })
    
    expect(result.current.plugins).toHaveLength(1)
    expect(result.current.plugins[0].isActive).toBe(true)
  })

  it('removes a plugin', () => {
    const { result } = renderHook(() => usePluginManager())
    
    act(() => {
      result.current.addPlugin(mockPlugin)
    })
    
    act(() => {
      result.current.removePlugin(mockPlugin.id)
    })
    
    expect(result.current.plugins).toHaveLength(0)
  })

  it('toggles plugin active state', () => {
    const { result } = renderHook(() => usePluginManager())
    
    act(() => {
      result.current.addPlugin(mockPlugin)
    })
    
    expect(result.current.plugins[0].isActive).toBe(false)
    
    act(() => {
      result.current.togglePlugin(mockPlugin.id)
    })
    
    expect(result.current.plugins[0].isActive).toBe(true)
    
    act(() => {
      result.current.togglePlugin(mockPlugin.id)
    })
    
    expect(result.current.plugins[0].isActive).toBe(false)
  })

  it('updates plugin with partial data', () => {
    const { result } = renderHook(() => usePluginManager())
    
    act(() => {
      result.current.addPlugin(mockPlugin)
    })
    
    act(() => {
      result.current.updatePlugin(mockPlugin.id, { 
        metadata: { ...mockPlugin.metadata, name: 'Updated Plugin' }
      })
    })
    
    expect(result.current.plugins[0].metadata.name).toBe('Updated Plugin')
  })

  it('filters active plugins correctly', () => {
    const { result } = renderHook(() => usePluginManager())
    
    const plugin1 = { ...mockPlugin, id: 'plugin1', isActive: true }
    const plugin2 = { ...mockPlugin, id: 'plugin2', isActive: false }
    const plugin3 = { ...mockPlugin, id: 'plugin3', isActive: true }
    
    act(() => {
      result.current.addPlugin(plugin1)
      result.current.addPlugin(plugin2)
      result.current.addPlugin(plugin3)
    })
    
    expect(result.current.plugins).toHaveLength(3)
    expect(result.current.activePlugins).toHaveLength(2)
    expect(result.current.activePlugins.map(p => p.id)).toEqual(['plugin1', 'plugin3'])
  })

  it('handles operations on non-existent plugins gracefully', () => {
    const { result } = renderHook(() => usePluginManager())
    
    act(() => {
      result.current.removePlugin('non-existent-id')
      result.current.togglePlugin('non-existent-id')
      result.current.updatePlugin('non-existent-id', { isActive: true })
    })
    
    expect(result.current.plugins).toHaveLength(0)
  })
})