import { configureStore } from '@reduxjs/toolkit';
import authReducer from '../slices/authSlice';
import messagesReducer from '../slices/messagesSlice';
import companionReducer from '../slices/companionSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    messages: messagesReducer,
    companion: companionReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
