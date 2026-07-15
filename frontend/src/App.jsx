import React from 'react';
import './App.css';
import { Provider } from 'react-redux';
import store from './redux/store';
import Header from './components/Header/Header';
import InteractionForm from './components/InteractionForm/InteractionForm';
import ChatPanel from './components/ChatPanel/ChatPanel';
import ToolStatus from './components/ToolStatus/ToolStatus';
import InteractionHistory from './components/InteractionHistory/InteractionHistory';
import Toast from './components/Notification/Toast';

export default function App() {
  return (
    <Provider store={store}>
      <div className="app">
        <Header />
        <main className="app__main">
          <section className="app__left-panel">
            <InteractionForm />
          </section>
          <section className="app__right-panel">
            <ChatPanel />
            <div className="app__sidebar-widgets">
              <ToolStatus />
              <InteractionHistory />
            </div>
          </section>
        </main>
        <Toast />
      </div>
    </Provider>
  );
}
