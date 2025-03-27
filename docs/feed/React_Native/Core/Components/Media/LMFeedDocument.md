---
sidebar_position: 5
title: Document
slug: /react-native/core/components/media/document
---

## Overview

`LMDocument` is a component designed for rendering document attachments within a post or media feed. It provides the ability to display information about the document, such as the filename and size, and includes functionality to handle document downloads or view actions. This component can be customized to display various document types and offers user interactions for document-related actions, such as opening or removing the document.

<img
src={require('../../../../../static/img/PostWidget/document/docPreview.webp').default}
alt="LMFeedPostLinkCell"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
/>

## Callbacks

- `onTap`: Callback to handle tap events trigerred by on clicking on the attached document.
- `onCancel`: Callback to handle tap events trigerred by on clicking of the cancel button.

## Customisation

| Property              | Type                                                       | Description                                                |
| --------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- |
| `documentIcon`        | [`LMIconProps`](../Fundamentals/LMFeedIcon.md)             | Customization for the document icon.                       |
| `defaultIconSize`     | `number`                                                   | Default size of the document icon.                         |
| `showPageCount`       | `boolean`                                                  | Whether to display the page count of the document.         |
| `showDocumentSize`    | `boolean`                                                  | Whether to show the size of the document.                  |
| `showDocumentFormat`  | `boolean`                                                  | Whether to display the format (file type) of the document. |
| `documentTitleStyle`  | `TextStyle`                                                | Style for the document title text.                         |
| `documentDetailStyle` | `TextStyle`                                                | Style for the document detail text (e.g., size or format). |
| `documentViewStyle`   | `ViewStyle`                                                | Style for the overall document view container.             |
| `onTap`               | `Function`                                                 | Function to trigger when the document is tapped.           |
| `showCancel`          | `boolean`                                                  | Whether to show the cancel button for the document view.   |
| `onCancel`            | `Function`                                                 | Function to trigger when the cancel button is pressed.     |
| `showMoreText`        | `boolean`                                                  | Whether to display additional text, such as "Show More".   |
| `showMoreTextStyle`   | `TextStyle`                                                | Style for the "Show More" text.                            |
| `cancelButton`        | [`CancelButton`](./LMFeedDocument.md/#cancelbutton-object) | Object to customize the cancel button (see table below).   |

### `CancelButton` Object

| Property      | Type                                                          | Description                                          |
| ------------- | ------------------------------------------------------------- | ---------------------------------------------------- |
| `text`        | [`LMTextProps`](../Fundamentals/LMFeedText.md/#customisation) | Customization for the text in the cancel button.     |
| `icon`        | [`LMIconProps`](../Fundamentals/LMFeedIcon.md/#customisation) | Customization for the icon in the cancel button.     |
| `onTap`       | `Function`                                                    | Function triggered when the cancel button is tapped. |
| `placement`   | `start` or `end`                                              | Position of the icon or text in the cancel button.   |
| `buttonStyle` | `ViewStyle`                                                   | Style for the cancel button container.               |
| `isClickable` | `boolean`                                                     | Determines if the cancel button is clickable.        |
