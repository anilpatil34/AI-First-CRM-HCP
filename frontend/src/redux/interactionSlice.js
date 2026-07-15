import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { FORM_INITIAL_STATE } from '../utils/constants';
import * as interactionAPI from '../services/interactionAPI';

export const createInteractionThunk = createAsyncThunk('interaction/create', async (data, { rejectWithValue }) => {
  try { return await interactionAPI.createInteraction(data); } catch (e) { return rejectWithValue(e.response?.data?.detail || 'Failed to create interaction'); }
});
export const fetchInteractions = createAsyncThunk('interaction/fetchAll', async ({ skip = 0, limit = 20 } = {}, { rejectWithValue }) => {
  try { return await interactionAPI.getAllInteractions(skip, limit); } catch (e) { return rejectWithValue(e.response?.data?.detail || 'Failed to fetch interactions'); }
});
export const updateInteractionThunk = createAsyncThunk('interaction/update', async ({ id, data }, { rejectWithValue }) => {
  try { return await interactionAPI.updateInteraction(id, data); } catch (e) { return rejectWithValue(e.response?.data?.detail || 'Failed to update interaction'); }
});

const interactionSlice = createSlice({
  name: 'interaction',
  initialState: {
    currentInteraction: { ...FORM_INITIAL_STATE },
    interactions: [],
    selectedInteraction: null,
    loading: false,
    error: null,
    saveStatus: 'idle',
  },
  reducers: {
    setField: (state, action) => { const { field, value } = action.payload; state.currentInteraction[field] = value; },
    setMultipleFields: (state, action) => { Object.entries(action.payload).forEach(([k, v]) => { if (k in state.currentInteraction) state.currentInteraction[k] = v; }); },
    resetForm: (state) => { state.currentInteraction = { ...FORM_INITIAL_STATE }; state.saveStatus = 'idle'; state.error = null; },
    setSelectedInteraction: (state, action) => { state.selectedInteraction = action.payload; },
    clearError: (state) => { state.error = null; },
    setSaveStatus: (state, action) => { state.saveStatus = action.payload; },
  },
  extraReducers: (builder) => {
    builder
      .addCase(createInteractionThunk.pending, (s) => { s.loading = true; s.saveStatus = 'saving'; s.error = null; })
      .addCase(createInteractionThunk.fulfilled, (s, a) => { s.loading = false; s.saveStatus = 'saved'; s.interactions.unshift(a.payload); })
      .addCase(createInteractionThunk.rejected, (s, a) => { s.loading = false; s.saveStatus = 'error'; s.error = a.payload; })
      .addCase(fetchInteractions.pending, (s) => { s.loading = true; })
      .addCase(fetchInteractions.fulfilled, (s, a) => { s.loading = false; s.interactions = a.payload.items || []; })
      .addCase(fetchInteractions.rejected, (s, a) => { s.loading = false; s.error = a.payload; })
      .addCase(updateInteractionThunk.fulfilled, (s, a) => { const idx = s.interactions.findIndex(i => i.id === a.payload.id); if (idx !== -1) s.interactions[idx] = a.payload; });
  },
});

export const { setField, setMultipleFields, resetForm, setSelectedInteraction, clearError, setSaveStatus } = interactionSlice.actions;
export default interactionSlice.reducer;
