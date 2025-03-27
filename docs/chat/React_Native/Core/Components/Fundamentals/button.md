---
sidebar_position: 3
title: Chat Button
slug: /react-native/core/fundamentals/button
---

## Overview

`LMChatButton` serves as a UI component designed for the purpose of rendering various buttons, including Attachment buttons, Send button, Mic button, and other input buttons within a chat interface.

<img
src={require('../../../../../static/img/reactNative/lmButton.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## Customisation/Props

The `LMChatButton` component requires certain props, some of which are mandatory, while others are optional. Here is a breakdown of the available props along with their types:

| Parameter   | Type                  | Description                                          | Optional           |
| ----------- | --------------------- | ---------------------------------------------------- | ------------------ |
| text        | LMChatTextViewProps   | Represents the text displayed on the button          | :heavy_check_mark: |
| icon        | LMChatIconProps       | Represents the icon displayed on the button          | :heavy_check_mark: |
| onTap       | (value?: any) => void | Represents the functionality on click of the button  |                    |
| placement   | "start" \| "end"      | Represents the placement of the icon on the button   | :heavy_check_mark: |
| isActive    | boolean               | Represents the active/inactive state of the button   | :heavy_check_mark: |
| activeIcon  | LMChatIconProps       | Icon displayed when the button is in an active state | :heavy_check_mark: |
| activeText  | LMChatTextViewProps   | Text displayed when the button is in an active state | :heavy_check_mark: |
| buttonStyle | ViewStyle             | Represents the style of the button                   | :heavy_check_mark: |
| isClickable | boolean               | Indicates if the button is disabled or not           | :heavy_check_mark: |
