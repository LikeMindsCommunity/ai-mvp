---
sidebar_position: 4
title: Search Header
slug: /react-native/core/components/search/search-header
---

## Overview

The `SearchHeader` component is responsible for rendering the search bar header in the chat interface. It allows users to search for specific chatrooms, messages, or participants within the chat application. The component typically includes styling for the search input field, a placeholder text, and supports customization for various UI elements, such as colors, font styles, and other visual properties. It enhances user experience by offering a streamlined way to search through content while maintaining a clean and customizable UI.

<img
src={require('../../../../../static/img/reactNative/lmSearchHeader.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## Customisations

| Property                     | Type        | Description                                      |
| ---------------------------- | ----------- | ------------------------------------------------ |
| `backArrowColor`             | `string`    | The color of the back arrow icon.                |
| `crossIconColor`             | `string`    | The color of the cross icon.                     |
| `searchPlaceholderTextColor` | `string`    | The color of the placeholder text in the search. |
| `searchText`                 | `TextStyle` | The style applied to the search input text.      |
