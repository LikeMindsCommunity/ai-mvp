
import React, { useRef } from 'react';
import Editor from "@monaco-editor/react";
import { CodeFile } from '@/types';

interface MonacoEditorProps {
  file: CodeFile;
  onChange?: (value: string) => void;
  readOnly?: boolean;
}

export const MonacoEditor: React.FC<MonacoEditorProps> = ({ 
  file, 
  onChange,
  readOnly = false
}) => {
  const editorRef = useRef(null);

  const handleEditorDidMount = (editor) => {
    editorRef.current = editor;
  };

  const getLanguage = (fileLanguage: string) => {
    // Map the file language to Monaco language ID
    const languageMap = {
      'javascript': 'javascript',
      'typescript': 'typescript',
      'jsx': 'javascript',
      'tsx': 'typescript',
      'css': 'css',
      'html': 'html',
      'json': 'json',
    };
    
    return languageMap[fileLanguage.toLowerCase()] || 'javascript';
  };

  return (
    <Editor
      height="100%"
      defaultLanguage={getLanguage(file.language)}
      defaultValue={file.content}
      onChange={onChange}
      onMount={handleEditorDidMount}
      options={{
        minimap: { enabled: false },
        scrollBeyondLastLine: false,
        fontSize: 14,
        fontFamily: "'JetBrains Mono', monospace",
        lineNumbers: 'on',
        scrollbar: {
          useShadows: false,
          vertical: 'visible',
          horizontal: 'visible',
          verticalScrollbarSize: 10,
          horizontalScrollbarSize: 10
        },
        readOnly: readOnly,
        wordWrap: 'on',
        automaticLayout: true,
      }}
      theme="vs-dark"
    />
  );
};
