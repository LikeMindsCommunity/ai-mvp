import React, { useState } from "react"
import { CodeFile } from "@/types"
import { cn } from "@/lib/utils"
import { FileCode, Copy, CheckCheck } from "lucide-react"
import { MonacoEditor } from "./MonacoEditor"

interface CodeDisplayProps {
  codeFiles: CodeFile[]
  activeFileId: string
  setActiveFileId: (id: string) => void
  updateFileContent?: (id: string, content: string) => void
}

export const CodeDisplay: React.FC<CodeDisplayProps> = ({
  codeFiles,
  activeFileId,
  setActiveFileId,
  updateFileContent,
}) => {
  const [copied, setCopied] = useState(false)
  const activeFile =
    codeFiles.find((file) => file.id === activeFileId) || codeFiles[0]

  const copyToClipboard = () => {
    if (activeFile) {
      navigator.clipboard.writeText(activeFile.content)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  const handleCodeChange = (value: string) => {
    if (updateFileContent && activeFile) {
      updateFileContent(activeFile.id, value)
    }
  }

  return (
    <div className="flex flex-col h-full overflow-hidden rounded-2xl glass-panel">
      {/* <div className="flex items-center justify-between p-4 border-b border-border/50">
        <h2 className="text-lg font-medium">Code</h2>
        <button
          onClick={copyToClipboard}
          className="flex items-center text-xs text-muted-foreground hover:text-foreground transition-colors"
        >
          {copied ? (
            <>
              <CheckCheck className="h-3.5 w-3.5 mr-1" />
              Copied
            </>
          ) : (
            <>
              <Copy className="h-3.5 w-3.5 mr-1" />
              Copy Code
            </>
          )}
        </button>
      </div> */}

      {/* <div className="border-b border-border/50 overflow-x-auto scrollbar-thin">
        <div className="flex">
          {codeFiles.map((file) => (
            <button
              key={file.id}
              className={cn(
                "flex items-center px-4 py-2 text-sm border-r border-border/50 min-w-[120px] transition-colors",
                file.id === activeFileId
                  ? "bg-accent text-foreground"
                  : "bg-transparent text-muted-foreground hover:text-foreground"
              )}
              onClick={() => setActiveFileId(file.id)}
            >
              <FileCode className="h-3.5 w-3.5 mr-2" />
              <span className="truncate">{file.name}</span>
            </button>
          ))}
        </div>
      </div> */}

      <div className="flex-1 overflow-hidden">
        {activeFile && (
          <MonacoEditor file={activeFile} onChange={handleCodeChange} />
        )}
      </div>
    </div>
  )
}
