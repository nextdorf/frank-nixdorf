import type { Plugin } from '@shared/types';

interface PluginSidebarProps {
  plugins: Plugin[];
  onPluginToggle: (pluginId: string) => void;
}

export default function PluginSidebar({ plugins, onPluginToggle }: PluginSidebarProps) {
  return (
    <div style={{
      width: '250px',
      backgroundColor: '#f8f9fa',
      borderRight: '1px solid #e0e0e0',
      padding: '16px',
      overflowY: 'auto'
    }}>
      <h3 style={{ margin: '0 0 16px 0', fontSize: '16px', fontWeight: '600' }}>
        Plugins
      </h3>
      
      {plugins.length === 0 ? (
        <p style={{ color: '#666', fontSize: '14px', fontStyle: 'italic' }}>
          No plugins available
        </p>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {plugins.map((plugin) => (
            <div
              key={plugin.id}
              style={{
                padding: '12px',
                backgroundColor: plugin.isActive ? '#e3f2fd' : 'white',
                border: '1px solid #e0e0e0',
                borderRadius: '6px',
                cursor: 'pointer'
              }}
              onClick={() => onPluginToggle(plugin.id)}
            >
              <div style={{ 
                display: 'flex', 
                justifyContent: 'space-between', 
                alignItems: 'center',
                marginBottom: '4px'
              }}>
                <strong style={{ fontSize: '14px' }}>{plugin.metadata.name}</strong>
                <span style={{
                  fontSize: '12px',
                  padding: '2px 6px',
                  backgroundColor: plugin.isActive ? '#4caf50' : '#ccc',
                  color: 'white',
                  borderRadius: '3px'
                }}>
                  {plugin.isActive ? 'ON' : 'OFF'}
                </span>
              </div>
              <p style={{ 
                margin: 0, 
                fontSize: '12px', 
                color: '#666',
                lineHeight: '1.3'
              }}>
                {plugin.metadata.description}
              </p>
              <div style={{ marginTop: '4px', fontSize: '11px', color: '#999' }}>
                v{plugin.metadata.version} • {plugin.metadata.type}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}