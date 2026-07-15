import React from 'react'; import './Loader.css';
export function Spinner({ size = 20 }) {
  return <div className="spinner" style={{ width: size, height: size }} />;
}
export function SkeletonLine({ width = '100%', height = 16 }) {
  return <div className="skeleton-line animate-shimmer" style={{ width, height, borderRadius: 'var(--radius-sm)' }} />;
}
export default function Loader({ text = 'Loading...' }) {
  return <div className="loader"><Spinner size={24} /><span className="loader__text">{text}</span></div>;
}
