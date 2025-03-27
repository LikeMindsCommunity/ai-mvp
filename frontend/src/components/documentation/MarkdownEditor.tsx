import React from 'react';
import MDEditor from '@uiw/react-md-editor';
import rehypeSanitize from 'rehype-sanitize';

interface MarkdownEditorProps {
    value: string;
    onChange: (value: string | undefined) => void;
}

const MarkdownEditor: React.FC<MarkdownEditorProps> = ({
    value,
    onChange,
}) => {
    return (
        <div data-color-mode="light" className="w-full h-full">
            <MDEditor
                value={value}
                onChange={onChange}
                height="100%"
                preview="live"
                previewOptions={{
                    rehypePlugins: [[rehypeSanitize]],
                }}
                className="w-full h-full border-none"
                textareaProps={{
                    placeholder: 'Start writing your documentation...',
                }}
            />
        </div>
    );
};

export default MarkdownEditor; 