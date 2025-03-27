---
sidebar_position: 5
title: Text
slug: /react-native/core/components/fundamentals/text
---

## Overview

The `LMText` component is used to render customizable text in the LikeMinds React Native application, allowing for various styling options and interactivity through press events.

<img
src={require('../../../../../static/img/reactNative/fundamentalLMText.webp').default}
alt="LMFeedPostContent"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="30%"
/>

## Callbacks

- `onTextLayout`: Callback to be trigerred on change of text layout.

## Customisation

| Property       | Type                         | Description                                          |
| -------------- | ---------------------------- | ---------------------------------------------------- |
| `maxLines`     | `number`                     | Defines the maximum lines to be displayed.           |
| `textStyle`    | `TextStyle` or `TextStyle[]` | Represents the style of the text.                    |
| `selectable`   | `boolean`                    | Defines the selection behavior of the text.          |
| `onTextLayout` | `Function`                   | Callback function executed on change of text layout. |
| `children`     | `React.ReactNode`            | Content to be displayed within the text component.   |
