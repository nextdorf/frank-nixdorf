import type { Plugin } from '@shared/types';

interface PluginToolbarProps {
  activePlugins: Plugin[];
}

export default function PluginToolbar({ activePlugins }: PluginToolbarProps) {
  const toolbarPlugins = activePlugins.filter(p => p.metadata.type === 'utility');

  return (
    <div style={{
      height: '48px',
      backgroundColor: '#f5f5f5',
      borderBottom: '1px solid #e0e0e0',
      padding: '0 16px',
      display: 'flex',
      alignItems: 'center',
      gap: '8px'
    }}>
      <span style={{ fontSize: '14px', fontWeight: '500', marginRight: '16px' }}>
        Tools:
      </span>
      
      {toolbarPlugins.length === 0 ? (
        <span style={{ fontSize: '12px', color: '#666', fontStyle: 'italic' }}>
          No active tools
        </span>
      ) : (
        toolbarPlugins.map((plugin) => (
          <button
            key={plugin.id}
            style={{
              padding: '6px 12px',
              backgroundColor: '#007acc',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              fontSize: '12px',
              cursor: 'pointer'
            }}
            onClick={() => {
              console.log(`Executing plugin: ${plugin.metadata.name}`);
            }}
          >
            {plugin.metadata.name}
          </button>
        ))
      )}
    </div>
  );
}