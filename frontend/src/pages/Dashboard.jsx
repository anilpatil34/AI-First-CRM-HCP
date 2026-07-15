import React from 'react';
import InteractionForm from '../components/InteractionForm/InteractionForm';
import ChatPanel from '../components/ChatPanel/ChatPanel';
import './Dashboard.css';

/**
 * Dashboard - Main page combining the interaction form, chat panel, and overview.
 */
function Dashboard() {
  return (
    <div className="dashboard">
      <div className="dashboard__left">
        <InteractionForm />
      </div>
      <div className="dashboard__right">
        <ChatPanel />
      </div>
    </div>
  );
}

export default Dashboard;
