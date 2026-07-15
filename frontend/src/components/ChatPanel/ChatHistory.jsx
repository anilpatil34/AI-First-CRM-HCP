import React from 'react';
import Message from './Message';

/**
 * ChatHistory - Scrollable list of chat messages.
 */
function ChatHistory() {
  const messages = []; // TODO: Pull from Redux chat slice

  return (
    <div className="chat-history">
      {messages.length === 0 ? (
        <p className="chat-history__empty">No messages yet. Start a conversation!</p>
      ) : (
        messages.map((msg, index) => (
          <Message key={index} message={msg} />
        ))
      )}
    </div>
  );
}

export default ChatHistory;
