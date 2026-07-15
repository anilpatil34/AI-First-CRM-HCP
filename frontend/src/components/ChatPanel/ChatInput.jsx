import React, { useState } from 'react';

/**
 * ChatInput - Text input and send button for the AI chat.
 */
function ChatInput() {
  const [message, setMessage] = useState('');

  const handleSend = () => {
    if (!message.trim()) return;
    // TODO: Dispatch message to chat slice
    setMessage('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-input">
      <textarea
        className="chat-input__field"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask the AI assistant..."
        rows={2}
      />
      <button className="chat-input__send" onClick={handleSend}>
        Send
      </button>
    </div>
  );
}

export default ChatInput;
