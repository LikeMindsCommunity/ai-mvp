import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Button } from '../components/ui/button';
import { Textarea } from '../components/ui/textarea';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../components/ui/card';
import { Switch } from '../components/ui/switch';
import { Label } from '../components/ui/label';

const QueryInterface = () => {
    const [query, setQuery] = useState('');
    const [response, setResponse] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [streamingEnabled, setStreamingEnabled] = useState(false);
    const [status, setStatus] = useState(null);
    const eventSourceRef = useRef(null);

    // API endpoint for queries - Get from environment variables
    const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    const API_QUERY_ENDPOINT = `${API_URL}/api/query`;

    // Clean up event source on unmount
    useEffect(() => {
        return () => {
            if (eventSourceRef.current) {
                eventSourceRef.current.close();
            }
        };
    }, []);

    // Handle streaming mode toggle
    const handleStreamingToggle = React.useCallback((checked) => {
        console.log(`Switching streaming mode to: ${checked}`);
        setStreamingEnabled(checked);
        // No API calls or side effects here - just update the state
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!query.trim()) {
            // Show error for empty query
            setError('Please enter a query to search the documentation');
            return;
        }

        setLoading(true);
        setError(null);
        setResponse(null);
        setStatus(null);

        // Close any existing event source
        if (eventSourceRef.current) {
            eventSourceRef.current.close();
            eventSourceRef.current = null;
        }

        if (streamingEnabled) {
            // Handle streaming response
            handleStreamingQuery();
        } else {
            // Handle regular response
            handleRegularQuery();
        }
    };

    const handleRegularQuery = async () => {
        try {
            console.log(`Sending query to ${API_QUERY_ENDPOINT}`);
            const response = await axios.post(API_QUERY_ENDPOINT, {
                query: query,
                stream: false,
                // Using default values for initial and final results
                conversation_history: []
            });

            setResponse(response.data);
            console.log('Response received:', response.data);

            // Log metrics
            console.log('Query metrics:', response.data.metrics);

        } catch (err) {
            console.error('Error querying the API:', err);
            setError(err.response?.data?.detail || err.message || 'An error occurred');
        } finally {
            setLoading(false);
        }
    };

    const handleStreamingQuery = () => {
        try {
            console.log(`Sending streaming query to ${API_QUERY_ENDPOINT}`);

            // Set up the event source with GET parameters
            const encodedQuery = encodeURIComponent(query);
            // Use full URL including protocol for EventSource
            const eventSourceUrl = `${API_QUERY_ENDPOINT}?query=${encodedQuery}&stream=true`;
            console.log(`Creating EventSource with URL: ${eventSourceUrl}`);
            const eventSource = new EventSource(eventSourceUrl);
            eventSourceRef.current = eventSource;

            // Initialize partial response
            const partialResponse = {
                response: "",
                sources: [],
                metrics: { total_time: 0 }
            };

            // Set initial empty response to show the UI
            setResponse(partialResponse);

            // Handle message events
            eventSource.onmessage = (event) => {
                try {
                    const eventData = JSON.parse(event.data);
                    console.log('Received event data:', eventData);

                    // Process different event types
                    if (eventData.event === 'status') {
                        setStatus(eventData.data);
                    } else if (eventData.event === 'token') {
                        // Stream tokens for the LLM response
                        setResponse(prev => ({
                            ...prev,
                            response: prev.response + eventData.data.token
                        }));
                    } else if (eventData.event === 'response_complete') {
                        // Update with final metadata (sources, metrics)
                        setResponse(prev => ({
                            ...prev,
                            sources: eventData.data.sources,
                            metrics: eventData.data.metrics
                        }));

                        eventSource.close();
                        eventSourceRef.current = null;
                        setLoading(false);
                    } else if (eventData.event === 'error') {
                        setError(eventData.data.error || 'An error occurred');
                        eventSource.close();
                        eventSourceRef.current = null;
                        setLoading(false);
                    } else if (eventData.event === 'done') {
                        console.log('Stream completed');
                        eventSource.close();
                        eventSourceRef.current = null;
                        setLoading(false);
                    }
                } catch (err) {
                    console.error('Error parsing event data:', err);
                }
            };

            // Handle connection errors
            eventSource.onerror = (err) => {
                console.error('EventSource error:', err);
                setError('Connection error. Please try again.');
                eventSource.close();
                eventSourceRef.current = null;
                setLoading(false);
            };
        } catch (err) {
            console.error('Error setting up EventSource:', err);
            setError(err.message || 'An error occurred while setting up the connection');
            setLoading(false);
        }
    };

    return (
        <div className="mx-auto max-w-5xl py-8 px-4 sm:px-6 lg:px-8">
            <div className="bg-white dark:bg-slate-900 shadow rounded-lg p-6">
                <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-6">LikeMinds Documentation Search</h2>

                <form onSubmit={handleSubmit} className="mb-6" noValidate>
                    <div className="mb-4">
                        <Textarea
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            placeholder="Ask a question about LikeMinds SDKs..."
                            className="h-24 text-base"
                        />
                    </div>

                    <div className="flex flex-col sm:flex-row gap-4 justify-between items-start sm:items-center">
                        <div
                            className="flex items-center space-x-2"
                            onClick={(e) => e.stopPropagation()}
                            onSubmit={(e) => e.preventDefault()}
                        >
                            <Switch
                                id="streaming-mode"
                                checked={streamingEnabled}
                                onCheckedChange={handleStreamingToggle}
                            />
                            <Label htmlFor="streaming-mode">Streaming mode</Label>
                        </div>

                        <Button
                            type="submit"
                            disabled={loading}
                            className="min-w-32"
                        >
                            {loading ? 'Processing...' : 'Search'}
                        </Button>
                    </div>
                </form>

                {error && (
                    <div className="p-4 mt-4 border-l-4 border-red-500 bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300">
                        <p>{error}</p>
                    </div>
                )}

                {status && loading && (
                    <div className="p-4 mt-4 border-l-4 border-blue-500 bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300">
                        <p className="font-medium">{status.message}</p>
                    </div>
                )}

                {response && (
                    <Card className="mt-6 border-slate-200 dark:border-slate-700">
                        <CardHeader className="pb-2">
                            <CardTitle className="text-xl text-violet-600 dark:text-violet-400">Response</CardTitle>
                        </CardHeader>

                        <CardContent className="pb-2 space-y-6">
                            <div className="p-4 bg-slate-50 dark:bg-slate-800/50 rounded-lg text-slate-800 dark:text-slate-200 leading-relaxed markdown-content">
                                <ReactMarkdown
                                    remarkPlugins={[remarkGfm]}
                                    components={{
                                        code({ node, inline, className, children, ...props }) {
                                            const match = /language-(\w+)/.exec(className || '');
                                            return (!inline && (match || node.position?.start.line !== node.position?.end.line)) ? (
                                                <pre className="bg-slate-800 dark:bg-slate-900 overflow-x-auto p-4 rounded-md my-4 text-white">
                                                    <code className="text-sm font-mono" {...props}>
                                                        {String(children).replace(/\n$/, '')}
                                                    </code>
                                                </pre>
                                            ) : (
                                                <code className="bg-slate-200 dark:bg-slate-700 px-1 py-0.5 rounded text-sm font-mono" {...props}>
                                                    {children}
                                                </code>
                                            );
                                        },
                                        h1: ({ children }) => <h1 className="text-2xl font-bold mt-6 mb-4">{children}</h1>,
                                        h2: ({ children }) => <h2 className="text-xl font-bold mt-5 mb-3">{children}</h2>,
                                        h3: ({ children }) => <h3 className="text-lg font-bold mt-4 mb-2">{children}</h3>,
                                        p: ({ children }) => <p className="mb-4">{children}</p>,
                                        ul: ({ children }) => <ul className="mb-4 ml-6 list-disc">{children}</ul>,
                                        ol: ({ children }) => <ol className="mb-4 ml-6 list-decimal">{children}</ol>,
                                        li: ({ children }) => <li className="mb-1">{children}</li>,
                                        a: ({ href, children }) => (
                                            <a href={href} className="text-violet-600 dark:text-violet-400 hover:underline" target="_blank" rel="noopener noreferrer">
                                                {children}
                                            </a>
                                        ),
                                        blockquote: ({ children }) => (
                                            <blockquote className="border-l-4 border-slate-300 dark:border-slate-700 pl-4 italic my-4">
                                                {children}
                                            </blockquote>
                                        ),
                                        table: ({ children }) => (
                                            <div className="overflow-x-auto my-4">
                                                <table className="min-w-full divide-y divide-slate-200 dark:divide-slate-700">
                                                    {children}
                                                </table>
                                            </div>
                                        ),
                                        thead: ({ children }) => <thead className="bg-slate-100 dark:bg-slate-800">{children}</thead>,
                                        tbody: ({ children }) => <tbody className="divide-y divide-slate-200 dark:divide-slate-800">{children}</tbody>,
                                        tr: ({ children }) => <tr>{children}</tr>,
                                        th: ({ children }) => <th className="px-4 py-2 text-left text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider">{children}</th>,
                                        td: ({ children }) => <td className="px-4 py-2">{children}</td>,
                                    }}
                                >
                                    {response.response}
                                </ReactMarkdown>
                            </div>

                            {response.sources && response.sources.length > 0 && (
                                <div className="space-y-3">
                                    <h4 className="text-sm font-semibold text-slate-700 dark:text-slate-300">Sources</h4>
                                    <div className="p-4 bg-indigo-50 dark:bg-indigo-900/20 rounded-lg space-y-2">
                                        {response.sources.map((source, index) => (
                                            <div
                                                key={index}
                                                className="p-2 bg-white dark:bg-slate-800/50 rounded-md text-xs text-slate-600 dark:text-slate-400"
                                            >
                                                {index + 1}. {source}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </CardContent>

                        <CardFooter>
                            <div className="flex justify-between items-center w-full p-3 bg-violet-50 dark:bg-violet-900/20 rounded-lg text-xs">
                                <span className="font-semibold text-violet-800 dark:text-violet-300">Response Time:</span>
                                <span className="text-violet-700 dark:text-violet-400 font-medium">
                                    {response.metrics?.total_time.toFixed(2)} seconds
                                </span>
                            </div>
                        </CardFooter>
                    </Card>
                )}
            </div>
        </div>
    );
};

export default QueryInterface; 