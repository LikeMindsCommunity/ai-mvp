
import React from 'react';
import { LayoutGrid, MessageSquare } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';

type ViewMode = 'chat' | 'codeAndPreview';

interface ViewToggleProps {
  activeView: ViewMode;
  onViewChange: (view: ViewMode) => void;
}

export const ViewToggle: React.FC<ViewToggleProps> = ({ activeView, onViewChange }) => {
  return (
    <div className="fixed bottom-6 right-6 z-10">
      <TooltipProvider>
        <div className="flex bg-background/80 backdrop-blur-sm rounded-full p-1 shadow-md border border-border/50">
          <Tooltip>
            <TooltipTrigger asChild>
              <Button
                variant={activeView === 'chat' ? 'default' : 'ghost'}
                size="icon"
                onClick={() => onViewChange('chat')}
                className="rounded-full"
                aria-label="Chat View"
              >
                <MessageSquare className="h-5 w-5" />
              </Button>
            </TooltipTrigger>
            <TooltipContent side="top">
              <p>Chat View</p>
            </TooltipContent>
          </Tooltip>

          <Tooltip>
            <TooltipTrigger asChild>
              <Button
                variant={activeView === 'codeAndPreview' ? 'default' : 'ghost'}
                size="icon"
                onClick={() => onViewChange('codeAndPreview')}
                className="rounded-full"
                aria-label="Code & Preview"
              >
                <LayoutGrid className="h-5 w-5" />
              </Button>
            </TooltipTrigger>
            <TooltipContent side="top">
              <p>Code & Preview</p>
            </TooltipContent>
          </Tooltip>
        </div>
      </TooltipProvider>
    </div>
  );
};
