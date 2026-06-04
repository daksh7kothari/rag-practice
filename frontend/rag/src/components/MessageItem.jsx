export function MessageItem({ message }) {
  return (
    <article className={`message ${message.role}`}>
      <div className="message-label">{message.role === 'user' ? 'You' : 'Assistant'}</div>
      <p>{message.content}</p>
    </article>
  )
}
