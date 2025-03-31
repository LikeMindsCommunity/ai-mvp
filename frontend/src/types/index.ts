
export type Role = 'user' | 'assistant';

export interface ChatMessage {
  id: string;
  role: Role;
  content: string;
  timestamp: Date;
}

export interface CodeFile {
  id: string;
  name: string;
  language: string;
  content: string;
}

export type DeviceViewMode = 'desktop' | 'tablet' | 'mobile';

export interface PreviewState {
  isLoading: boolean;
  error: string | null;
  deviceMode: DeviceViewMode;
  currentUrl: string;
}
