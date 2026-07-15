import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { sendMessage as sendChatAPI } from '../services/chatAPI';
import { setMultipleFields } from './interactionSlice';
import { setActiveTool, addToHistory } from './toolSlice';
import { addToast } from './uiSlice';
import { AI_WELCOME_MESSAGE } from '../utils/constants';
import { generateSessionId } from '../utils/helpers';

export const sendChatMessage = createAsyncThunk('chat/sendMessage', async (message, { dispatch, getState, rejectWithValue }) => {
  try {
    const { chat } = getState();
    const result = await sendChatAPI(message, chat.sessionId);

    // Apply form updates if AI extracted data
    if (result.form_updates && Object.keys(result.form_updates).length > 0) {
      dispatch(setMultipleFields(result.form_updates));
      dispatch(addToast({ type: 'success', message: '✨ Form auto-filled with AI-extracted data' }));
    }

    // Track tool calls
    if (result.tool_calls?.length > 0) {
      result.tool_calls.forEach(tc => {
        dispatch(addToHistory(tc));
      });
    }

    return result;
  } catch (e) {
    return rejectWithValue(e.response?.data?.detail || 'Failed to send message');
  }
});

const chatSlice = createSlice({
  name: 'chat',
  initialState: {
    messages: [{ ...AI_WELCOME_MESSAGE, id: 'welcome' }],
    isTyping: false,
    sessionId: generateSessionId(),
    suggestions: [],
    error: null,
  },
  reducers: {
    addMessage: (state, action) => { state.messages.push({ ...action.payload, id: Date.now().toString(), timestamp: new Date().toISOString() }); },
    setTyping: (state, action) => { state.isTyping = action.payload; },
    setSuggestions: (state, action) => { state.suggestions = action.payload; },
    clearChat: (state) => { state.messages = [{ ...AI_WELCOME_MESSAGE, id: 'welcome' }]; state.suggestions = []; state.sessionId = generateSessionId(); },
    clearError: (state) => { state.error = null; },
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendChatMessage.pending, (state, action) => {
        state.isTyping = true;
        state.error = null;
        state.messages.push({ id: Date.now().toString(), role: 'user', content: action.meta.arg, timestamp: new Date().toISOString() });
      })
      .addCase(sendChatMessage.fulfilled, (state, action) => {
        state.isTyping = false;
        state.messages.push({
          id: (Date.now() + 1).toString(), role: 'assistant',
          content: action.payload.response,
          toolCalls: action.payload.tool_calls || [],
          timestamp: new Date().toISOString(),
        });
        if (action.payload.suggestions?.length > 0) state.suggestions = action.payload.suggestions;
      })
      .addCase(sendChatMessage.rejected, (state, action) => {
        state.isTyping = false;
        state.error = action.payload;
        state.messages.push({ id: (Date.now() + 1).toString(), role: 'assistant', content: '⚠️ Sorry, I encountered an error. Please try again.', timestamp: new Date().toISOString() });
      });
  },
});

export const { addMessage, setTyping, setSuggestions, clearChat, clearError } = chatSlice.actions;
export default chatSlice.reducer;
