import React from "react"
import { cn } from "@/lib/utils"
import { FileCode } from "lucide-react"
import { CodeFile } from "@/types"

interface CodeSidebarProps {
  codeFiles: CodeFile[]
  activeFileId: string
  setActiveFileId: (id: string) => void
}

const CodeSidebar: React.FC<CodeSidebarProps> = ({
  codeFiles,
  activeFileId,
  setActiveFileId,
}) => {
  return (
    <div className="w-64 h-full bg-background border-r border-border/50 overflow-y-auto">
      <div className="p-4 border-b border-border/50">
        <h2 className="text-lg font-medium">Files</h2>
      </div>
      <ul className="p-2">
        {codeFiles.map((file) => (
          <li key={file.id}>
            <button
              className={cn(
                "w-full flex items-center px-4 py-2 text-sm rounded-md transition-colors",
                file.id === activeFileId
                  ? "bg-accent text-foreground"
                  : "bg-transparent text-muted-foreground hover:bg-muted hover:text-foreground"
              )}
              onClick={() => setActiveFileId(file.id)}
            >
              <FileCode className="h-4 w-4 mr-2" />
              <span className="truncate">{file.name}</span>
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default CodeSidebar
