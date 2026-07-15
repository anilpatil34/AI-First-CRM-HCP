import React from 'react';

/**
 * TextArea - Reusable textarea component with label support.
 */
function TextArea({ label, id, value, onChange, placeholder, rows = 4, required = false, ...rest }) {
  return (
    <div className="textarea-group">
      {label && <label htmlFor={id} className="textarea-group__label">{label}</label>}
      <textarea
        className="textarea-group__field"
        id={id}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        rows={rows}
        required={required}
        {...rest}
      />
    </div>
  );
}

export default TextArea;
