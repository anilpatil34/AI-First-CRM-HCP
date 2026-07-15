import React from 'react';

/**
 * Button - Reusable button component with variant support.
 */
function Button({ children, variant = 'primary', type = 'button', onClick, disabled = false, ...rest }) {
  return (
    <button
      className={`btn btn--${variant}`}
      type={type}
      onClick={onClick}
      disabled={disabled}
      {...rest}
    >
      {children}
    </button>
  );
}

export default Button;
