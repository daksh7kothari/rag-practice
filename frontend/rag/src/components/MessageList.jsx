import { MessageItem } from './MessageItem'
import { LoadingMessage } from './LoadingMessage'

export function MessageList({ messages, isLoading, endOfMessagesRef }) {
  return (
    <div className="messages" aria-live="polite">
      {messages.map((message) => (
        <MessageItem key={message.id} message={message} />
      ))}
      {isLoading && <LoadingMessage />}
      <div ref={endOfMessagesRef} />
    </div>
  )
}
