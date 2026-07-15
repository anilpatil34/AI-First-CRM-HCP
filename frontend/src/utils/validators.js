/**
 * Form validation utilities.
 */

export function validateRequired(value, fieldName) {
  if (!value || (typeof value === 'string' && !value.trim())) {
    return `${fieldName} is required`;
  }
  return null;
}

export function validateEmail(email) {
  if (!email) return null;
  const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return pattern.test(email) ? null : 'Invalid email format';
}

export function validateDate(dateStr) {
  if (!dateStr) return null;
  const pattern = /^\d{4}-\d{2}-\d{2}$/;
  if (!pattern.test(dateStr)) return 'Date must be in YYYY-MM-DD format';
  const d = new Date(dateStr);
  return isNaN(d.getTime()) ? 'Invalid date' : null;
}

export function validateChatMessage(message) {
  if (!message || !message.trim()) return 'Message cannot be empty';
  if (message.length > 5000) return 'Message is too long (max 5000 characters)';
  return null;
}

export function validateInteractionForm(formData) {
  const errors = {};
  const nameErr = validateRequired(formData.hcpName, 'HCP Name');
  if (nameErr) errors.hcpName = nameErr;
  if (formData.date) {
    const dateErr = validateDate(formData.date);
    if (dateErr) errors.date = dateErr;
  }
  return { isValid: Object.keys(errors).length === 0, errors };
}
