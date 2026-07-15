import React from 'react';
import './ToolStatus.css';
import { useToolStatus } from '../../hooks/useToolStatus';
import { TOOL_LABELS } from '../../utils/constants';
import { FiActivity } from 'react-icons/fi';

export default function ToolStatus() {
  const { activeTool, isExecuting, toolHistory } = useToolStatus();

  return (
    <div className="tool-status">
      <div className="tool-status__header">
        <FiActivity className="tool-status__icon" />
        <h3 className="tool-status__title">AI Tools</h3>
        {isExecuting && <span className="tool-status__live">LIVE</span>}
      </div>

      {isExecuting && activeTool && (
        <div className="tool-status__active animate-pulse">
          <span className="tool-status__dot" />
          {TOOL_LABELS[activeTool] || `Running: ${activeTool}`}
        </div>
      )}

      {toolHistory.length > 0 && (
        <div className="tool-status__history">
          {toolHistory.slice(0, 5).map((tc, i) => (
            <div key={i} className="tool-history-item">
              <span className="tool-history-item__name">{tc.tool_name?.replace(/_/g, ' ')}</span>
              <span className="tool-history-item__result">{typeof tc.result === 'string' ? tc.result.substring(0, 40) : '✓'}</span>
            </div>
          ))}
        </div>
      )}

      {!isExecuting && toolHistory.length === 0 && (
        <p className="tool-status__empty">No tools executed yet. Start chatting to see AI tools in action.</p>
      )}
    </div>
  );
}
