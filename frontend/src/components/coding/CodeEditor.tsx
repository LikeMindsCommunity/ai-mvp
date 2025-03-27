import React from 'react';
import Editor from '@monaco-editor/react';
import { useSelector } from 'react-redux';
import { RootState } from '@/store';

interface CodeEditorProps {
    value: string;
    onChange: (value: string | undefined) => void;
    language?: string;
}

const CodeEditor: React.FC<CodeEditorProps> = ({
    value,
    onChange,
    language = 'typescript',
}) => {
    const { preferences } = useSelector((state: RootState) => state.user);

    const handleEditorChange = (value: string | undefined) => {
        onChange(value);
    };

    return (
        <Editor
            height="100%"
            defaultLanguage={language}
            value={value}
            theme={preferences.theme === 'dark' ? 'vs-dark' : 'light'}
            onChange={handleEditorChange}
            options={{
                minimap: { enabled: false },
                fontSize: preferences.fontSize,
                wordWrap: 'on',
                lineNumbers: 'on',
                folding: true,
                automaticLayout: true,
                scrollBeyondLastLine: false,
            }}
        />
    );
};

export default CodeEditor; 