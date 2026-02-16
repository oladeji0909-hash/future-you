import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface Message {
  id: number;
  content: string;
  message_type: string;
  status: string;
  delivery_timing: string;
  scheduled_for: string | null;
  created_at: string;
  tags: string[];
}

interface MessagesState {
  messages: Message[];
  loading: boolean;
}

const initialState: MessagesState = {
  messages: [],
  loading: false,
};

const messagesSlice = createSlice({
  name: 'messages',
  initialState,
  reducers: {
    setMessages: (state, action: PayloadAction<Message[]>) => {
      state.messages = action.payload;
    },
    addMessage: (state, action: PayloadAction<Message>) => {
      state.messages.unshift(action.payload);
    },
    removeMessage: (state, action: PayloadAction<number>) => {
      state.messages = state.messages.filter(msg => msg.id !== action.payload);
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
  },
});

export const { setMessages, addMessage, removeMessage, setLoading } = messagesSlice.actions;
export default messagesSlice.reducer;
