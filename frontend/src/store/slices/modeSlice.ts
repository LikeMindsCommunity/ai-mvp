import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export type AppMode = 'documentation' | 'coding';

interface ModeState {
    currentMode: AppMode;
    documentationMode: {
        currentDocument: string | null;
        documentHistory: string[];
        lastEditTimestamp: number | null;
    };
    codingMode: {
        currentFile: string | null;
        openFiles: string[];
        previewEnabled: boolean;
        deviceOrientation: 'portrait' | 'landscape';
        platform: 'ios' | 'android' | 'web' | null;
    };
}

const initialState: ModeState = {
    currentMode: 'documentation',
    documentationMode: {
        currentDocument: null,
        documentHistory: [],
        lastEditTimestamp: null,
    },
    codingMode: {
        currentFile: null,
        openFiles: [],
        previewEnabled: true,
        deviceOrientation: 'portrait',
        platform: null,
    },
};

const modeSlice = createSlice({
    name: 'mode',
    initialState,
    reducers: {
        setMode: (state, action: PayloadAction<AppMode>) => {
            state.currentMode = action.payload;
        },
        setCurrentDocument: (state, action: PayloadAction<string>) => {
            state.documentationMode.currentDocument = action.payload;
            state.documentationMode.documentHistory.push(action.payload);
            state.documentationMode.lastEditTimestamp = Date.now();
        },
        setCurrentFile: (state, action: PayloadAction<string>) => {
            state.codingMode.currentFile = action.payload;
            if (!state.codingMode.openFiles.includes(action.payload)) {
                state.codingMode.openFiles.push(action.payload);
            }
        },
        closeFile: (state, action: PayloadAction<string>) => {
            state.codingMode.openFiles = state.codingMode.openFiles.filter(
                file => file !== action.payload
            );
            if (state.codingMode.currentFile === action.payload) {
                state.codingMode.currentFile = state.codingMode.openFiles[0] || null;
            }
        },
        togglePreview: (state) => {
            state.codingMode.previewEnabled = !state.codingMode.previewEnabled;
        },
        setDeviceOrientation: (state, action: PayloadAction<'portrait' | 'landscape'>) => {
            state.codingMode.deviceOrientation = action.payload;
        },
        setPlatform: (state, action: PayloadAction<'ios' | 'android' | 'web' | null>) => {
            state.codingMode.platform = action.payload;
        },
        clearDocumentHistory: (state) => {
            state.documentationMode.documentHistory = [];
        },
    },
});

export const {
    setMode,
    setCurrentDocument,
    setCurrentFile,
    closeFile,
    togglePreview,
    setDeviceOrientation,
    setPlatform,
    clearDocumentHistory,
} = modeSlice.actions;

export default modeSlice.reducer; 