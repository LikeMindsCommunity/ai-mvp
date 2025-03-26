import * as React from "react"

const Switch = React.forwardRef(({ className, checked, onCheckedChange, disabled, ...props }, ref) => {
    // Handle click without triggering any side effects
    const handleToggle = React.useCallback((e) => {
        // Prevent default browser behavior
        e.preventDefault();
        e.stopPropagation();

        // Only call the change handler if it exists and component isn't disabled
        if (onCheckedChange && !disabled) {
            onCheckedChange(!checked);
        }
    }, [checked, disabled, onCheckedChange]);

    return (
        <button
            ref={ref}
            role="switch"
            type="button"
            aria-checked={checked}
            disabled={disabled}
            data-state={checked ? "checked" : "unchecked"}
            onClick={handleToggle}
            className={`
        relative inline-flex shrink-0 cursor-pointer rounded-full border-2 border-transparent 
        transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 
        focus:ring-violet-500 focus:ring-offset-2 h-6 w-11
        ${checked ? 'bg-violet-600' : 'bg-gray-200 dark:bg-gray-700'}
        ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
        ${className || ''}
      `}
            {...props}
        >
            <span
                aria-hidden="true"
                className={`
          pointer-events-none inline-block h-5 w-5 transform rounded-full 
          bg-white shadow ring-0 transition duration-200 ease-in-out
          ${checked ? 'translate-x-5' : 'translate-x-0'}
        `}
            />
        </button>
    )
})

Switch.displayName = "Switch"

export { Switch } 