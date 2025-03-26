import * as React from "react"

const Textarea = React.forwardRef(({ className, ...props }, ref) => {
    return (
        <textarea
            className={`
                flex min-h-20 w-full rounded-md border border-slate-200 
                dark:border-slate-800 bg-transparent px-3 py-2 
                text-sm ring-offset-background placeholder:text-slate-500 
                focus-visible:outline-none focus-visible:ring-2 
                focus-visible:ring-violet-500 focus-visible:ring-offset-2 
                disabled:cursor-not-allowed disabled:opacity-50
                shadow-sm
                ${className || ''}
            `}
            ref={ref}
            {...props}
        />
    )
})
Textarea.displayName = "Textarea"

export { Textarea } 