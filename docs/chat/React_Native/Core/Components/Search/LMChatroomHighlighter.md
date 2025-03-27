---
sidebar_position: 2
title: Chatroom Highlighter
slug: /react-native/core/components/search/chatroom-highlighter
---

## Overview

The `Highlighter` component is designed to highlight specific text within a larger body of text. It takes in a string of text and a list of keywords, dynamically rendering the keywords in a highlighted format while keeping the surrounding text in a normal style. This is particularly useful for enhancing readability and drawing attention to important terms or phrases in chat or document contexts.

<img
src={require('../../../../../static/img/reactNative/lmSearchHighlighter.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## Customisation

The highlighter can be customised using the [`searchedHighlightedTextStyle`](./LMChatroomSearchHeader.md/#customisations) and [`searchedNonHighlightedTextStyle`](./LMChatroomHighlighter.md/#customisation)

## Props

| Property          | Type                    | Description                                            | Required           |
| ----------------- | ----------------------- | ------------------------------------------------------ | ------------------ |
| `autoEscape`      | `boolean`               | Specifies whether to auto escape the text.             |                    |
| `highlightStyle`  | `TextStyle[]` or `null` | Defines the style to apply to highlighted text.        |                    |
| `searchWords`     | `string[]`              | An array of words to search and highlight in the text. | :heavy_check_mark: |
| `textToHighlight` | `string`                | The text that will be highlighted.                     | :heavy_check_mark: |
| `sanitize`        | `Function`              | A function to sanitize the text before highlighting.   |                    |
| `style`           | `TextStyle[]` or `null` | Specifies the style of the text.                       |                    |
