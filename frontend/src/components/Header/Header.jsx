import React from 'react';
import './Header.css';
import { FiBell, FiUser, FiCpu } from 'react-icons/fi';

export default function Header() {
  return (
    <header className="header">
      <div className="header__left">
        <div className="header__logo">
          <FiCpu className="header__logo-icon" />
          <div>
            <h1 className="header__title">AI-First CRM</h1>
            <span className="header__subtitle">HCP Interaction Management</span>
          </div>
        </div>
      </div>
      <div className="header__right">
        <button className="header__icon-btn" aria-label="Notifications"><FiBell /></button>
        <div className="header__avatar"><FiUser /></div>
      </div>
    </header>
  );
}
