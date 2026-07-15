/**
 * Application constants.
 * Centralized configuration for the CRM frontend.
 */

export const INTERACTION_TYPES = ['Meeting', 'Call', 'Email', 'Conference', 'Other'];

export const SENTIMENT_VALUES = ['Positive', 'Neutral', 'Negative'];

export const SENTIMENT_EMOJIS = {
  Positive: '😊',
  Neutral: '😐',
  Negative: '😟',
};

export const SENTIMENT_COLORS = {
  Positive: 'var(--color-sentiment-positive)',
  Neutral: 'var(--color-sentiment-neutral)',
  Negative: 'var(--color-sentiment-negative)',
};

export const API_ENDPOINTS = {
  CHAT: '/api/v1/chat',
  INTERACTION: '/api/v1/interaction',
  INTERACTIONS: '/api/v1/interactions',
  DOCTORS: '/api/v1/doctors',
  DOCTOR: '/api/v1/doctor',
  DOCTOR_SEARCH: '/api/v1/doctor/search',
  HISTORY: '/api/v1/history',
  HEALTH: '/api/v1/health',
};

export const FORM_INITIAL_STATE = {
  hcpName: '',
  interactionType: 'Meeting',
  date: '',
  time: '',
  attendees: [],
  topicsDiscussed: '',
  materialsShared: [],
  samplesDistributed: [],
  sentiment: 'Neutral',
  outcomes: '',
  followUpActions: '',
  summary: '',
  aiGenerated: false,
};

export const AI_WELCOME_MESSAGE = {
  id: 'welcome',
  role: 'assistant',
  content:
    'Log interaction details here (e.g., "Met Dr. Smith, discussed Product X efficacy, positive sentiment, shared brochure") or ask for help.',
  timestamp: new Date().toISOString(),
};

export const MAX_CHAT_HISTORY = 50;

export const TOOL_LABELS = {
  log_interaction: '📝 Extracting interaction data...',
  edit_interaction: '✏️ Updating field...',
  summarize_interaction: '📋 Generating summary...',
  suggest_followup: '💡 Suggesting follow-ups...',
  doctor_lookup: '🔍 Looking up doctor...',
};
