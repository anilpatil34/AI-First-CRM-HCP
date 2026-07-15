import { useSelector, useDispatch } from 'react-redux';
import { sendChatMessage, clearChat, setSuggestions } from '../redux/chatSlice';
import { useCallback } from 'react';

export function useChat() {
  const dispatch = useDispatch();
  const { messages, isTyping, suggestions, sessionId, error } = useSelector(s => s.chat);

  const sendMessage = useCallback((text) => {
    if (text?.trim()) dispatch(sendChatMessage(text.trim()));
  }, [dispatch]);

  return {
    messages, isTyping, suggestions, sessionId, error,
    sendMessage,
    clearChat: () => dispatch(clearChat()),
    clearSuggestions: () => dispatch(setSuggestions([])),
  };
}
