---
sidebar_position: 8
title: Member Item
slug: /react-native/core/member-item
---

## Overview

`LMMemberListItem` is used to display user information associated for a like list. It showcases the user's profile image and name, along with an optional custom title.

<img
src={require('../../../../static/img/iOS/components/likeComponent.webp').default}
alt="LMFeedNotificationView"
style={{border: '2px solid #d6d6d6'}}
/>

## Callbacks

- `onTap`: Callback to handle tap events. We return the user object from this callback.

## Customisation

| Property              | Type                                                              | Description                           | Required           |
| --------------------- | ----------------------------------------------------------------- | ------------------------------------- | ------------------ |
| `likes`               | [`LMLikeUI`](../Models/LMLikeItemViewData.md)                     | Props for a single item of the list.  | :heavy_check_mark: |
| `profilePictureProps` | [`LMProfilePictureProps`](./Fundamentals/LMFeedProfilePicture.md) | Props for profile picture.            |                    |
| `nameProps`           | [`LMTextProps`](./Fundamentals/LMFeedText.md)                     | Props for user name.                  |                    |
| `customTitleProps`    | [`LMTextProps`](./Fundamentals/LMFeedText.md)                     | Props for title of the user.          |                    |
| `boxStyle`            | `ViewStyle`                                                       | Props for the box styling of an item. |                    |
| `onTap`               | `Function`                                                        | Prop for onTap event.                 |                    |
