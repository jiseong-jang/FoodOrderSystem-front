import axios, { AxiosInstance } from 'axios'
import { ChatRequest, ChatResponse, ChatMessage, OrderConfirmRequest, OrderConfirmResponse } from '../types'

// FastAPI 서비스는 별도의 baseURL 사용
const voiceApiClient: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_VOICE_API_URL || 'http://localhost:5001',
  headers: {
    'Content-Type': 'application/json',
  },
})

export const voiceOrderApi = {
  // 서버 상태 확인
  checkHealth: async (): Promise<{ status: string }> => {
    const response = await voiceApiClient.get('/health')
    return response.data
  },

  // STT: 음성 파일을 텍스트로 변환
  transcribeAudio: async (audioBlob: Blob, language?: string): Promise<string> => {
    const formData = new FormData()
    formData.append('file', audioBlob, 'audio.webm')
    
    const params: any = {}
    if (language) {
      params.language = language
    }
    
    const response = await voiceApiClient.post('/api/stt/transcribe', formData, {
      params,
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data.transcript || response.data.text || ''
  },

  // LLM: 주문 대화 생성
  generateChat: async (messages: ChatRequest['messages']): Promise<ChatResponse> => {
    const response = await voiceApiClient.post<ChatResponse>('/api/llm/generate', {
      messages,
    })
    return response.data
  },

  // 주문 확정 및 OrderSummary 반환
  confirmOrder: async (history: ChatMessage[], finalMessage?: string): Promise<OrderConfirmResponse> => {
    const response = await voiceApiClient.post<OrderConfirmResponse>('/api/order/confirm', {
      history,
      finalMessage,
    } as OrderConfirmRequest)
    return response.data
  },

  // 초기 인사 메시지 가져오기
  getGreeting: async (lang: string = 'ko-KR', name: string = '고객님'): Promise<string> => {
    const response = await voiceApiClient.get('/config/greeting', {
      params: { lang, name },
    })
    return response.data.greeting || '안녕하세요!'
  },
}

