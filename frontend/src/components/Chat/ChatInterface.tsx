import React, { useRef } from "react"
import { ChatMessage, TypingIndicator } from "./ChatMessage"
import { Button } from "@/components/ui/button"
import { Send, X } from "lucide-react"

interface ChatInterfaceProps {
  messages: any[]
  isTyping: boolean
  inputValue: string
  messagesEndRef: React.RefObject<HTMLDivElement>
  onInputChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void
  onSubmit: (e: React.FormEvent) => void
  onCancel: () => void
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({
  messages,
  isTyping,
  inputValue,
  messagesEndRef,
  onInputChange,
  onSubmit,
  onCancel,
}) => {
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  // Auto-resize textarea as user types
  const handleTextareaInput = () => {
    const textarea = textareaRef.current
    if (textarea) {
      textarea.style.height = "auto"
      textarea.style.height = Math.min(textarea.scrollHeight, 200) + "px"
    }
  }

  // Handle keyboard shortcuts
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      onSubmit(e as unknown as React.FormEvent)
    }
  }

  return (
    <div className="flex flex-col h-full overflow-hidden rounded-2xl glass-panel">
      <div className="p-4 border-b border-border/50">
        <h2 className="text-lg font-medium">Chat</h2>
      </div>

      <div className="flex-1 overflow-y-auto p-4 scrollbar-thin">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-muted-foreground p-4 text-center">
            <p className="mb-2 text-lg">How can I help you build today?</p>
            <p className="text-sm max-w-md">
              Describe what you'd like to create, and I'll generate the code in
              real-time.
            </p>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}
            {isTyping && <TypingIndicator />}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>
      {/*  absolute bottom-[10px] right-[10px] flex gap-2 */}
      <div className="p-4 border-t border-border/50">
        <form
          onSubmit={onSubmit}
          className="flex flex-row gap-2 items-center justify-between w-full rounded-lg border border-input bg-background p-4 "
        >
          <textarea
            ref={textareaRef}
            className="flex-1 bg-background resize-none min-h-[44px] max-h-[200px] pr-[90px]rounded-lg  focus:outline-none scrollbar-thin  "
            placeholder="Describe what you want to build..."
            value={inputValue}
            onChange={onInputChange}
            onInput={handleTextareaInput}
            onKeyDown={handleKeyDown}
            rows={1}
          />

          <div className="">
            {isTyping && (
              <Button
                type="button"
                variant="ghost"
                size="icon"
                onClick={onCancel}
                className="h-[30px] w-[30px]"
              >
                <X className="h-4 w-4" />
              </Button>
            )}
            <Button
              type="submit"
              variant="default"
              className="h-10 rounded-sm p-4 text-xs"
              disabled={!inputValue.trim()}
            >
              <Send className="h-3 w-3 mr-1" />
            </Button>
          </div>
        </form>
      </div>
    </div>
  )
}
