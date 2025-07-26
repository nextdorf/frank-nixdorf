import { useState, useCallback } from 'react';
import type { Plugin } from '@shared/types';

export interface PluginManager {
  plugins: Plugin[];
  activePlugins: Plugin[];
  addPlugin: (plugin: Plugin) => void;
  removePlugin: (pluginId: string) => void;
  togglePlugin: (pluginId: string) => void;
  updatePlugin: (pluginId: string, updates: Partial<Plugin>) => void;
}

export function usePluginManager(): PluginManager {
  const [plugins, setPlugins] = useState<Plugin[]>([]);

  const addPlugin = useCallback((plugin: Plugin) => {
    setPlugins(current => {
      const exists = current.find(p => p.id === plugin.id);
      if (exists) {
        return current.map(p => p.id === plugin.id ? plugin : p);
      }
      return [...current, plugin];
    });
  }, []);

  const removePlugin = useCallback((pluginId: string) => {
    setPlugins(current => current.filter(p => p.id !== pluginId));
  }, []);

  const togglePlugin = useCallback((pluginId: string) => {
    setPlugins(current =>
      current.map(p =>
        p.id === pluginId ? { ...p, isActive: !p.isActive } : p
      )
    );
  }, []);

  const updatePlugin = useCallback((pluginId: string, updates: Partial<Plugin>) => {
    setPlugins(current =>
      current.map(p =>
        p.id === pluginId ? { ...p, ...updates } : p
      )
    );
  }, []);

  const activePlugins = plugins.filter(p => p.isActive);

  return {
    plugins,
    activePlugins,
    addPlugin,
    removePlugin,
    togglePlugin,
    updatePlugin
  };
}