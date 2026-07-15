import React from 'react'; import './Toast.css';
import { useSelector, useDispatch } from 'react-redux';
import { removeToast } from '../../redux/uiSlice';
import { FiCheckCircle, FiAlertTriangle, FiXCircle, FiInfo, FiX } from 'react-icons/fi';
import { useEffect } from 'react';

const ICONS = { success: <FiCheckCircle />, warning: <FiAlertTriangle />, error: <FiXCircle />, info: <FiInfo /> };

function ToastItem({ toast }) {
  const dispatch = useDispatch();
  useEffect(() => { const t = setTimeout(() => dispatch(removeToast(toast.id)), toast.duration || 4000); return () => clearTimeout(t); }, [toast, dispatch]);
  return (
    <div className={`toast toast--${toast.type}`}>
      <span className="toast__icon">{ICONS[toast.type] || ICONS.info}</span>
      <span className="toast__message">{toast.message}</span>
      <button className="toast__close" onClick={() => dispatch(removeToast(toast.id))}><FiX /></button>
      <div className="toast__progress" style={{ animationDuration: `${toast.duration || 4000}ms` }} />
    </div>
  );
}

export default function Toast() {
  const toasts = useSelector(s => s.ui.toasts);
  if (!toasts.length) return null;
  return <div className="toast-container">{toasts.map(t => <ToastItem key={t.id} toast={t} />)}</div>;
}
