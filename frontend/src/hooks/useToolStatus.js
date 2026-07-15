import { useSelector, useDispatch } from 'react-redux';
import { clearTool } from '../redux/toolSlice';

export function useToolStatus() {
  const dispatch = useDispatch();
  const { activeTool, isExecuting, toolResult, toolHistory } = useSelector(s => s.tool);
  return { activeTool, isExecuting, toolResult, toolHistory, clearTool: () => dispatch(clearTool()) };
}
