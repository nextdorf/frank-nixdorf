import type { Plugin } from '@shared/types';

interface PluginCanvasProps {
  activePlugins: Plugin[];
}

export default function PluginCanvas({ activePlugins }: PluginCanvasProps) {
  const canvasPlugins = activePlugins.filter(p => 
    p.metadata.type === 'component' || p.metadata.type === 'widget'
  );

  return (
    <div style={{
      flex: 1,
      backgroundColor: 'white',
      padding: '16px',
      overflowY: 'auto'
    }}>
      {canvasPlugins.length === 0 ? (
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          height: '200px',
          color: '#666',
          fontSize: '14px'
        }}>
          <div style={{ fontSize: '48px', marginBottom: '16px', opacity: 0.3 }}>
            🧩
          </div>
          <p>No active plugins in canvas</p>
          <p style={{ fontSize: '12px', textAlign: 'center', maxWidth: '300px' }}>
            Type a command like "Add a timer" to generate and activate plugins
          </p>
        </div>
      ) : (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '16px'
        }}>
          {canvasPlugins.map((plugin) => (
            <div
              key={plugin.id}
              style={{
                border: '1px solid #e0e0e0',
                borderRadius: '8px',
                padding: '16px',
                backgroundColor: '#fafafa'
              }}
            >
              <h4 style={{ margin: '0 0 8px 0', fontSize: '16px' }}>
                {plugin.metadata.name}
              </h4>
              <p style={{ margin: '0 0 12px 0', fontSize: '12px', color: '#666' }}>
                {plugin.metadata.description}
              </p>
              <div style={{
                backgroundColor: '#f0f0f0',
                padding: '12px',
                borderRadius: '4px',
                fontFamily: 'monospace',
                fontSize: '12px',
                border: '1px solid #ddd'
              }}>
                <div style={{ marginBottom: '8px', color: '#666' }}>
                  Plugin Code Preview:
                </div>
                <pre style={{ 
                  margin: 0, 
                  whiteSpace: 'pre-wrap',
                  maxHeight: '150px',
                  overflow: 'auto'
                }}>
                  {plugin.code.substring(0, 200)}
                  {plugin.code.length > 200 && '...'}
                </pre>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}