import { configureStore } from '@reduxjs/toolkit';
import userReducer from './slices/userSlice';
import modeReducer from './slices/modeSlice';
import projectReducer from './slices/projectSlice';
import chatReducer from './slices/chatSlice';

export const store = configureStore({
    reducer: {
        user: userReducer,
        mode: modeReducer,
        project: projectReducer,
        chat: chatReducer,
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware({
            serializableCheck: {
                // Ignore these action types
                ignoredActions: ['user/setUser'],
                // Ignore these field paths in all actions
                ignoredActionPaths: ['payload.timestamp'],
                // Ignore these paths in the state
                ignoredPaths: ['user.auth'],
            },
        }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch; 