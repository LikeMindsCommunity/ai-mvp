---
sidebar_position: 7
title: Comment View
slug: /react-native/core/components/comment/comment-view
---

## Overview

`LMCommentItem` is designed to display detailed information about a comment for a feed post.

<img
src={require('../../../../static/img/PostWidget/comment/commentHeader.webp').default}
alt="LMFeedPostDetailCommentHeaderView"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
/>

## Callbacks

- `onTapViewMore`: Callback to load more replies. `page` of type number and `data` which is an array of [`LMCommentViewData`](../Models/LMCommentViewData.md) will be returned from this callback.
- `onTapReplies`: Callback to render initial list of replies. `data` which is an array of [`LMCommentViewData`](../Models/LMCommentViewData.md) and `commentIdOfReplies` os type `string` will be returned from this callback.
- `onCommentOverflowMenuClick`: Callback trigerred on click of menu icon & handles the position and visibility of the modal. `event` object and `commentId` of type `string` will be returned from this callback.

## Customisation

| Property                     | Type                                                          | Description                                                                              |
| ---------------------------- | ------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `likeIconButton`             | [`LMButtonProps`](../Components/Fundamentals/LMFeedButton.md) | Custom like icon button                                                                  |
| `likeTextButton`             | [`LMButtonProps`](../Components/Fundamentals/LMFeedButton.md) | Custom like text button                                                                  |
| `onTapViewMore`              | `Function`                                                    | Callback function to be executed on click of view more replies                           |
| `commentMaxLines`            | `number`                                                      | Maximum lines of comment to be shown                                                     |
| `menuIcon`                   | [`LMButtonProps`](../Components/Fundamentals/LMFeedButton.md) | Custom menu icon button                                                                  |
| `commentUserNameStyle`       | `TextStyle`                                                   | Custom style for user name text                                                          |
| `commentContentProps`        | [`LMTextProps`](../Components/Fundamentals/LMFeedText.md)     | Custom props for comment item                                                            |
| `showMoreProps`              | [`LMTextProps`](../Components/Fundamentals/LMFeedText.md)     | Custom props for see more text                                                           |
| `replyTextProps`             | [`LMButtonProps`](../Components/Fundamentals/LMFeedButton.md) | Custom props for reply text                                                              |
| `repliesCountTextStyle`      | `TextStyle`                                                   | Custom props for comment text count                                                      |
| `timeStampStyle`             | `TextStyle`                                                   | Custom props for time stamp text                                                         |
| `viewMoreRepliesProps`       | [`LMTextProps`](../Components/Fundamentals/LMFeedText.md)     | Custom props for View more text                                                          |
| `onTapReplies`               | `Function`                                                    | Custom callback to be executed on click of Replies text                                  |
| `isRepliesVisible`           | `boolean`                                                     | Boolean to decide whether replies will be visible or not                                 |
| `onCommentOverflowMenuClick` | `Function`                                                    | Custom callback on click of menu icon & handles the position and visibility of the modal |
| `hideThreeDotsMenu`          | `boolean`                                                     | Boolean to hide/show three dots                                                          |
