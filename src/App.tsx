import { useState } from 'react';
import DocumentEditor from './components/DocumentEditor';
import CommandBar from './components/CommandBar';
import PluginSidebar from './components/PluginSidebar';
import PluginToolbar from './components/PluginToolbar';
import PluginCanvas from './components/PluginCanvas';
import { usePluginManager } from './hooks/usePluginManager';
import { apiClient } from './services/apiClient';
import type { Plugin } from '@shared/types';

function App() {
  const [documentContent, setDocumentContent] = useState('# Welcome to The Anything App\n\nThis is your document workspace that extends itself via AI-generated plugins.\n\nTry typing a command like "Add a timer" in the command bar below!');
  const [isLoading, setIsLoading] = useState(false);
  const [lastResponse, setLastResponse] = useState<string>('');
  
  const pluginManager = usePluginManager();

  const handleCommand = async (prompt: string) => {
    setIsLoading(true);
    try {
      const textResponse = await apiClient.sendTextPrompt({ prompt });
      setLastResponse(textResponse.response);

      if (prompt.toLowerCase().includes('timer') || prompt.toLowerCase().includes('calculator')) {
        try {
          const pluginResponse = await apiClient.generatePlugin({ description: prompt });
          
          const newPlugin: Plugin = {
            id: pluginResponse.pluginId,
            metadata: pluginResponse.metadata,
            code: pluginResponse.code,
            isActive: true
          };
          
          pluginManager.addPlugin(newPlugin);
        } catch (pluginError) {
          console.error('Plugin generation failed:', pluginError);
        }
      }
    } catch (error) {
      console.error('Command failed:', error);
      setLastResponse(`Error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <header style={{ 
        padding: '12px 16px', 
        backgroundColor: '#2d3748', 
        color: 'white',
        borderBottom: '1px solid #4a5568'
      }}>
        <h1 style={{ margin: 0, fontSize: '18px', fontWeight: '600' }}>
          The Anything App
        </h1>
      </header>

      <PluginToolbar activePlugins={pluginManager.activePlugins} />

      <div style={{ flex: 1, display: 'flex' }}>
        <PluginSidebar 
          plugins={pluginManager.plugins}
          onPluginToggle={pluginManager.togglePlugin}
        />
        
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
          <div style={{ display: 'flex', flex: 1 }}>
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
              <div style={{ flex: 1 }}>
                <DocumentEditor 
                  value={documentContent}
                  onChange={setDocumentContent}
                />
              </div>
              
              {lastResponse && (
                <div style={{
                  padding: '12px',
                  backgroundColor: '#f0f8ff',
                  borderTop: '1px solid #e0e0e0',
                  fontSize: '14px',
                  maxHeight: '100px',
                  overflowY: 'auto'
                }}>
                  <strong>AI Response:</strong> {lastResponse}
                </div>
              )}
            </div>
            
            <PluginCanvas activePlugins={pluginManager.activePlugins} />
          </div>
          
          <CommandBar onSubmit={handleCommand} isLoading={isLoading} />
        </div>
      </div>
    </div>
  );
}

export default App
