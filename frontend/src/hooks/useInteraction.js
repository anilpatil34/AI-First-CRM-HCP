import { useSelector, useDispatch } from 'react-redux';
import { setField, setMultipleFields, resetForm, createInteractionThunk, fetchInteractions } from '../redux/interactionSlice';
import { useCallback } from 'react';

export function useInteraction() {
  const dispatch = useDispatch();
  const { currentInteraction, interactions, loading, error, saveStatus } = useSelector(s => s.interaction);

  return {
    currentInteraction, interactions, loading, error, saveStatus,
    updateField: useCallback((field, value) => dispatch(setField({ field, value })), [dispatch]),
    updateMultipleFields: useCallback((fields) => dispatch(setMultipleFields(fields)), [dispatch]),
    resetForm: useCallback(() => dispatch(resetForm()), [dispatch]),
    submitInteraction: useCallback(() => dispatch(createInteractionThunk(currentInteraction)), [dispatch, currentInteraction]),
    loadInteractions: useCallback(() => dispatch(fetchInteractions()), [dispatch]),
  };
}
