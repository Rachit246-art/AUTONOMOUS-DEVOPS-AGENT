
const API_BASE = (
  import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
).replace(/\/+$/, '');

const CHAT_ENDPOINT =
  import.meta.env.VITE_CHAT_ENDPOINT || '/api/incidents/';

const CONVERSATIONS_ENDPOINT =
  import.meta.env.VITE_CONVERSATIONS_ENDPOINT || '/api/conversations';

export const getChatUrl = () => {
  const endpoint = CHAT_ENDPOINT.startsWith('/')
    ? CHAT_ENDPOINT
    : `/${CHAT_ENDPOINT}`;

  return `${API_BASE}${endpoint}`;
};

export const getConversationsUrl = () => {
  return `${API_BASE}${CONVERSATIONS_ENDPOINT.startsWith('/')
    ? CONVERSATIONS_ENDPOINT
    : `/${CONVERSATIONS_ENDPOINT}`}`;
};

export const getDeleteConversationUrl = (id) => {
  return `${getConversationsUrl()}/${encodeURIComponent(id)}`;
};
