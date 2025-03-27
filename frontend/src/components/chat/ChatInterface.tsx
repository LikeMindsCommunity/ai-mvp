import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '@/store';
import { addMessage, setTypingStatus } from '@/store/slices/chatSlice';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Message } from '@/store/slices/chatSlice';
import ReactMarkdown from 'react-markdown';

interface ChatInterfaceProps {
    threadId: string;
    mode: 'documentation' | 'coding';
    context?: {
        projectId?: string;
        documentId?: string;
        fileId?: string;
    };
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({
    threadId,
    mode,
    context,
}) => {
    const dispatch = useDispatch();
    const [input, setInput] = useState('');
    const { threads, isTyping } = useSelector((state: RootState) => state.chat);
    const currentThread = threads.find(t => t.id === threadId);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || isTyping) return;

        const message: Omit<Message, 'id'> = {
            role: 'user',
            content: input,
            timestamp: Date.now(),
        };

        dispatch(addMessage({ threadId, message }));
        setInput('');
        dispatch(setTypingStatus(true));

        try {
            // TODO: Implement API call to get AI response
            // const response = await fetch('/api/chat', ...);
            // dispatch(addMessage({ threadId, message: response }));
        } catch (error) {
            console.error('Error getting AI response:', error);
        } finally {
            dispatch(setTypingStatus(false));
        }
    };

    return (
        <div className="flex flex-col h-full">
            <div className="flex-1 overflow-y-auto space-y-4 p-4">
                {currentThread?.messages.map((message) => (
                    <div
                        key={message.id}
                        className={`flex ${message.role === 'assistant' ? 'justify-start' : 'justify-end'
                            }`}
                    >
                        <div
                            className={`max-w-[80%] rounded-lg p-4 ${message.role === 'assistant'
                                    ? 'bg-slate-100 dark:bg-slate-800'
                                    : 'bg-violet-100 dark:bg-violet-900'
                                }`}
                        >
                            <div className="prose dark:prose-invert max-w-none">
                                <ReactMarkdown>
                                    {message.content}
                                </ReactMarkdown>
                            </div>
                            {message.metadata && (
                                <div className="mt-2 pt-2 border-t border-slate-200 dark:border-slate-700">
                                    {message.metadata.codeBlocks?.map((block, index) => (
                                        <pre key={index} className="mt-2 p-2 bg-slate-800 rounded text-white">
                                            <code>{block.code}</code>
                                        </pre>
                                    ))}
                                    {message.metadata.references?.map((ref, index) => (
                                        <a
                                            key={index}
                                            href={ref.url}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="block mt-1 text-sm text-violet-600 dark:text-violet-400 hover:underline"
                                        >
                                            {ref.title}
                                        </a>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                ))}
                {isTyping && (
                    <div className="flex justify-start">
                        <div className="bg-slate-100 dark:bg-slate-800 rounded-lg p-4">
                            <div className="flex space-x-2">
                                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" />
                                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-100" />
                                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-200" />
                            </div>
                        </div>
                    </div>
                )}
            </div>

            <form onSubmit={handleSubmit} className="p-4 border-t border-slate-200 dark:border-slate-700">
                <div className="flex space-x-2">
                    <Textarea
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder={`Ask about ${mode === 'documentation' ? 'documentation' : 'code'}...`}
                        className="min-h-[60px]"
                    />
                    <Button type="submit" disabled={isTyping || !input.trim()}>
                        Send
                    </Button>
                </div>
            </form>
        </div>
    );
};

export default ChatInterface; 