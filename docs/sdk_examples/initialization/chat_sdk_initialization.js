/**
 * LikeMinds Chat SDK Initialization Example
 * 
 * This example demonstrates the proper way to initialize the LikeMinds Chat SDK
 * in a React Native application, including all necessary configuration options
 * and best practices for error handling.
 */

import React, { useEffect, useState } from 'react';
import { View, Text, Alert } from 'react-native';
import { LMChatClient } from '@likeminds.community/chat-rn';

const ChatSDKInitializationExample = () => {
    const [isInitialized, setIsInitialized] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        // Initialize the Chat SDK when the component mounts
        initializeChatSDK();
    }, []);

    /**
     * Initialize the LikeMinds Chat SDK with proper configuration
     * 
     * Important considerations:
     * 1. API Key should be stored securely, not hardcoded
     * 2. User ID must be unique and persistent
     * 3. Environment should match your backend configuration
     * 4. Always handle initialization errors
     */
    const initializeChatSDK = async () => {
        try {
            // Configuration object for the SDK
            const config = {
                apiKey: 'YOUR_API_KEY', // Replace with your actual API key
                userId: 'unique_user_id', // Replace with your user's unique ID
                userName: 'User Display Name', // User's display name

                // Advanced configuration options
                environment: 'PRODUCTION', // 'PRODUCTION' or 'STAGING'
                enableLogging: __DEV__, // Enable logs only in development

                // Storage configuration (optional)
                storageConfig: {
                    cacheSize: 50, // MB
                    retentionPeriod: 7, // Days to retain messages locally
                },

                // Notification configuration (optional)
                notificationConfig: {
                    enabled: true,
                    iconResId: 'ic_notification', // Android notification icon
                    channelId: 'chat_notifications', // Android notification channel
                }
            };

            // Initialize the SDK with the config
            const response = await LMChatClient.initialize(config);

            // Check if initialization was successful
            if (response.success) {
                console.log('Chat SDK initialized successfully');
                setIsInitialized(true);

                // Register event listeners after successful initialization
                registerEventListeners();
            } else {
                // Handle initialization failure
                console.error('Chat SDK initialization failed:', response.error);
                setError(response.error?.message || 'Failed to initialize Chat SDK');

                // Show error to user
                Alert.alert(
                    'Initialization Failed',
                    'Could not initialize the chat. Please try again later.',
                    [{ text: 'OK' }]
                );
            }
        } catch (error) {
            // Handle unexpected errors
            console.error('Unexpected error during Chat SDK initialization:', error);
            setError(error?.message || 'Unexpected error during initialization');

            // Show error to user
            Alert.alert(
                'Error',
                'An unexpected error occurred. Please check your internet connection and try again.',
                [{ text: 'OK' }]
            );
        }
    };

    /**
     * Register event listeners for the Chat SDK
     * This is important for receiving real-time updates
     */
    const registerEventListeners = () => {
        // Listen for new messages
        LMChatClient.addListener('onNewMessage', (message) => {
            console.log('New message received:', message);
            // Handle new message (e.g., update UI, play sound)
        });

        // Listen for connection state changes
        LMChatClient.addListener('onConnectionStateChanged', (state) => {
            console.log('Connection state changed:', state);
            // Handle connection state changes
        });

        // Listen for error events
        LMChatClient.addListener('onError', (error) => {
            console.error('Chat SDK error:', error);
            // Handle error event
        });

        console.log('Event listeners registered');
    };

    // Simple UI to show initialization status
    return (
        <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
            <Text style={{ fontSize: 18, marginBottom: 20 }}>
                Chat SDK Status: {isInitialized ? 'Initialized' : 'Not Initialized'}
            </Text>

            {error && (
                <Text style={{ color: 'red', textAlign: 'center', margin: 20 }}>
                    Error: {error}
                </Text>
            )}
        </View>
    );
};

export default ChatSDKInitializationExample;

/**
 * Additional Notes:
 * 
 * - Always initialize the SDK in a component that loads early in your app
 *   lifecycle, such as your App.js or a splash screen component.
 * 
 * - The API key should be stored securely and not hardcoded. Consider using
 *   environment variables or a secure storage solution.
 * 
 * - User ID must be unique and consistent across sessions. It's often tied
 *   to your app's authentication system.
 * 
 * - This example uses React Hooks, but the same principles apply when using
 *   class components or other frameworks.
 * 
 * - The LikeMinds Chat SDK requires a stable internet connection for initialization.
 *   Consider implementing retry logic for poor network conditions.
 */ 