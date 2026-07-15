import React, { useEffect } from 'react';
import './InteractionHistory.css';
import { useInteraction } from '../../hooks/useInteraction';
import { SENTIMENT_EMOJIS } from '../../utils/constants';
import { formatRelativeTime, truncateText } from '../../utils/helpers';
import { FiClock, FiChevronRight } from 'react-icons/fi';

export default function InteractionHistory() {
  const { interactions, loading, loadInteractions } = useInteraction();

  useEffect(() => { loadInteractions(); }, [loadInteractions]);

  return (
    <div className="interaction-history">
      <div className="interaction-history__header">
        <FiClock className="interaction-history__icon" />
        <h3 className="interaction-history__title">Recent Interactions</h3>
        <span className="interaction-history__count">{interactions.length}</span>
      </div>

      {loading && <p className="interaction-history__loading">Loading...</p>}

      <div className="interaction-history__list">
        {interactions.length === 0 && !loading && (
          <p className="interaction-history__empty">No interactions yet. Use the AI chat to log your first one!</p>
        )}
        {interactions.slice(0, 8).map((item) => (
          <div key={item.id} className="history-item">
            <div className="history-item__top">
              <span className="history-item__doctor">{item.doctor_name || 'Unknown'}</span>
              <span className="history-item__sentiment">{SENTIMENT_EMOJIS[item.sentiment] || '😐'}</span>
            </div>
            <div className="history-item__meta">
              <span className="history-item__type">{item.interaction_type}</span>
              <span className="history-item__date">{item.date || formatRelativeTime(item.created_at)}</span>
            </div>
            {item.summary && <p className="history-item__summary">{truncateText(item.summary, 80)}</p>}
          </div>
        ))}
      </div>
    </div>
  );
}
