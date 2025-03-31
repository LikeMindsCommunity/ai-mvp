import React, { useState, useRef } from "react"
import { Header } from "@/components/layout/Header"
import { ChatInterface } from "@/components/Chat/ChatInterface"
import { CodeDisplay } from "@/components/CodeEditor/CodeDisplay"
import { PreviewWindow } from "@/components/Preview/PreviewWindow"
import { useChatInteraction } from "@/hooks/useChatInteraction"
import { ViewToggle } from "@/components/layout/ViewToggle"
import { cn } from "@/lib/utils"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import CodeSidebar from "@/components/CodeEditor/CodeSidebar"

type CodePreviewTab = "code" | "preview"

const Index = () => {
  const [activeCodePreviewTab, setActiveCodePreviewTab] =
    useState<CodePreviewTab>("code")
  const [chatWidth, setChatWidth] = useState(30) // Percentage width for the chat window
  const isResizing = useRef(false)

  const {
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
  } = useChatInteraction()

  const handleMouseDown = () => {
    isResizing.current = true
  }

  const handleMouseMove = (e: MouseEvent) => {
    if (!isResizing.current) return
    const newWidth = (e.clientX / window.innerWidth) * 100
    if (newWidth >= 20 && newWidth <= 50) {
      setChatWidth(newWidth)
    }
  }

  const handleMouseUp = () => {
    isResizing.current = false
  }

  React.useEffect(() => {
    window.addEventListener("mousemove", handleMouseMove)
    window.addEventListener("mouseup", handleMouseUp)
    return () => {
      window.removeEventListener("mousemove", handleMouseMove)
      window.removeEventListener("mouseup", handleMouseUp)
    }
  }, [])

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-background to-muted/30">
      {/* <Header /> */}

      <main className="h-screen flex-1 container mx-auto py-6 px-4 md:px-6 flex flex-row gap-6">
        <div
          className="h-[calc(100vh-250px)] border-r border-border/50"
          style={{ width: `${chatWidth}%` }}
        >
          {/* Chat View */}
          <div className="h-full overflow-y-auto">
            <ChatInterface
              messages={messages}
              isTyping={isTyping}
              inputValue={inputValue}
              messagesEndRef={messagesEndRef}
              onInputChange={handleInputChange}
              onSubmit={handleSubmit}
              onCancel={handleCancel}
            />
          </div>
        </div>

        {/* Resizable Divider */}
        <div
          className="w-1 cursor-col-resize bg-border"
          onMouseDown={handleMouseDown}
        ></div>

        {/* Code & Preview View */}
        <div className="flex-1 h-[calc(100vh-250px)] flex flex-row">
          {/* Code Sidebar */}
          {activeCodePreviewTab === "code" && (
            <CodeSidebar
              codeFiles={codeFiles}
              activeFileId={activeFileId}
              setActiveFileId={setActiveFileId}
            />
          )}

          <div className="flex-1 h-full flex flex-col">
            <Tabs
              value={activeCodePreviewTab}
              onValueChange={(value) =>
                setActiveCodePreviewTab(value as CodePreviewTab)
              }
              className="flex-1 flex flex-col overflow-hidden"
            >
              <div className="flex justify-end mb-2">
                <TabsList>
                  <TabsTrigger value="code">Code</TabsTrigger>
                  <TabsTrigger value="preview">Preview</TabsTrigger>
                </TabsList>
              </div>

              <TabsContent value="code" className="flex-1 mt-0 overflow-y-auto">
                <CodeDisplay
                  codeFiles={codeFiles}
                  activeFileId={activeFileId}
                  setActiveFileId={setActiveFileId}
                  updateFileContent={updateFileContent}
                />
              </TabsContent>

              <TabsContent
                value="preview"
                className="flex-1 mt-0 overflow-y-auto"
              >
                <PreviewWindow codeFiles={codeFiles} />
              </TabsContent>
            </Tabs>
          </div>
        </div>
      </main>

      <footer className="py-6 border-t border-border/50">
        <div className="container px-4 text-center text-sm text-muted-foreground">
          <p>SDK integrations</p>
        </div>
      </footer>
    </div>
  )
}

export default Index
