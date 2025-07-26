import { useState } from 'react';

interface CommandBarProps {
  onSubmit: (prompt: string) => void;
  isLoading?: boolean;
}

export default function CommandBar({ onSubmit, isLoading = false }: CommandBarProps) {
  const [input, setInput] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      onSubmit(input.trim());
      setInput('');
    }
  };

  const handleNotImplemented = () => {
    alert('Feature not implemented yet');
  };

  return (
    <div style={{ 
      padding: '16px', 
      borderTop: '1px solid #e0e0e0',
      backgroundColor: '#f5f5f5',
      display: 'flex',
      gap: '8px',
      alignItems: 'center'
    }}>
      <form onSubmit={handleSubmit} style={{ flex: 1, display: 'flex', gap: '8px' }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your command (e.g., 'Add a timer')..."
          disabled={isLoading}
          style={{
            flex: 1,
            padding: '8px 12px',
            border: '1px solid #ccc',
            borderRadius: '4px',
            fontSize: '14px'
          }}
        />
        <button
          type="submit"
          disabled={isLoading || !input.trim()}
          style={{
            padding: '8px 16px',
            backgroundColor: '#007acc',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: isLoading ? 'not-allowed' : 'pointer',
            fontSize: '14px'
          }}
        >
          {isLoading ? 'Processing...' : 'Send'}
        </button>
      </form>
      
      <button
        onClick={handleNotImplemented}
        disabled={isLoading}
        style={{
          padding: '8px',
          backgroundColor: '#f0f0f0',
          border: '1px solid #ccc',
          borderRadius: '4px',
          cursor: 'pointer',
          fontSize: '12px'
        }}
        title="Voice input (not implemented)"
      >
        🎤
      </button>
      
      <button
        onClick={handleNotImplemented}
        disabled={isLoading}
        style={{
          padding: '8px',
          backgroundColor: '#f0f0f0',
          border: '1px solid #ccc',
          borderRadius: '4px',
          cursor: 'pointer',
          fontSize: '12px'
        }}
        title="Image input (not implemented)"
      >
        📷
      </button>
    </div>
  );
}