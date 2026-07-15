import React from 'react';

/**
 * Message - Single chat message bubble (user or AI).
 */
function Message({ message }) {
  const { role = 'user', content = '' } = message || {};

  return (
    <div className={`message message--${role}`}>
      <div className="message__content">{content}</div>
    </div>
  );
}

export default Message;
