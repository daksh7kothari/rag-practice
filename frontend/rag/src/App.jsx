import './App.css'
import { useChat } from './hooks/useChat'
import { ChatHeader, MessageList, ChatInput } from './components'

function App() {
  const { messages, query, isLoading, canSend, endOfMessagesRef, setQuery, handleSubmit } =
    useChat()

  return (
    <main className="chat-screen">
      <section className="chat-box" aria-label="Chat">
        <ChatHeader />
        <MessageList messages={messages} isLoading={isLoading} endOfMessagesRef={endOfMessagesRef} />
        <ChatInput
          query={query}
          isLoading={isLoading}
          canSend={canSend}
          onQueryChange={setQuery}
          onSubmit={handleSubmit}
        />
      </section>
    </main>
  )
}

export default App
