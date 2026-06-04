export function ChatInput({ query, isLoading, canSend, onQueryChange, onSubmit }) {
  return (
    <form className="composer" onSubmit={onSubmit}>
      <input
        type="text"
        placeholder="Ask a question about your documents..."
        className="query-input"
        value={query}
        onChange={(e) => onQueryChange(e.target.value)}
        aria-label="Message input"
      />
      <button className="submit-button" type="submit" disabled={!canSend}>
        {isLoading ? 'Sending...' : 'Send'}
      </button>
    </form>
  )
}
