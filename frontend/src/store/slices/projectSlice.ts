import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface GitHubRepo {
    name: string;
    fullName: string;
    url: string;
    branch: string;
    private: boolean;
}

interface SDKConfig {
    platform: string;
    version: string;
    features: string[];
}

interface ProjectState {
    name: string | null;
    description: string | null;
    githubRepo: GitHubRepo | null;
    sdkConfig: SDKConfig | null;
    features: {
        id: string;
        name: string;
        status: 'pending' | 'in_progress' | 'completed';
        type: 'chat' | 'feed' | 'other';
    }[];
    dependencies: {
        name: string;
        version: string;
        type: 'production' | 'development';
    }[];
    lastSaved: number | null;
}

const initialState: ProjectState = {
    name: null,
    description: null,
    githubRepo: null,
    sdkConfig: null,
    features: [],
    dependencies: [],
    lastSaved: null,
};

const projectSlice = createSlice({
    name: 'project',
    initialState,
    reducers: {
        setProjectInfo: (state, action: PayloadAction<{ name: string; description: string }>) => {
            state.name = action.payload.name;
            state.description = action.payload.description;
            state.lastSaved = Date.now();
        },
        setGitHubRepo: (state, action: PayloadAction<GitHubRepo>) => {
            state.githubRepo = action.payload;
            state.lastSaved = Date.now();
        },
        setSDKConfig: (state, action: PayloadAction<SDKConfig>) => {
            state.sdkConfig = action.payload;
            state.lastSaved = Date.now();
        },
        addFeature: (state, action: PayloadAction<Omit<ProjectState['features'][0], 'status'>>) => {
            state.features.push({ ...action.payload, status: 'pending' });
            state.lastSaved = Date.now();
        },
        updateFeatureStatus: (state, action: PayloadAction<{ id: string; status: 'pending' | 'in_progress' | 'completed' }>) => {
            const feature = state.features.find(f => f.id === action.payload.id);
            if (feature) {
                feature.status = action.payload.status;
                state.lastSaved = Date.now();
            }
        },
        addDependency: (state, action: PayloadAction<ProjectState['dependencies'][0]>) => {
            state.dependencies.push(action.payload);
            state.lastSaved = Date.now();
        },
        removeDependency: (state, action: PayloadAction<string>) => {
            state.dependencies = state.dependencies.filter(dep => dep.name !== action.payload);
            state.lastSaved = Date.now();
        },
        resetProject: () => initialState,
    },
});

export const {
    setProjectInfo,
    setGitHubRepo,
    setSDKConfig,
    addFeature,
    updateFeatureStatus,
    addDependency,
    removeDependency,
    resetProject,
} = projectSlice.actions;

export default projectSlice.reducer; 