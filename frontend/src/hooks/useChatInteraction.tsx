
import { useState, useEffect, useRef, useCallback } from 'react';
import { ChatMessage, CodeFile } from '@/types';

export function useChatInteraction() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'m your AI assistant. Tell me what you want to build, and I\'ll help you create it with code.',
      timestamp: new Date(Date.now() - 60000),
    }
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [codeFiles, setCodeFiles] = useState<CodeFile[]>([
    {
      id: '1',
      name: 'App.js',
      language: 'javascript',
      content: `import React, { useState } from 'react';

function Button({ children, onClick, variant = "primary" }) {
  const getButtonClasses = () => {
    const baseClasses = "px-4 py-2 rounded font-medium transition-colors";
    
    switch (variant) {
      case "primary":
        return \`\${baseClasses} bg-blue-500 text-white hover:bg-blue-600\`;
      case "secondary":
        return \`\${baseClasses} bg-gray-200 text-gray-800 hover:bg-gray-300\`;
      case "success":
        return \`\${baseClasses} bg-green-500 text-white hover:bg-green-600\`;
      case "danger":
        return \`\${baseClasses} bg-red-500 text-white hover:bg-red-600\`;
      default:
        return \`\${baseClasses} bg-blue-500 text-white hover:bg-blue-600\`;
    }
  };
  
  return (
    <button 
      className={getButtonClasses()}
      onClick={onClick}
    >
      {children}
    </button>
  );
}

function Card({ title, children }) {
  return (
    <div className="border border-gray-200 rounded-lg p-4 shadow-sm">
      {title && <h3 className="text-lg font-semibold mb-2">{title}</h3>}
      {children}
    </div>
  );
}

function App() {
  const [count, setCount] = useState(0);
  
  return (
    <div className="p-6 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-6">React Component Demo</h1>
      
      <div className="space-y-6">
        <Card title="Button Components">
          <div className="space-y-2">
            <div className="flex flex-wrap gap-2">
              <Button variant="primary">Primary</Button>
              <Button variant="secondary">Secondary</Button>
              <Button variant="success">Success</Button>
              <Button variant="danger">Danger</Button>
            </div>
          </div>
        </Card>
        
        <Card title="Counter Example">
          <div className="flex items-center justify-center space-x-4">
            <Button 
              variant="secondary" 
              onClick={() => setCount(count - 1)}
            >
              -
            </Button>
            <span className="text-xl font-semibold">{count}</span>
            <Button 
              variant="primary" 
              onClick={() => setCount(count + 1)}
            >
              +
            </Button>
          </div>
        </Card>
      </div>
    </div>
  );
}

export default App;`
    },
    {
      id: '2',
      name: 'styles.css',
      language: 'css',
      content: `/* Additional custom styles */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

body {
  font-family: 'Inter', sans-serif;
  background-color: #f9fafb;
  color: #111827;
}

/* Custom animations */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.animate-fadeIn {
  animation: fadeIn 0.3s ease-in-out;
}

/* Custom utility classes */
.hover-scale {
  transition: transform 0.2s ease;
}
.hover-scale:hover {
  transform: scale(1.05);
}
`
    },
    {
      id: '3',
      name: 'index.html',
      language: 'html',
      content: `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>React App</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div id="root"></div>
  <script src="index.js"></script>
</body>
</html>`
    }
  ]);
  
  const [activeFileId, setActiveFileId] = useState<string>('1');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when messages change
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  // Function to update file content
  const updateFileContent = useCallback((fileId: string, content: string) => {
    setCodeFiles(prev => 
      prev.map(file => 
        file.id === fileId ? { ...file, content } : file
      )
    );
  }, []);

  // Mock function to send a message
  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim()) return;
    
    // Create a new user message
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date(),
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(true);
    
    // Mock API delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Mock response with AI typing effect
    setTimeout(() => {
      const aiMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `I've created a component based on your request. Here's a React component with different button variants and a simple counter:

\`\`\`jsx
function Button({ children, onClick, variant = "primary" }) {
  const getButtonClasses = () => {
    const baseClasses = "px-4 py-2 rounded font-medium transition-colors";
    
    switch (variant) {
      case "primary":
        return \`\${baseClasses} bg-blue-500 text-white hover:bg-blue-600\`;
      case "secondary":
        return \`\${baseClasses} bg-gray-200 text-gray-800 hover:bg-gray-300\`;
      // More variants...
    }
  };
  
  return (
    <button className={getButtonClasses()} onClick={onClick}>
      {children}
    </button>
  );
}
\`\`\`

You can now use this in your application. Would you like me to explain how it works or make any modifications?`,
        timestamp: new Date(),
      };
      
      setMessages(prev => [...prev, aiMessage]);
      setIsTyping(false);
    }, 2000);
  }, []);

  const handleCancel = useCallback(() => {
    setIsTyping(false);
    // In a real app, you would cancel the API request here
  }, []);

  // Handle input change
  const handleInputChange = useCallback((e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputValue(e.target.value);
  }, []);

  // Handle form submission
  const handleSubmit = useCallback((e: React.FormEvent) => {
    e.preventDefault();
    sendMessage(inputValue);
  }, [inputValue, sendMessage]);

  return {
    messages,
    isTyping,
    inputValue,
    codeFiles,
    activeFileId,
    messagesEndRef,
    setActiveFileId,
    handleInputChange,
    handleSubmit,
    handleCancel,
    updateFileContent,
  };
}
