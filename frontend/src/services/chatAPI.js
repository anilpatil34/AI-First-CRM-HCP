import api from './api';
import { API_ENDPOINTS } from '../utils/constants';

export const sendMessage = (message, sessionId) =>
  api.post(API_ENDPOINTS.CHAT, { message, session_id: sessionId }).then(r => r.data);
