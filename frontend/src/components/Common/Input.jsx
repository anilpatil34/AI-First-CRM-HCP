import React from 'react';

/**
 * Input - Reusable text input component with label support.
 */
function Input({ label, id, type = 'text', value, onChange, placeholder, required = false, ...rest }) {
  return (
    <div className="input-group">
      {label && <label htmlFor={id} className="input-group__label">{label}</label>}
      <input
        className="input-group__field"
        id={id}
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        {...rest}
      />
    </div>
  );
}

export default Input;
