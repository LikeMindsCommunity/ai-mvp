
import React from 'react';
import { ChatMessage as ChatMessageType } from '@/types';
import { cn } from '@/lib/utils';
import { Copy } from 'lucide-react';

// Simple markdown code block parser
const formatMessageContent = (content: string) => {
  const codeBlockRegex = /```([a-zA-Z]*)\n([\s\S]*?)```/g;
  const parts = [];
  let lastIndex = 0;
  let match;

  while ((match = codeBlockRegex.exec(content)) !== null) {
    // Add text before code block
    if (match.index > lastIndex) {
      parts.push({
        type: 'text',
        content: content.slice(lastIndex, match.index),
      });
    }

    // Add code block
    parts.push({
      type: 'code',
      language: match[1] || 'plaintext',
      content: match[2],
    });

    lastIndex = match.index + match[0].length;
  }

  // Add remaining text after last code block
  if (lastIndex < content.length) {
    parts.push({
      type: 'text',
      content: content.slice(lastIndex),
    });
  }

  return parts.length > 0 ? parts : [{ type: 'text', content }];
};

const CodeBlock = ({ language, content }: { language: string; content: string }) => {
  const copyToClipboard = () => {
    navigator.clipboard.writeText(content);
  };

  return (
    <div className="relative mt-2 mb-4 rounded-md overflow-hidden bg-muted/70">
      <div className="flex justify-between items-center px-4 py-1 bg-muted/90 text-xs font-mono text-muted-foreground">
        <span>{language || 'code'}</span>
        <button 
          onClick={copyToClipboard}
          className="p-1 hover:text-foreground transition-colors"
          aria-label="Copy code"
        >
          <Copy className="h-3.5 w-3.5" />
        </button>
      </div>
      <pre className="px-4 py-3 overflow-x-auto scrollbar-thin">
        <code className="text-sm font-mono">{content}</code>
      </pre>
    </div>
  );
};

interface ChatMessageProps {
  message: ChatMessageType;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === 'user';
  const formattedContent = formatMessageContent(message.content);
  
  return (
    <div
      className={cn(
        "flex w-full mb-4 animate-fade-in",
        isUser ? "justify-end" : "justify-start"
      )}
    >
      <div
        className={cn(
          "max-w-[85%] rounded-2xl px-4 py-2.5",
          isUser 
            ? "bg-primary text-primary-foreground" 
            : "bg-muted text-foreground"
        )}
      >
        {formattedContent.map((part, index) => (
          <React.Fragment key={index}>
            {part.type === 'text' ? (
              <p className="whitespace-pre-wrap text-balance">{part.content}</p>
            ) : (
              <CodeBlock language={part.language} content={part.content} />
            )}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
};

export const TypingIndicator = () => {
  return (
    <div className="flex mb-4">
      <div className="bg-muted rounded-2xl px-4 py-3.5 flex items-center space-x-1">
        <div className="w-1.5 h-1.5 rounded-full bg-muted-foreground/70 animate-typing-dot-1"></div>
        <div className="w-1.5 h-1.5 rounded-full bg-muted-foreground/70 animate-typing-dot-2"></div>
        <div className="w-1.5 h-1.5 rounded-full bg-muted-foreground/70 animate-typing-dot-3"></div>
      </div>
    </div>
  );
};
