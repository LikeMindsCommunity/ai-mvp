import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface Message {
    id: string;
    role: 'user' | 'assistant' | 'system';
    content: string;
    timestamp: number;
    metadata?: {
        codeBlocks?: {
            language: string;
            code: string;
        }[];
        files?: {
            name: string;
            content: string;
            type: string;
        }[];
        references?: {
            title: string;
            url: string;
        }[];
    };
}

interface ChatThread {
    id: string;
    title: string;
    messages: Message[];
    createdAt: number;
    updatedAt: number;
    mode: 'documentation' | 'coding';
    context?: {
        projectId?: string;
        documentId?: string;
        fileId?: string;
    };
}

interface ChatState {
    threads: ChatThread[];
    activeThreadId: string | null;
    isTyping: boolean;
    error: string | null;
    pendingMessages: {
        threadId: string;
        message: Omit<Message, 'id'>;
    }[];
}

const initialState: ChatState = {
    threads: [],
    activeThreadId: null,
    isTyping: false,
    error: null,
    pendingMessages: [],
};

const chatSlice = createSlice({
    name: 'chat',
    initialState,
    reducers: {
        createThread: (state, action: PayloadAction<{ title: string; mode: ChatThread['mode']; context?: ChatThread['context'] }>) => {
            const newThread: ChatThread = {
                id: Date.now().toString(),
                title: action.payload.title,
                messages: [],
                createdAt: Date.now(),
                updatedAt: Date.now(),
                mode: action.payload.mode,
                context: action.payload.context,
            };
            state.threads.push(newThread);
            state.activeThreadId = newThread.id;
        },
        setActiveThread: (state, action: PayloadAction<string>) => {
            state.activeThreadId = action.payload;
        },
        addMessage: (state, action: PayloadAction<{ threadId: string; message: Omit<Message, 'id'> }>) => {
            const thread = state.threads.find(t => t.id === action.payload.threadId);
            if (thread) {
                const newMessage: Message = {
                    ...action.payload.message,
                    id: Date.now().toString(),
                };
                thread.messages.push(newMessage);
                thread.updatedAt = Date.now();
            }
        },
        setTypingStatus: (state, action: PayloadAction<boolean>) => {
            state.isTyping = action.payload;
        },
        setError: (state, action: PayloadAction<string | null>) => {
            state.error = action.payload;
        },
        addPendingMessage: (state, action: PayloadAction<ChatState['pendingMessages'][0]>) => {
            state.pendingMessages.push(action.payload);
        },
        removePendingMessage: (state, action: PayloadAction<{ threadId: string; timestamp: number }>) => {
            state.pendingMessages = state.pendingMessages.filter(
                msg => !(msg.threadId === action.payload.threadId && msg.message.timestamp === action.payload.timestamp)
            );
        },
        clearThread: (state, action: PayloadAction<string>) => {
            const thread = state.threads.find(t => t.id === action.payload);
            if (thread) {
                thread.messages = [];
                thread.updatedAt = Date.now();
            }
        },
        deleteThread: (state, action: PayloadAction<string>) => {
            state.threads = state.threads.filter(t => t.id !== action.payload);
            if (state.activeThreadId === action.payload) {
                state.activeThreadId = state.threads[0]?.id || null;
            }
        },
    },
});

export const {
    createThread,
    setActiveThread,
    addMessage,
    setTypingStatus,
    setError,
    addPendingMessage,
    removePendingMessage,
    clearThread,
    deleteThread,
} = chatSlice.actions;

export default chatSlice.reducer; 