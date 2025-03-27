---
sidebar_position: 4
title: Swipeable
slug: /react-native/core/components/media/swipeable
---

## Overview

The `Swipeable` component in the LikeMinds Chat React Native integration provides swipe gesture functionality for items in a list or collection. It enables users to perform actions like deleting, replying, or reacting to messages by swiping left or right on an item. The component manages the swipe gestures, renders any actions tied to the swipe, and ensures a smooth and responsive user interaction, enhancing the overall chat experience by allowing quick access to these options.

<img
src={require('../../../../../static/img/reactNative/lmSwipeableView.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## Props

| Property          | Type              | Description                               | Default | Required           |
| ----------------- | ----------------- | ----------------------------------------- | ------- | ------------------ |
| `onFocusKeyboard` | `Function`        | Triggered when the keyboard gains focus.  |         |                    |
| `item`            | `Conversation`    | Represents the conversation data.         |         | :heavy_check_mark: |
| `isStateIncluded` | `boolean`         | Indicates if the state is included.       |         | :heavy_check_mark: |
| `children`        | `React.ReactNode` | The child elements to be rendered inside. |         |                    |
