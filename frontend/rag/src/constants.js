const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''
export const API_QUERY_URL = `${API_BASE_URL.replace(/\/$/, '')}/api/query`

export const SEED_MESSAGES = [
  {
    id: 1,
    role: 'assistant',
    content: 'Hi, I\'m the SRM Team Robocon Assistant. Ask me anything about the RECRUITMENT\'26 !',
    
  },
]
