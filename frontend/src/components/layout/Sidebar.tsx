import React from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '@/store';
import { Button } from '@/components/ui/button';
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from '@/components/ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

const Sidebar: React.FC = () => {
    const { currentMode } = useSelector((state: RootState) => state.mode);
    const { threads } = useSelector((state: RootState) => state.chat);
    const { name: projectName } = useSelector((state: RootState) => state.project);

    return (
        <div className="w-64 bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-700 h-[calc(100vh-4rem)] flex flex-col">
            <div className="p-4 border-b border-slate-200 dark:border-slate-700">
                <Dialog>
                    <DialogTrigger asChild>
                        <Button className="w-full justify-start" variant="outline">
                            {projectName || 'Select Project'}
                        </Button>
                    </DialogTrigger>
                    <DialogContent>
                        <DialogHeader>
                            <DialogTitle>Project Selection</DialogTitle>
                            <DialogDescription>
                                Select an existing project or create a new one
                            </DialogDescription>
                        </DialogHeader>
                        {/* Project selection content */}
                    </DialogContent>
                </Dialog>
            </div>

            <div className="flex-1 overflow-y-auto">
                <Tabs defaultValue="chat" className="w-full">
                    <TabsList className="w-full justify-start border-b border-slate-200 dark:border-slate-700 px-4">
                        <TabsTrigger value="chat">Chat</TabsTrigger>
                        <TabsTrigger value="files">Files</TabsTrigger>
                    </TabsList>

                    <TabsContent value="chat" className="p-0">
                        <div className="space-y-2 p-4">
                            {threads.map((thread) => (
                                <Button
                                    key={thread.id}
                                    variant="ghost"
                                    className="w-full justify-start text-left font-normal"
                                >
                                    {thread.title}
                                </Button>
                            ))}

                            {threads.length === 0 && (
                                <p className="text-sm text-slate-500 dark:text-slate-400 text-center py-4">
                                    No chat threads yet
                                </p>
                            )}
                        </div>
                    </TabsContent>

                    <TabsContent value="files" className="p-0">
                        <div className="space-y-2 p-4">
                            {currentMode === 'documentation' ? (
                                <p className="text-sm text-slate-500 dark:text-slate-400 text-center py-4">
                                    Documentation files will appear here
                                </p>
                            ) : (
                                <p className="text-sm text-slate-500 dark:text-slate-400 text-center py-4">
                                    Project files will appear here
                                </p>
                            )}
                        </div>
                    </TabsContent>
                </Tabs>
            </div>

            <div className="p-4 border-t border-slate-200 dark:border-slate-700">
                <Button variant="outline" className="w-full">
                    {currentMode === 'documentation' ? 'New Document' : 'New Feature'}
                </Button>
            </div>
        </div>
    );
};

export default Sidebar; 