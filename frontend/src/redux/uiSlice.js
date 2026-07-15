import { createSlice } from '@reduxjs/toolkit';

let toastId = 0;

const uiSlice = createSlice({
  name: 'ui',
  initialState: { toasts: [], sidebarOpen: true, theme: 'light', isFormHighlighted: false, highlightedFields: [] },
  reducers: {
    addToast: (s, a) => {
      const toast = { id: ++toastId, type: 'info', duration: 4000, ...a.payload };
      s.toasts.push(toast);
    },
    removeToast: (s, a) => { s.toasts = s.toasts.filter(t => t.id !== a.payload); },
    toggleSidebar: (s) => { s.sidebarOpen = !s.sidebarOpen; },
    setTheme: (s, a) => { s.theme = a.payload; },
    setFormHighlighted: (s, a) => { s.isFormHighlighted = a.payload; },
    setHighlightedFields: (s, a) => { s.highlightedFields = a.payload; s.isFormHighlighted = a.payload.length > 0; },
  },
});

export const { addToast, removeToast, toggleSidebar, setTheme, setFormHighlighted, setHighlightedFields } = uiSlice.actions;
export default uiSlice.reducer;
