
import React, { useEffect, useState } from 'react';
import { DeviceViewMode, CodeFile } from '@/types';
import { cn } from '@/lib/utils';
import { Laptop, Smartphone, Tablet, RotateCcw, ExternalLink } from 'lucide-react';

interface PreviewWindowProps {
  codeFiles: CodeFile[];
  isLoading?: boolean;
}

export const PreviewWindow: React.FC<PreviewWindowProps> = ({
  codeFiles,
  isLoading = false,
}) => {
  const [deviceMode, setDeviceMode] = useState<DeviceViewMode>('desktop');
  const [key, setKey] = useState(0); // Used for forcing iframe refresh
  const [error, setError] = useState<string | null>(null);

  // Force refresh preview when code changes
  useEffect(() => {
    refreshPreview();
  }, [codeFiles]);

  const refreshPreview = () => {
    setKey(prev => prev + 1);
    setError(null);
  };

  const getPreviewWidth = () => {
    switch (deviceMode) {
      case 'mobile':
        return 'w-[320px]';
      case 'tablet':
        return 'w-[768px]';
      default:
        return 'w-full';
    }
  };

  const generateHtmlPreview = () => {
    try {
      // Find main files
      const appCode = codeFiles.find(file => file.name === 'App.js')?.content || '';
      const cssCode = codeFiles.find(file => file.name === 'styles.css')?.content || '';
      
      return `
        <!DOCTYPE html>
        <html>
          <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <script src="https://cdn.tailwindcss.com"></script>
            <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
            <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
            <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
            <style>
              ${cssCode}
              body { margin: 0; padding: 0; }
              #root { width: 100%; height: 100vh; }
              .error-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(255, 0, 0, 0.05);
                color: #e00;
                padding: 20px;
                font-family: monospace;
                white-space: pre-wrap;
                overflow: auto;
                z-index: 9999;
              }
            </style>
          </head>
          <body>
            <div id="root"></div>
            <script type="text/babel">
              try {
                ${appCode}
                
                ReactDOM.render(<App />, document.getElementById('root'));
              } catch (error) {
                const errorDiv = document.createElement('div');
                errorDiv.className = 'error-overlay';
                errorDiv.textContent = error.toString();
                document.body.appendChild(errorDiv);
                console.error(error);
              }
            </script>
          </body>
        </html>
      `;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred generating preview');
      return `
        <!DOCTYPE html>
        <html>
          <body>
            <div style="color: red; padding: 20px; font-family: monospace;">
              Error generating preview: ${error || 'Unknown error'}
            </div>
          </body>
        </html>
      `;
    }
  };

  const htmlPreview = generateHtmlPreview();

  const handleIframeError = () => {
    setError('Failed to render preview. Check console for details.');
  };

  return (
    <div className="flex flex-col h-full overflow-hidden rounded-2xl glass-panel">
      <div className="flex items-center justify-between p-4 border-b border-border/50">
        <h2 className="text-lg font-medium">Preview</h2>
        <div className="flex items-center space-x-2">
          <button
            className={cn(
              "p-1.5 rounded-md transition-colors",
              deviceMode === 'desktop' 
                ? "bg-accent text-foreground" 
                : "text-muted-foreground hover:text-foreground"
            )}
            onClick={() => setDeviceMode('desktop')}
            title="Desktop view"
          >
            <Laptop className="h-4 w-4" />
          </button>
          <button
            className={cn(
              "p-1.5 rounded-md transition-colors",
              deviceMode === 'tablet' 
                ? "bg-accent text-foreground" 
                : "text-muted-foreground hover:text-foreground"
            )}
            onClick={() => setDeviceMode('tablet')}
            title="Tablet view"
          >
            <Tablet className="h-4 w-4" />
          </button>
          <button
            className={cn(
              "p-1.5 rounded-md transition-colors",
              deviceMode === 'mobile' 
                ? "bg-accent text-foreground" 
                : "text-muted-foreground hover:text-foreground"
            )}
            onClick={() => setDeviceMode('mobile')}
            title="Mobile view"
          >
            <Smartphone className="h-4 w-4" />
          </button>
          <button
            className="p-1.5 rounded-md text-muted-foreground hover:text-foreground transition-colors"
            onClick={refreshPreview}
            title="Refresh preview"
          >
            <RotateCcw className="h-4 w-4" />
          </button>
          <button
            className="p-1.5 rounded-md text-muted-foreground hover:text-foreground transition-colors"
            title="Open in new tab"
            onClick={() => {
              const newWindow = window.open('', '_blank');
              if (newWindow) {
                newWindow.document.write(htmlPreview);
                newWindow.document.close();
              }
            }}
          >
            <ExternalLink className="h-4 w-4" />
          </button>
        </div>
      </div>

      <div className="flex-1 bg-background/50 overflow-hidden p-4 flex items-center justify-center">
        <div className={cn(
          "h-full transition-all duration-300 overflow-hidden rounded-md border border-border bg-white",
          getPreviewWidth()
        )}>
          {isLoading ? (
            <div className="h-full w-full flex items-center justify-center">
              <div className="flex flex-col items-center">
                <div className="animate-pulse-slow h-8 w-8 rounded-full bg-muted"></div>
                <p className="mt-2 text-sm text-muted-foreground">Loading preview...</p>
              </div>
            </div>
          ) : error ? (
            <div className="h-full w-full flex items-center justify-center p-4">
              <div className="bg-red-50 border border-red-200 rounded-md p-4 text-red-500 font-mono text-sm whitespace-pre-wrap overflow-auto">
                {error}
              </div>
            </div>
          ) : (
            <iframe
              key={key}
              title="Preview"
              className="w-full h-full"
              srcDoc={htmlPreview}
              sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox"
              onError={handleIframeError}
            />
          )}
        </div>
      </div>
    </div>
  );
};
