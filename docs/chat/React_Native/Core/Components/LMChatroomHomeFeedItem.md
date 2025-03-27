---
sidebar_position: 1
title: Chatroom Item
slug: /react-native/core/components/chatroom-item-item
---

## Overview

The `chatroomItem` component is responsible for rendering individual feed items within the chat screen. It displays information such as the chatroom title, description, participants, and messages, and provides interaction options like joining a chatroom or viewing messages. The component also manages dynamic states like whether the user has joined a chatroom or if the chatroom is pinned.

<img
src={require('../../../../static/img/reactNative/lmHomeFeedItem.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## Customisation

| Property               | Type                                            | Description                                           |
| ---------------------- | ----------------------------------------------- | ----------------------------------------------------- |
| `avatar`               | [`Avatar`](#avatar)                             | Represents the styling for the avatar                 |
| `title`                | [`Title`](#title)                               | Represents the styling for the title text             |
| `lastConversation`     | [`LastConversation`](#lastconversation)         | Represents the styling for the last conversation text |
| `unreadCount`          | [`UnreadCount`](#unreadcount)                   | Represents the styling for the unread message count   |
| `lastConversationTime` | [`LastConversationTime`](#lastconversationtime) | Represents the styling for the last conversation time |

### Avatar

| Property       | Type     | Description                         |
| -------------- | -------- | ----------------------------------- |
| `borderRadius` | `string` | Defines the border radius of avatar |

### Title

| Property     | Type     | Description                           |
| ------------ | -------- | ------------------------------------- |
| `color`      | `string` | Defines the color of title text       |
| `fontSize`   | `number` | Defines the font size of title text   |
| `fontFamily` | `string` | Defines the font family of title text |

### LastConversation

| Property     | Type     | Description                                           |
| ------------ | -------- | ----------------------------------------------------- |
| `color`      | `string` | Defines the color of the last conversation text       |
| `fontSize`   | `number` | Defines the font size of the last conversation text   |
| `fontFamily` | `string` | Defines the font family of the last conversation text |

### UnreadCount

| Property          | Type     | Description                                        |
| ----------------- | -------- | -------------------------------------------------- |
| `color`           | `string` | Defines the color of unread count text             |
| `fontSize`        | `number` | Defines the font size of unread count              |
| `fontFamily`      | `string` | Defines the font family of unread count            |
| `borderRadius`    | `string` | Defines the border radius of unread count badge    |
| `backgroundColor` | `string` | Defines the background color of unread count badge |

### LastConversationTime

| Property     | Type     | Description                                           |
| ------------ | -------- | ----------------------------------------------------- |
| `color`      | `string` | Defines the color of the last conversation time       |
| `fontSize`   | `number` | Defines the font size of the last conversation time   |
| `fontFamily` | `string` | Defines the font family of the last conversation time |

## Props

| Property                 | Type      | Description                                             | Required           |
| ------------------------ | --------- | ------------------------------------------------------- | ------------------ |
| `avatar`                 | `string`  | The avatar URL of the chatroom or participant           | :heavy_check_mark: |
| `title`                  | `string`  | The title or name of the chatroom                       | :heavy_check_mark: |
| `lastMessage`            | `string`  | The last message text in the chatroom                   | :heavy_check_mark: |
| `time`                   | `string`  | The time of the last message                            | :heavy_check_mark: |
| `pinned`                 | `boolean` | Whether the chatroom is pinned                          | :heavy_check_mark: |
| `unreadCount`            | `number`  | The number of unread messages                           | :heavy_check_mark: |
| `lastConversation`       | `any`     | The last conversation data in the chatroom              | :heavy_check_mark: |
| `chatroomID`             | `number`  | The unique ID of the chatroom                           | :heavy_check_mark: |
| `lastConversationMember` | `string`  | The last member involved in the conversation            |                    |
| `isSecret`               | `boolean` | Whether the chatroom is secret                          | :heavy_check_mark: |
| `deletedBy`              | `string`  | The user who deleted the chatroom (if applicable)       |                    |
| `inviteReceiver`         | `any`     | The receiver of the chatroom invitation (if applicable) |                    |
| `chatroomType`           | `number`  | The type of the chatroom                                | :heavy_check_mark: |
| `muteStatus`             | `boolean` | The mute status of the chatroom                         | :heavy_check_mark: |
