import React from 'react';
import './InteractionForm.css';
import { useInteraction } from '../../hooks/useInteraction';
import { useSelector } from 'react-redux';
import { INTERACTION_TYPES, SENTIMENT_VALUES, SENTIMENT_EMOJIS } from '../../utils/constants';
import { getCurrentDate, getCurrentTime } from '../../utils/helpers';
import { FiSave, FiRefreshCw, FiCalendar, FiClock, FiUser, FiMessageSquare, FiTarget, FiPackage, FiFileText, FiTrendingUp } from 'react-icons/fi';

export default function InteractionForm() {
  const { currentInteraction, loading, saveStatus, updateField, resetForm, submitInteraction } = useInteraction();
  const highlightedFields = useSelector(s => s.ui.highlightedFields);

  const isHighlighted = (field) => highlightedFields.includes(field);
  const cl = (field) => isHighlighted(field) ? 'form-group field-highlighted' : 'form-group';

  const handleSubmit = (e) => {
    e.preventDefault();
    submitInteraction();
  };

  return (
    <form className="interaction-form" onSubmit={handleSubmit}>
      <div className="form-header">
        <h2 className="form-header__title"><FiFileText /> Interaction Form</h2>
        <div className="form-header__actions">
          <button type="button" className="btn btn--ghost" onClick={resetForm} title="Reset form"><FiRefreshCw /> Reset</button>
          <button type="submit" className={`btn btn--primary ${saveStatus === 'saving' ? 'btn--loading' : ''}`} disabled={loading}>
            <FiSave /> {saveStatus === 'saving' ? 'Saving...' : saveStatus === 'saved' ? 'Saved ✓' : 'Save'}
          </button>
        </div>
      </div>

      {currentInteraction.aiGenerated && (
        <div className="form-ai-badge"><span className="ai-badge">✨ AI Auto-filled</span> Review and edit if needed</div>
      )}

      <div className="form-grid">
        {/* HCP Name */}
        <div className={cl('hcpName')}>
          <label className="form-label"><FiUser /> HCP / Doctor Name</label>
          <input className="form-input" type="text" placeholder="e.g. Dr. Rajesh Sharma" value={currentInteraction.hcpName} onChange={e => updateField('hcpName', e.target.value)} />
        </div>

        {/* Interaction Type */}
        <div className={cl('interactionType')}>
          <label className="form-label"><FiMessageSquare /> Interaction Type</label>
          <select className="form-select" value={currentInteraction.interactionType} onChange={e => updateField('interactionType', e.target.value)}>
            {INTERACTION_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
          </select>
        </div>

        {/* Date */}
        <div className={cl('date')}>
          <label className="form-label"><FiCalendar /> Date</label>
          <div className="form-input-group">
            <input className="form-input" type="date" value={currentInteraction.date} onChange={e => updateField('date', e.target.value)} />
            <button type="button" className="btn-inline" onClick={() => updateField('date', getCurrentDate())}>Today</button>
          </div>
        </div>

        {/* Time */}
        <div className={cl('time')}>
          <label className="form-label"><FiClock /> Time</label>
          <div className="form-input-group">
            <input className="form-input" type="time" value={currentInteraction.time} onChange={e => updateField('time', e.target.value)} />
            <button type="button" className="btn-inline" onClick={() => updateField('time', getCurrentTime())}>Now</button>
          </div>
        </div>

        {/* Sentiment */}
        <div className={`${cl('sentiment')} form-group--full`}>
          <label className="form-label"><FiTrendingUp /> Sentiment</label>
          <div className="sentiment-selector">
            {SENTIMENT_VALUES.map(s => (
              <button key={s} type="button" className={`sentiment-btn sentiment-btn--${s.toLowerCase()} ${currentInteraction.sentiment === s ? 'sentiment-btn--active' : ''}`} onClick={() => updateField('sentiment', s)}>
                {SENTIMENT_EMOJIS[s]} {s}
              </button>
            ))}
          </div>
        </div>

        {/* Topics */}
        <div className={`${cl('topicsDiscussed')} form-group--full`}>
          <label className="form-label"><FiTarget /> Topics Discussed</label>
          <textarea className="form-textarea" rows={3} placeholder="Key topics, products discussed, doctor's feedback..." value={currentInteraction.topicsDiscussed} onChange={e => updateField('topicsDiscussed', e.target.value)} />
        </div>

        {/* Outcomes */}
        <div className={`${cl('outcomes')} form-group--full`}>
          <label className="form-label">📋 Outcomes</label>
          <textarea className="form-textarea" rows={2} placeholder="Key outcomes, agreements, decisions..." value={currentInteraction.outcomes} onChange={e => updateField('outcomes', e.target.value)} />
        </div>

        {/* Follow-up */}
        <div className={`${cl('followUpActions')} form-group--full`}>
          <label className="form-label">📌 Follow-up Actions</label>
          <textarea className="form-textarea" rows={2} placeholder="Next steps, action items..." value={currentInteraction.followUpActions} onChange={e => updateField('followUpActions', e.target.value)} />
        </div>

        {/* Summary */}
        <div className={`${cl('summary')} form-group--full`}>
          <label className="form-label">📝 Summary</label>
          <textarea className="form-textarea" rows={4} placeholder="AI-generated or manual summary of the interaction..." value={currentInteraction.summary} onChange={e => updateField('summary', e.target.value)} />
        </div>

        {/* Materials */}
        <div className={cl('materialsShared')}>
          <label className="form-label"><FiPackage /> Materials Shared</label>
          <input className="form-input" type="text" placeholder="Comma-separated materials" value={Array.isArray(currentInteraction.materialsShared) ? currentInteraction.materialsShared.join(', ') : currentInteraction.materialsShared} onChange={e => updateField('materialsShared', e.target.value.split(',').map(s => s.trim()).filter(Boolean))} />
        </div>

        {/* Samples */}
        <div className={cl('samplesDistributed')}>
          <label className="form-label"><FiPackage /> Samples Distributed</label>
          <input className="form-input" type="text" placeholder="Comma-separated samples" value={Array.isArray(currentInteraction.samplesDistributed) ? currentInteraction.samplesDistributed.join(', ') : currentInteraction.samplesDistributed} onChange={e => updateField('samplesDistributed', e.target.value.split(',').map(s => s.trim()).filter(Boolean))} />
        </div>
      </div>
    </form>
  );
}
