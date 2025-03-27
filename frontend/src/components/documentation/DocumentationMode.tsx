import React, { useState } from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '@/store';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import ChatInterface from '@/components/chat/ChatInterface';
import MarkdownEditor from './MarkdownEditor';

const DocumentationMode: React.FC = () => {
    const { currentDocument } = useSelector((state: RootState) => state.mode.documentationMode);
    const { activeThreadId } = useSelector((state: RootState) => state.chat);
    const [markdown, setMarkdown] = useState<string>('');

    const handleMarkdownChange = (value: string | undefined) => {
        if (value !== undefined) {
            setMarkdown(value);
        }
    };

    return (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Left panel: Document editor */}
            <Card>
                <CardHeader>
                    <CardTitle>Document Editor</CardTitle>
                </CardHeader>
                <CardContent>
                    {currentDocument ? (
                        <div className="h-[600px] rounded-lg overflow-hidden border border-slate-200 dark:border-slate-700">
                            <MarkdownEditor
                                value={markdown}
                                onChange={handleMarkdownChange}
                            />
                        </div>
                    ) : (
                        <div className="text-center py-12">
                            <h3 className="text-lg font-medium text-slate-900 dark:text-white mb-2">
                                No Document Selected
                            </h3>
                            <p className="text-slate-600 dark:text-slate-400">
                                Select a document from the sidebar or create a new one to get started
                            </p>
                        </div>
                    )}
                </CardContent>
            </Card>

            {/* Right panel: AI Assistant */}
            <Card>
                <CardHeader>
                    <CardTitle>AI Assistant</CardTitle>
                </CardHeader>
                <CardContent className="h-[600px] p-0">
                    {activeThreadId ? (
                        <ChatInterface
                            threadId={activeThreadId}
                            mode="documentation"
                            context={{
                                documentId: currentDocument || undefined,
                            }}
                        />
                    ) : (
                        <div className="flex items-center justify-center h-full">
                            <p className="text-slate-600 dark:text-slate-400">
                                Select or create a chat thread to get started
                            </p>
                        </div>
                    )}
                </CardContent>
            </Card>
        </div>
    );
};

export default DocumentationMode; 