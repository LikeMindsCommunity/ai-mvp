import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface UserPreferences {
    theme: 'light' | 'dark';
    fontSize: number;
    useStreamingMode: boolean;
}

interface UserState {
    isAuthenticated: boolean;
    user: {
        id?: string;
        email?: string;
        name?: string;
        picture?: string;
    } | null;
    preferences: UserPreferences;
    githubToken?: string;
    likemindsApiKey?: string;
}

const initialState: UserState = {
    isAuthenticated: false,
    user: null,
    preferences: {
        theme: 'light',
        fontSize: 14,
        useStreamingMode: true,
    },
};

const userSlice = createSlice({
    name: 'user',
    initialState,
    reducers: {
        setUser: (state, action: PayloadAction<UserState['user']>) => {
            state.user = action.payload;
            state.isAuthenticated = !!action.payload;
        },
        setPreferences: (state, action: PayloadAction<Partial<UserPreferences>>) => {
            state.preferences = { ...state.preferences, ...action.payload };
        },
        setGithubToken: (state, action: PayloadAction<string>) => {
            state.githubToken = action.payload;
        },
        setLikemindsApiKey: (state, action: PayloadAction<string>) => {
            state.likemindsApiKey = action.payload;
        },
        logout: (state) => {
            state.isAuthenticated = false;
            state.user = null;
            state.githubToken = undefined;
            state.likemindsApiKey = undefined;
        },
    },
});

export const {
    setUser,
    setPreferences,
    setGithubToken,
    setLikemindsApiKey,
    logout,
} = userSlice.actions;

export default userSlice.reducer; 