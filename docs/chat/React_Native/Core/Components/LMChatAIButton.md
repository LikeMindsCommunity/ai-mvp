---
sidebar_position: 8
title: AI Chatbot Initiate Button
slug: /react-native/core/components/AI-Chatbot-Initiate-button
---

## Overview

The `LMChatAIButton` component is responsible for initiating the SDK and navigating the user to a chatroom with the AI Chatbot.

<img
src={require('../../../../static/img/reactNative/LMChatAIButton.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## Styling Customisation

These styling properties for the `LMChatAIButton` component can be set using the `setLMChatAIButtonStyle` on the `STYLES` object.

| Property                | Type                                | Description         |
| ----------------------- | ----------------------------------- | ------------------- |
| `buttonStyle`           | `ViewStyle`     | Defines the style for the user's name.  |
| `textStyle`             | `TextStyle`     | Defines the style for the user's title. |
| `iconStyle`             | `ImageStyle`    | Placeholder text for the search input.  |

## Props

| Property          | Type                        | Description                                                     |
|-------------------|-----------------------------|-----------------------------------------------------------------|
| `text`            | `string`                   | The text displayed on the button.                                |
| `textSize`        | `number`                   | The size of the text on the button.                              |
| `textColor`       | `string`                   | The color of the text.                                           |
| `backgroundColor` | `string`                   | The background color of the button.                              |
| `borderRadius`    | `number`                   | The border radius of the button.                                 |
| `icon`            | `Object`                   | The icon displayed on the button.                                |
| `iconPlacement`   | `string`                   | The position of the icon on the button.                          |
| `apiKey`          | `string`                   | The API key required for authentication.                         |
| `uuid`            | `string`                   | The unique identifier for the user.                              |
| `userName`        | `string`                   | The name of the user.                                            |
| `imageUrl`        | `string`                   | The URL of the user's image.                                     |
| `isGuest`         | `boolean`                  | Indicates whether the user is a guest.                           |
| `accessToken`     | `string`                   | The access token for authentication.(API Key Security flow)      |
| `refreshToken`    | `string`                   | The refresh token for renewing access.(API Key Security flow)    |
| `onTap`           | `() => void`               | The function executed when the button is tapped.                 |
