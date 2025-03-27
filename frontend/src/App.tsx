import React from 'react';
import QueryInterface from './components/QueryInterface';

export default function App() {
    return (
        <div className="min-h-screen flex flex-col bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
            {/* Header */}
            <header className="sticky top-0 z-40 w-full border-b bg-gradient-to-r from-violet-600 to-indigo-600 shadow-sm">
                <div className="container flex h-16 items-center px-4 sm:px-6 lg:px-8">
                    <div className="mr-4 flex">
                        <a href="/" className="flex items-center space-x-2">
                            <span className="font-bold text-xl text-white">LikeMinds Documentation Bot</span>
                        </a>
                    </div>
                    <div className="flex flex-1 items-center justify-end space-x-4">
                        <nav className="flex items-center space-x-2">
                            <a
                                href="https://github.com/LikeMindsCommunity"
                                target="_blank"
                                rel="noreferrer"
                                className="text-sm font-medium text-white hover:text-indigo-100 transition-colors"
                            >
                                GitHub
                            </a>
                            <a
                                href="http://docs.likeminds.community"
                                className="text-sm font-medium text-white hover:text-indigo-100 transition-colors"
                            >
                                API Docs
                            </a>
                        </nav>
                    </div>
                </div>
            </header>

            {/* Main content */}
            <main className="flex-1 py-12">
                <div className="container px-4 sm:px-6 lg:px-8">
                    {/* Hero section */}
                    <div className="text-center mb-12">
                        <h1 className="text-2xl font-extrabold tracking-tight lg:text-3xl mb-4 bg-gradient-to-r from-violet-600 to-indigo-600 text-transparent bg-clip-text">
                            Ask anything about LikeMinds SDK
                        </h1>
                        <p className="text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
                            Get instant answers from the documentation for Chat and Feed SDKs
                        </p>
                    </div>

                    {/* Main layout */}
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                        {/* Main query interface */}
                        <div className="lg:col-span-2">
                            <div className="bg-white dark:bg-slate-800 rounded-xl border shadow-lg overflow-hidden">
                                <QueryInterface />
                            </div>
                        </div>

                        {/* Sidebar */}
                        <div>
                            <div className="bg-white dark:bg-slate-800 rounded-xl border shadow-lg p-6">
                                <h2 className="text-lg font-semibold mb-4 text-violet-600 dark:text-violet-400">
                                    Available Documentation
                                </h2>

                                <div className="space-y-4">
                                    <div className="group rounded-lg p-4 transition-all hover:bg-cyan-50 dark:hover:bg-cyan-900/20 transform hover:-translate-y-1 bg-gradient-to-br from-cyan-50 to-cyan-100 dark:from-cyan-900/20 dark:to-cyan-800/20 border border-cyan-100 dark:border-cyan-800/30">
                                        <h3 className="font-medium text-cyan-800 dark:text-cyan-300 mb-1 text-sm">Chat SDK</h3>
                                        <p className="text-sm text-slate-600 dark:text-slate-400">Documentation for implementing chat features</p>
                                    </div>

                                    <div className="group rounded-lg p-4 transition-all hover:bg-emerald-50 dark:hover:bg-emerald-900/20 transform hover:-translate-y-1 bg-gradient-to-br from-emerald-50 to-emerald-100 dark:from-emerald-900/20 dark:to-emerald-800/20 border border-emerald-100 dark:border-emerald-800/30">
                                        <h3 className="font-medium text-emerald-800 dark:text-emerald-300 mb-1 text-sm">Feed SDK</h3>
                                        <p className="text-sm text-slate-600 dark:text-slate-400">Documentation for implementing social feed features</p>
                                    </div>

                                    <div className="group rounded-lg p-4 transition-all hover:bg-violet-50 dark:hover:bg-violet-900/20 transform hover:-translate-y-1 bg-gradient-to-br from-violet-50 to-violet-100 dark:from-violet-900/20 dark:to-violet-800/20 border border-violet-100 dark:border-violet-800/30">
                                        <h3 className="font-medium text-violet-800 dark:text-violet-300 mb-1 text-sm">Platforms</h3>
                                        <p className="text-sm text-slate-600 dark:text-slate-400">Android, iOS, React, React Native, Flutter</p>
                                    </div>
                                </div>

                                <div className="mt-6 p-4 bg-slate-100 dark:bg-slate-700/30 rounded-lg text-xs text-slate-600 dark:text-slate-400">
                                    This assistant uses Retrieval-Augmented Generation (RAG) with Claude 3.7 Sonnet and GPT-4 to provide accurate answers from the documentation.
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </main>

            {/* Footer */}
            <footer className="w-full border-t bg-gradient-to-r from-slate-50/80 to-slate-100/80 dark:from-slate-900/80 dark:to-slate-800/80 backdrop-blur-sm">
                <div className="container flex flex-col sm:flex-row justify-between items-center py-6 px-4 sm:px-6 lg:px-8">
                    <p className="text-sm text-slate-600 dark:text-slate-400">
                        &copy; {new Date().getFullYear()} LikeMinds. All rights reserved.
                    </p>
                    <div className="flex space-x-6 mt-4 sm:mt-0">
                        <a
                            href="#"
                            className="text-sm text-slate-600 dark:text-slate-400 hover:text-violet-600 dark:hover:text-violet-400 transition-colors"
                        >
                            Privacy Policy
                        </a>
                        <a
                            href="#"
                            className="text-sm text-slate-600 dark:text-slate-400 hover:text-violet-600 dark:hover:text-violet-400 transition-colors"
                        >
                            Terms of Service
                        </a>
                    </div>
                </div>
            </footer>
        </div>
    );
} 