import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface ChatMessage {
  role: 'user' | 'companion';
  content: string;
  timestamp: string;
}

interface CompanionState {
  messages: ChatMessage[];
  personality: string;
  loading: boolean;
}

const initialState: CompanionState = {
  messages: [],
  personality: 'supportive_friend',
  loading: false,
};

const companionSlice = createSlice({
  name: 'companion',
  initialState,
  reducers: {
    addChatMessage: (state, action: PayloadAction<ChatMessage>) => {
      state.messages.push(action.payload);
    },
    setPersonality: (state, action: PayloadAction<string>) => {
      state.personality = action.payload;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
  },
});

export const { addChatMessage, setPersonality, setLoading } = companionSlice.actions;
export default companionSlice.reducer;
