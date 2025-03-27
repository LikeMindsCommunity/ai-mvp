---
sidebar_position: 7
title: Post Header
slug: /react-native/core/components/post/post-header
---

## Overview

`LMPostHeader` renders the header section of a post, displaying key information such as the author's name, profile picture, and the post's timestamp, providing context and identification for the post.

<img
src={require('../../../../../static/img/PostWidget/postHeader.webp').default}
alt="LMFeedPostHeaderView"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="40%"
/>

## Customisation

The `STYLES` class allows you to customize the appearance of the `LMPostContent`. You can set the styles in `header` inside of `postListStyle` in `STYLES`.

| Property               | Type                                           | Description                                        |
| ---------------------- | ---------------------------------------------- | -------------------------------------------------- |
| `profilePicture`       | [`ProfilePicture`](#profilepicture)            | Configuration for the profile picture display.     |
| `titleText`            | `TextStyle`                                    | Style for the title text.                          |
| `createdAt`            | `TextStyle`                                    | Style for the created at timestamp.                |
| `pinIcon`              | [`LMIconProps`](../Fundamentals/LMFeedIcon.md) | Icon properties for the pinned post indicator.     |
| `menuIcon`             | [`LMIconProps`](../Fundamentals/LMFeedIcon.md) | Icon properties for the menu icon.                 |
| `showMemberStateLabel` | `boolean`                                      | Determines whether to show the member state label. |
| `memberStateViewStyle` | `ViewStyle`                                    | Style for the member state label view.             |
| `memberStateTextStyle` | `TextStyle`                                    | Style for the member state label text.             |
| `postHeaderViewStyle`  | `ViewStyle`                                    | Style for the overall post header container.       |
| `showMenuIcon`         | `boolean`                                      | Determines whether to show the menu icon.          |
| `onTap`                | `Function`                                     | Callback function triggered on tapping the header. |
| `postMenu`             | [`PostMenu`](#postmenu)                        | Configuration for the post menu.                   |

### ProfilePicture

| Property               | Type         | Description                                                        |
| ---------------------- | ------------ | ------------------------------------------------------------------ |
| `fallbackTextStyle`    | `TextStyle`  | Style for the fallback text if the profile picture is unavailable. |
| `size`                 | `number`     | Size of the profile picture.                                       |
| `onTap`                | `Function`   | Callback function triggered on tapping the profile picture.        |
| `fallbackTextBoxStyle` | `ViewStyle`  | Style for the container of the fallback text.                      |
| `profilePictureStyle`  | `ImageStyle` | Style for the profile picture itself.                              |

### PostMenu

| Property            | Type        | Description                                       |
| ------------------- | ----------- | ------------------------------------------------- |
| `menuItemTextStyle` | `TextStyle` | Style for the text of menu items.                 |
| `menuViewStyle`     | `ViewStyle` | Style for the menu container.                     |
| `backdropColor`     | `string`    | Color of the backdrop when the menu is displayed. |
