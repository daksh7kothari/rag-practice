import { useEffect, useMemo, useRef, useState } from 'react'
import './App.css'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

const seedMessages = [
  {
    id: 1,
    role: 'assistant',
    content: 'Hi, I’m the SRM Team Robocon Assistant. Ask me anything about the REQRUITMENT\'26 !',
  },
]

function App() {
  const [messages, setMessages] = useState(seedMessages)
  const [query, setQuery] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const endOfMessagesRef = useRef(null)

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  const canSend = useMemo(() => query.trim().length > 0 && !isLoading, [query, isLoading])

  async function handleSubmit(event) {
    event?.preventDefault()
    if (!query.trim() || isLoading) return

    const userMessage = { id: Date.now(), role: 'user', content: query.trim() }
    const nextMessages = [...messages, userMessage]
    setMessages(nextMessages)
    setQuery('')
    setIsLoading(true)

    try {
      const res = await fetch(`${API_BASE_URL}/api/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: userMessage.content }),
      })

      const data = await res.json()
      setMessages((current) => [
        ...current,
        {
          id: Date.now() + 1,
          role: 'assistant',
          content: data.answer ?? 'No answer returned.',
        },
      ])
    } catch (error) {
      console.error('Error:', error)
      setMessages((current) => [
        ...current,
        {
          id: Date.now() + 1,
          role: 'assistant',
          content: 'Something went wrong while contacting the backend.',
        },
      ])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="chat-screen">
      <section className="chat-box" aria-label="Chat">
        <header className="chat-header">
          <div>
            <p className="chat-kicker">SRM TEAM ROBOCON Assistant</p>
            <h1>REQRUITMENT'26</h1>
          </div>
          {/* <p className="chat-status">{isLoading ? '' : ''}</p> */}
          <img src="/LOGO.png" alt="Assistant Avatar" className="avatar" height="80" width="80" />
        </header>

        <div className="messages" aria-live="polite">
          {messages.map((message) => (
            <article key={message.id} className={`message ${message.role}`}>
              <div className="message-label">{message.role === 'user' ? 'You' : 'Assistant'}</div>
              <p>{message.content}</p>
            </article>
          ))}
          {isLoading && (
            <article className="message assistant">
              <div className="message-label">Assistant</div>
              <p>Thinking...</p>
            </article>
          )}
          <div ref={endOfMessagesRef} />
        </div>

        <form className="composer" onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Ask a question about your documents..."
            className="query-input"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            aria-label="Message input"
          />
          <button className="submit-button" type="submit" disabled={!canSend}>
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </form>
      </section>
    </main>
  )
}

export default App
