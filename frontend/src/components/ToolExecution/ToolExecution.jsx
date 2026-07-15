import React from 'react';
import './ToolExecution.css';

/**
 * ToolExecution - Displays the status and results of AI tool executions.
 */
function ToolExecution({ tool }) {
  const { name = 'Unknown Tool', status = 'idle', result = null } = tool || {};

  return (
    <div className={`tool-execution tool-execution--${status}`}>
      <div className="tool-execution__header">
        <span className="tool-execution__name">{name}</span>
        <span className="tool-execution__status">{status}</span>
      </div>
      {result && (
        <div className="tool-execution__result">
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default ToolExecution;
