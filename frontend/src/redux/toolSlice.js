import { createSlice } from '@reduxjs/toolkit';

const toolSlice = createSlice({
  name: 'tool',
  initialState: { activeTool: null, toolResult: null, toolHistory: [], isExecuting: false },
  reducers: {
    setActiveTool: (s, a) => { s.activeTool = a.payload; s.isExecuting = !!a.payload; },
    setToolResult: (s, a) => { s.toolResult = a.payload; s.isExecuting = false; },
    addToHistory: (s, a) => { s.toolHistory.unshift({ ...a.payload, timestamp: new Date().toISOString() }); if (s.toolHistory.length > 20) s.toolHistory.pop(); },
    clearTool: (s) => { s.activeTool = null; s.toolResult = null; s.isExecuting = false; },
  },
});

export const { setActiveTool, setToolResult, addToHistory, clearTool } = toolSlice.actions;
export default toolSlice.reducer;
