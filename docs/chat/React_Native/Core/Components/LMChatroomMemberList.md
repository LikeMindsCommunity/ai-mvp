---
sidebar_position: 7
title: Member List
slug: /react-native/core/components/members-list
---

## Overview

The `CommonAllMembers` component in this file is responsible for rendering the list of all members in a chatroom. It fetches and displays member details like their name and profile picture, typically for group chats or communities.

<img
src={require('../../../../static/img/reactNative/lmViewParticipants.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## Customisation

| Property                | Type                                | Description                             |
| ----------------------- | ----------------------------------- | --------------------------------------- |
| `userNameStyles`        | [UserNameStyles](#usernamestyles)   | Defines the style for the user's name.  |
| `userTitleStyles`       | [UserTitleStyles](#usertitlestyles) | Defines the style for the user's title. |
| `searchPlaceholderText` | string                              | Placeholder text for the search input.  |

### UserNameStyles

| Property     | Type   | Description                     |
| ------------ | ------ | ------------------------------- |
| `color`      | string | Color of the user's name text.  |
| `fontSize`   | number | Font size of the user's name.   |
| `fontFamily` | string | Font family of the user's name. |

### UserTitleStyles

| Property     | Type   | Description                      |
| ------------ | ------ | -------------------------------- |
| `color`      | string | Color of the user's title text.  |
| `fontSize`   | number | Font size of the user's title.   |
| `fontFamily` | string | Font family of the user's title. |

## Props

| Property       | Type    | Description                                     | Required           |
| -------------- | ------- | ----------------------------------------------- | ------------------ |
| `navigation`   | any     | Navigation object to handle screen transitions. | :heavy_check_mark: |
| `chatroomID`   | string  | Unique ID of the chatroom.                      | :heavy_check_mark: |
| `isDM`         | boolean | Indicates if the chatroom is a direct message.  | :heavy_check_mark: |
| `chatroomName` | string  | Name of the chatroom.                           |                    |
| `showList`     | boolean | Determines whether to display the list.         |                    |
