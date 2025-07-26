import { Editor } from '@monaco-editor/react';
import { useState } from 'react';

interface DocumentEditorProps {
  value?: string;
  onChange?: (value: string) => void;
}

export default function DocumentEditor({ value = '', onChange }: DocumentEditorProps) {
  const [content, setContent] = useState(value);

  const handleEditorChange = (newValue: string | undefined) => {
    const updatedValue = newValue || '';
    setContent(updatedValue);
    onChange?.(updatedValue);
  };

  return (
    <div style={{ height: '100%', width: '100%' }}>
      <Editor
        height="100%"
        defaultLanguage="plaintext"
        value={content}
        onChange={handleEditorChange}
        theme="vs-light"
        options={{
          minimap: { enabled: false },
          wordWrap: 'on',
          lineNumbers: 'on',
          scrollBeyondLastLine: false,
          automaticLayout: true,
        }}
      />
    </div>
  );
}