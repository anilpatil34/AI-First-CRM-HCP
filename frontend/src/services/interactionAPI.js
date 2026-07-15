import api from './api';
import { API_ENDPOINTS } from '../utils/constants';

export const createInteraction = (data) => api.post(API_ENDPOINTS.INTERACTION, data).then(r => r.data);
export const getInteraction = (id) => api.get(`${API_ENDPOINTS.INTERACTION}/${id}`).then(r => r.data);
export const updateInteraction = (id, data) => api.put(`${API_ENDPOINTS.INTERACTION}/${id}`, data).then(r => r.data);
export const deleteInteraction = (id) => api.delete(`${API_ENDPOINTS.INTERACTION}/${id}`).then(r => r.data);
export const getAllInteractions = (skip = 0, limit = 20) => api.get(API_ENDPOINTS.INTERACTIONS, { params: { skip, limit } }).then(r => r.data);
export const getInteractionHistory = (doctorName) => api.get(`${API_ENDPOINTS.HISTORY}/${doctorName}`).then(r => r.data);
