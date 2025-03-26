import * as React from "react"

const Button = React.forwardRef(({ className, disabled, children, type = "button", ...props }, ref) => {
    return (
        <button
            ref={ref}
            type={type}
            disabled={disabled}
            className={`
        inline-flex items-center justify-center rounded-md text-sm font-medium
        transition-colors focus-visible:outline-none focus-visible:ring-2
        focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50
        disabled:pointer-events-none ring-offset-background
        bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-700 hover:to-indigo-700
        text-white hover:text-white 
        transition-all transform hover:-translate-y-1 hover:shadow-lg px-4 py-2
        ${className || ''}
      `}
            {...props}
        >
            {children}
        </button>
    )
})

Button.displayName = "Button"

export { Button } 