---
sidebar_position: 4
title: Reaction List
slug: /react-native/core/components/reaction-list
---

## Overview

The `MessageList` component is responsible for rendering a list of messages in a chat interface. It manages the display of individual messages, handling any necessary UI elements like timestamps and sender information. The component also includes functionality for displaying loading indicators and empty states when no messages are available.

<img
src={require('../../../../../static/img/reactNative/lmReactionList.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## Customisations

| Property                         | Type     | Description                                     |
| -------------------------------- | -------- | ----------------------------------------------- |
| `reactionSize`                   | `number` | Defines the size of the reaction icon.          |
| `reactionLeftItemStroke`         | `string` | Sets the stroke color for the left reaction.    |
| `reactionRightItemStroke`        | `string` | Sets the stroke color for the right reaction.   |
| `reactionItemBorderRadius`       | `number` | Defines the border radius for reaction items.   |
| `gap`                            | `number` | Specifies the gap between items.                |
| `selectedMessageBackgroundColor` | `string` | Sets the background color of selected messages. |
| `tabOptionColor`                 | `string` | Defines the color for the tab option.           |

## Props

| Property            | Type       | Description                                         | Required           |
| ------------------- | ---------- | --------------------------------------------------- | ------------------ |
| `item`              | `any`      | Represents the current item in the list.            | :heavy_check_mark: |
| `chatroomID`        | `any`      | ID of the chatroom associated with the item.        | :heavy_check_mark: |
| `userIdStringified` | `any`      | Stringified version of the user ID.                 | :heavy_check_mark: |
| `reactionArr`       | `any`      | Array containing reactions for the item.            |                    |
| `isTypeSent`        | `boolean`  | Specifies if the item type is 'sent'.               |                    |
| `isIncluded`        | `boolean`  | Indicates whether the item is included in the view. | :heavy_check_mark: |
| `handleLongPress`   | `Function` | Triggered when the item is long-pressed.            | :heavy_check_mark: |
| `removeReaction`    | `Function` | Removes a reaction from the item.                   | :heavy_check_mark: |
