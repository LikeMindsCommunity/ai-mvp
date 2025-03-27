---
sidebar_position: 7
title: Post Footer
slug: /react-native/core/components/post/post-footer
---

## Overview

`LMPostFooter` is responsible for rendering the footer section of a post, including interactive elements like likes, comments, and shares, providing a way for users to engage with the post.

<img
src={require('../../../../../static/img/PostWidget/postFooter.webp').default}
alt="LMFeedPostFooterView"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="30%" />

## Customisation

The `STYLES` class allows you to customize the appearance of the `LMPostContent`. You can set the styles in `footer` inside of `postListStyle` in `STYLES`.

| Property           | Type                                | Description                                   |
| ------------------ | ----------------------------------- | --------------------------------------------- |
| `showBookMarkIcon` | `boolean`                           | Determines whether to show the bookmark icon. |
| `showShareIcon`    | `boolean`                           | Determines whether to show the share icon.    |
| `saveButton`       | [`SaveButton`](#savebutton)         | Configuration for the save button.            |
| `shareButton`      | [`ShareButton`](#sharebutton)       | Configuration for the share button.           |
| `likeIconButton`   | [`LikeIconButton`](#likeiconbutton) | Configuration for the like icon button.       |
| `likeTextButton`   | [`LikeTextButton`](#liketextbutton) | Configuration for the like text button.       |
| `commentButton`    | [`CommentButton`](#commentbutton)   | Configuration for the comment button.         |
| `footerBoxStyle`   | `ViewStyle`                         | Style for the footer container.               |

### SaveButton

| Property      | Type                                           | Description                            |
| ------------- | ---------------------------------------------- | -------------------------------------- |
| `text`        | [`LMTextProps`](../Fundamentals/LMFeedText.md) | Text properties for the save button.   |
| `icon`        | [`LMIconProps`](../Fundamentals/LMFeedIcon.md) | Icon properties for the save button.   |
| `onTap`       | `Function`                                     | Callback function triggered on tap.    |
| `placement`   | `"start"` or `"end"`                           | Determines icon text placement.        |
| `activeIcon`  | [`LMIconProps`](../Fundamentals/LMFeedIcon.md) | Icon properties for the active state.  |
| `activeText`  | [`LMTextProps`](../Fundamentals/LMFeedText.md) | Text properties for the active state.  |
| `buttonStyle` | `ViewStyle`                                    | Style for the save button.             |
| `isClickable` | `boolean`                                      | Determines if the button is clickable. |

### ShareButton

| Property      | Type                                           | Description                            |
| ------------- | ---------------------------------------------- | -------------------------------------- |
| `text`        | [`LMTextProps`](../Fundamentals/LMFeedText.md) | Text properties for the share button.  |
| `icon`        | [`LMIconProps`](../Fundamentals/LMFeedIcon.md) | Icon properties for the share button.  |
| `onTap`       | `Function`                                     | Callback function triggered on tap.    |
| `placement`   | `"start"` or `"end"`                           | Determines icon text placement.        |
| `activeIcon`  | [`LMIconProps`](../Fundamentals/LMFeedIcon.md) | Icon properties for the active state.  |
| `activeText`  | [`LMTextProps`](../Fundamentals/LMFeedText.md) | Text properties for the active state.  |
| `buttonStyle` | `ViewStyle`                                    | Style for the share button.            |
| `isClickable` | `boolean`                                      | Determines if the button is clickable. |

### LikeIconButton

| Property      | Type                                           | Description                            |
| ------------- | ---------------------------------------------- | -------------------------------------- |
| `icon`        | [`LMIconProps`](../Fundamentals/LMFeedIcon.md) | Icon properties for the like button.   |
| `activeIcon`  | [`LMIconProps`](../Fundamentals/LMFeedIcon.md) | Icon properties for the active state.  |
| `onTap`       | `Function`                                     | Callback function triggered on tap.    |
| `buttonStyle` | `ViewStyle`                                    | Style for the like button.             |
| `isClickable` | `boolean`                                      | Determines if the button is clickable. |

### LikeTextButton

| Property      | Type        | Description                            |
| ------------- | ----------- | -------------------------------------- |
| `text`        | `TextStyle` | Style for the text in the like button. |
| `onTap`       | `Function`  | Callback function triggered on tap.    |
| `buttonStyle` | `ViewStyle` | Style for the like text button.        |
| `isClickable` | `boolean`   | Determines if the button is clickable. |

### CommentButton

| Property      | Type                                           | Description                               |
| ------------- | ---------------------------------------------- | ----------------------------------------- |
| `text`        | `TextStyle`                                    | Style for the text in the comment button. |
| `icon`        | [`LMIconProps`](../Fundamentals/LMFeedIcon.md) | Icon properties for the comment button.   |
| `onTap`       | `Function`                                     | Callback function triggered on tap.       |
| `placement`   | `"start"` or `"end"`                           | Determines icon text placement.           |
| `buttonStyle` | `ViewStyle`                                    | Style for the comment button.             |
| `isClickable` | `boolean`                                      | Determines if the button is clickable.    |
