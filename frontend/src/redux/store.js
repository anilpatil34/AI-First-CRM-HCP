import { configureStore } from '@reduxjs/toolkit';
import interactionReducer from './interactionSlice';
import chatReducer from './chatSlice';
import toolReducer from './toolSlice';
import uiReducer from './uiSlice';

const store = configureStore({
  reducer: {
    interaction: interactionReducer,
    chat: chatReducer,
    tool: toolReducer,
    ui: uiReducer,
  },
  middleware: (getDefaultMiddleware) => getDefaultMiddleware({ serializableCheck: false }),
});

export default store;
