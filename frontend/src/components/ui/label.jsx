import * as React from "react"

const Label = React.forwardRef(({ className, htmlFor, children, ...props }, ref) => {
    return (
        <label
            ref={ref}
            htmlFor={htmlFor}
            className={`
        text-sm font-medium text-slate-700 dark:text-slate-300
        ${className || ''}
      `}
            {...props}
        >
            {children}
        </label>
    )
})

Label.displayName = "Label"

export { Label } 