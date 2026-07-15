import React, { useState, useRef, useEffect } from 'react';
import './ChatPanel.css';
import { useChat } from '../../hooks/useChat';
import { useToolStatus } from '../../hooks/useToolStatus';
import { TOOL_LABELS } from '../../utils/constants';
import { FiSend, FiTrash2, FiCpu, FiUser } from 'react-icons/fi';

function TypingIndicator() {
  return (
    <div className="message message--ai">
      <div className="message__avatar message__avatar--ai"><FiCpu /></div>
      <div className="message__bubble message__bubble--ai">
        <div className="typing-indicator">
          <span className="typing-dot" />
          <span className="typing-dot" />
          <span className="typing-dot" />
        </div>
      </div>
    </div>
  );
}

function ToolBadge({ toolCalls }) {
  if (!toolCalls?.length) return null;
  return (
    <div className="tool-badges">
      {toolCalls.map((tc, i) => (
        <span key={i} className="tool-badge">{TOOL_LABELS[tc.tool_name] || `🔧 ${tc.tool_name}`}</span>
      ))}
    </div>
  );
}

function ChatMessage({ message }) {
  const isUser = message.role === 'user';
  return (
    <div className={`message message--${isUser ? 'user' : 'ai'}`}>
      <div className={`message__avatar message__avatar--${isUser ? 'user' : 'ai'}`}>
        {isUser ? <FiUser /> : <FiCpu />}
      </div>
      <div className="message__content">
        <div className={`message__bubble message__bubble--${isUser ? 'user' : 'ai'}`}>
          <p className="message__text">{message.content}</p>
        </div>
        {!isUser && <ToolBadge toolCalls={message.toolCalls} />}
      </div>
    </div>
  );
}

function SuggestionChips({ suggestions, onSelect }) {
  if (!suggestions?.length) return null;
  return (
    <div className="suggestion-chips">
      <span className="suggestion-chips__label">💡 Suggested:</span>
      <div className="suggestion-chips__list">
        {suggestions.map((s, i) => (
          <button key={i} className="suggestion-chip" onClick={() => onSelect(s)}>{s}</button>
        ))}
      </div>
    </div>
  );
}

export default function ChatPanel() {
  const { messages, isTyping, suggestions, sendMessage, clearChat } = useChat();
  const { activeTool, isExecuting } = useToolStatus();
  const [input, setInput] = useState('');
  const messagesContainerRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    if (messagesContainerRef.current) {
      const container = messagesContainerRef.current;
      container.scrollTop = container.scrollHeight;
      
      // Delay slightly to allow layout calculations (e.g. suggestions container height changes) to complete
      const timer = setTimeout(() => {
        container.scrollTop = container.scrollHeight;
      }, 80);
      
      return () => clearTimeout(timer);
    }
  }, [messages, isTyping, suggestions]);

  const handleSend = () => {
    if (!input.trim() || isTyping) return;
    sendMessage(input.trim());
    setInput('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleSuggestionSelect = (text) => {
    sendMessage(text);
  };

  return (
    <div className="chat-panel">
      <div className="chat-panel__header">
        <div className="chat-panel__header-left">
          <FiCpu className="chat-panel__header-icon" />
          <div>
            <h2 className="chat-panel__title">AI Assistant</h2>
            <span className="chat-panel__status">
              {isExecuting ? `${TOOL_LABELS[activeTool] || 'Processing...'}` : isTyping ? 'Thinking...' : 'Online'}
            </span>
          </div>
        </div>
        <button className="chat-panel__clear-btn" onClick={clearChat} title="Clear chat"><FiTrash2 /></button>
      </div>

      <div ref={messagesContainerRef} className="chat-panel__messages">
        {messages.map((msg) => (
          <ChatMessage key={msg.id} message={msg} />
        ))}
        {isTyping && <TypingIndicator />}
      </div>

      <SuggestionChips suggestions={suggestions} onSelect={handleSuggestionSelect} />

      <div className="chat-panel__input-area">
        <textarea
          ref={inputRef}
          className="chat-panel__input"
          placeholder='Try: "Met Dr. Sharma today, discussed CardioX, positive response..."'
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={1}
          disabled={isTyping}
        />
        <button className="chat-panel__send-btn" onClick={handleSend} disabled={!input.trim() || isTyping} aria-label="Send message">
          <FiSend />
        </button>
      </div>
    </div>
  );
}
