---
sidebar_position: 2
title: Explore Feed Item
slug: /react-native/core/components/explore-feed/explore-feed-item
---

## Overview

The `ExploreFeedItem` component renders a single item within an explore feed, displaying relevant content like media, text, or any associated user interactions. It handles the layout, presentation, and formatting of the feed items, making them interactable within the explore section.

<img
src={require('../../../../../static/img/reactNative/lmExploreFeedItem.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## Customisation

| Property              | Type                                        | Description                                      |
| --------------------- | ------------------------------------------- | ------------------------------------------------ |
| `header`              | [Header](#header)                           | Style configuration for the header               |
| `filterHeader`        | [FilterHeader](#filterheader)               | Style configuration for the filter header        |
| `chatroomTitle`       | [ChatroomTitle](#chatroomtitle)             | Style configuration for the chatroom title       |
| `chatroomSubTitle`    | [ChatroomSubtitle](#chatroomsubtitle)       | Style configuration for the chatroom subtitle    |
| `chatroomDescription` | [ChatroomDescription](#chatroomdescription) | Style configuration for the chatroom description |
| `joinButton`          | [JoinButton](#joinbutton)                   | Style configuration for the join button          |
| `joinedButton`        | [JoinedButton](#joinedbutton)               | Style configuration for the joined button        |

### Header

| Property          | Type     | Description                     |
| ----------------- | -------- | ------------------------------- |
| `color`           | `string` | Color of the header text        |
| `fontSize`        | `number` | Font size of the header text    |
| `fontFamily`      | `string` | Font family of the header text  |
| `placeHolderText` | `string` | Placeholder text for the header |

### FilterHeader

| Property     | Type     | Description                           |
| ------------ | -------- | ------------------------------------- |
| `color`      | `string` | Color of the filter header text       |
| `fontSize`   | `number` | Font size of the filter header text   |
| `fontFamily` | `string` | Font family of the filter header text |

### ChatroomTitle

| Property     | Type     | Description                       |
| ------------ | -------- | --------------------------------- |
| `color`      | `string` | Color of the chatroom title       |
| `fontSize`   | `number` | Font size of the chatroom title   |
| `fontFamily` | `string` | Font family of the chatroom title |

### ChatroomSubtitle

| Property     | Type     | Description                          |
| ------------ | -------- | ------------------------------------ |
| `color`      | `string` | Color of the chatroom subtitle       |
| `fontSize`   | `number` | Font size of the chatroom subtitle   |
| `fontFamily` | `string` | Font family of the chatroom subtitle |

### ChatroomDescription

| Property     | Type     | Description                             |
| ------------ | -------- | --------------------------------------- |
| `color`      | `string` | Color of the chatroom description       |
| `fontSize`   | `number` | Font size of the chatroom description   |
| `fontFamily` | `string` | Font family of the chatroom description |

### JoinButton

| Property          | Type     | Description                          |
| ----------------- | -------- | ------------------------------------ |
| `placeHolderText` | `string` | Placeholder text for the join button |
| `color`           | `string` | Color of the join button text        |
| `fontSize`        | `number` | Font size of the join button text    |
| `fontFamily`      | `string` | Font family of the join button text  |
| `backgroundColor` | `string` | Background color of the join button  |
| `borderRadius`    | `string` | Border radius of the join button     |

### JoinedButton

| Property          | Type     | Description                            |
| ----------------- | -------- | -------------------------------------- |
| `placeHolderText` | `string` | Placeholder text for the joined button |
| `color`           | `string` | Color of the joined button text        |
| `fontSize`        | `number` | Font size of the joined button text    |
| `fontFamily`      | `string` | Font family of the joined button text  |
| `backgroundColor` | `string` | Background color of the joined button  |
| `borderRadius`    | `string` | Border radius of the joined button     |

## Props

| Property                | Type      | Description                                    |
| ----------------------- | --------- | ---------------------------------------------- |
| `avatar`                | `string`  | URL of the chatroom avatar                     |
| `header`                | `string`  | Header text for the chatroom                   |
| `title`                 | `string`  | Title of the chatroom                          |
| `lastMessage`           | `string`  | Last message sent in the chatroom              |
| `pinned`                | `boolean` | Indicates if the chatroom is pinned            |
| `isJoined`              | `boolean` | Indicates if the user has joined the chatroom  |
| `participants`          | `number`  | Number of participants in the chatroom         |
| `messageCount`          | `number`  | Total number of messages in the chatroom       |
| `externalSeen`          | `number`  | Number of messages seen externally             |
| `isSecret`              | `boolean` | Indicates if the chatroom is secret            |
| `chatroomID`            | `number`  | Unique identifier for the chatroom             |
| `filterState`           | `any`     | Current state of the filter                    |
| `navigation`            | `any`     | Navigation prop for navigating between screens |
| `participantsIconPath`  | `any`     | Path to the icon representing participants     |
| `totalMessagesIconPath` | `any`     | Path to the icon representing total messages   |
| `joinButtonPath`        | `any`     | Path to the join button icon                   |
| `joinedButtonPath`      | `any`     | Path to the joined button icon                 |
