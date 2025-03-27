import React, { useState } from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '@/store';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import CodeEditor from './CodeEditor';
import ChatInterface from '@/components/chat/ChatInterface';

const CodingMode: React.FC = () => {
    const { currentFile, previewEnabled, platform } = useSelector((state: RootState) => state.mode.codingMode);
    const { sdkConfig } = useSelector((state: RootState) => state.project);
    const { activeThreadId } = useSelector((state: RootState) => state.chat);
    const [code, setCode] = useState<string>('');

    const handleCodeChange = (value: string | undefined) => {
        if (value !== undefined) {
            setCode(value);
        }
    };

    return (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Left panel: Code editor */}
            <Card>
                <CardHeader>
                    <CardTitle>Code Editor</CardTitle>
                </CardHeader>
                <CardContent>
                    {currentFile ? (
                        <div className="h-[600px] rounded-lg overflow-hidden border border-slate-200 dark:border-slate-700">
                            <CodeEditor
                                value={code}
                                onChange={handleCodeChange}
                                language={currentFile.endsWith('.ts') || currentFile.endsWith('.tsx') ? 'typescript' : 'javascript'}
                            />
                        </div>
                    ) : (
                        <div className="text-center py-12">
                            <h3 className="text-lg font-medium text-slate-900 dark:text-white mb-2">
                                No File Selected
                            </h3>
                            <p className="text-slate-600 dark:text-slate-400">
                                Select a file from the sidebar or create a new feature to get started
                            </p>
                        </div>
                    )}
                </CardContent>
            </Card>

            {/* Right panel: Preview and AI Assistant */}
            <div className="space-y-6">
                {/* Preview section */}
                {previewEnabled && (
                    <Card>
                        <CardHeader>
                            <CardTitle>
                                Preview
                                {platform && ` (${platform.toUpperCase()})`}
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="h-[300px] rounded-lg overflow-hidden border border-slate-200 dark:border-slate-700">
                                {/* Add Expo Web preview here */}
                                <p className="text-slate-600 dark:text-slate-400 text-center py-12">
                                    {sdkConfig ? (
                                        `Preview for ${sdkConfig.platform} will be shown here`
                                    ) : (
                                        'Configure SDK settings to enable preview'
                                    )}
                                </p>
                            </div>
                        </CardContent>
                    </Card>
                )}

                {/* AI Assistant */}
                <Card>
                    <CardHeader>
                        <CardTitle>AI Assistant</CardTitle>
                    </CardHeader>
                    <CardContent className="h-[300px] p-0">
                        {activeThreadId ? (
                            <ChatInterface
                                threadId={activeThreadId}
                                mode="coding"
                                context={{
                                    fileId: currentFile || undefined,
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
        </div>
    );
};

export default CodingMode; 