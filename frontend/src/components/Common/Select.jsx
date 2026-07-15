import React from 'react';

/**
 * Select - Reusable dropdown select component.
 */
function Select({ label, id, value, onChange, options = [], placeholder, required = false, ...rest }) {
  return (
    <div className="select-group">
      {label && <label htmlFor={id} className="select-group__label">{label}</label>}
      <select
        className="select-group__field"
        id={id}
        value={value}
        onChange={onChange}
        required={required}
        {...rest}
      >
        {placeholder && <option value="">{placeholder}</option>}
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
    </div>
  );
}

export default Select;
