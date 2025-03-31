
import React from 'react';
import { Github } from 'lucide-react';

export const Header: React.FC = () => {
  return (
    <header className="py-4 px-6 flex items-center justify-between">
      <div className="flex items-center">
        <div className="font-medium text-xl">BuildAI</div>
      </div>
      <div className="flex items-center space-x-4">
        <a 
          href="#" 
          className="text-muted-foreground hover:text-foreground transition-colors text-sm"
        >
          Documentation
        </a>
        <a 
          href="#" 
          className="text-muted-foreground hover:text-foreground transition-colors text-sm"
        >
          Examples
        </a>
        <a 
          href="#" 
          className="text-muted-foreground hover:text-foreground transition-colors"
        >
          <Github className="h-5 w-5" />
        </a>
      </div>
    </header>
  );
};
