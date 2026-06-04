import { useEffect, useMemo, useRef, useState } from 'react'
import { API_QUERY_URL, SEED_MESSAGES } from '../constants'

export function useChat() {
  const [messages, setMessages] = useState(SEED_MESSAGES)
  const [query, setQuery] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const endOfMessagesRef = useRef(null)

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  // Check if send button should be enabled
  const canSend = useMemo(() => query.trim().length > 0 && !isLoading, [query, isLoading])

  // Send message to API
  async function handleSubmit(event) {
    event?.preventDefault()
    if (!query.trim() || isLoading) return

    const userMessage = { id: Date.now(), role: 'user', content: query.trim() }
    const nextMessages = [...messages, userMessage]
    setMessages(nextMessages)
    setQuery('')
    setIsLoading(true)

    try {
      const res = await fetch(API_QUERY_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: userMessage.content }),
      })

      if (!res.ok) {
        const errorText = await res.text()
        throw new Error(`Backend responded with ${res.status}: ${errorText}`)
      }

      const data = await res.json()
      const answer =
        typeof data.answer === 'string' && data.answer.trim().length > 0
          ? data.answer
          : `Backend returned no answer. Check VITE_API_BASE_URL (${API_QUERY_URL}).`

      setMessages((current) => [
        ...current,
        {
          id: Date.now() + 1,
          role: 'assistant',
          content: answer,
        },
      ])
    } catch (error) {
      console.error('Error:', error)
      setMessages((current) => [
        ...current,
        {
          id: Date.now() + 1,
          role: 'assistant',
          content: `Something went wrong while contacting the backend. Check VITE_API_BASE_URL (${API_QUERY_URL}).`,
        },
      ])
    } finally {
      setIsLoading(false)
    }
  }

  return {
    messages,
    query,
    isLoading,
    canSend,
    endOfMessagesRef,
    setQuery,
    handleSubmit,
  }
}
