---
sidebar_position: 7
title: Post Content
slug: /react-native/core/components/post/post-content
---

## Overview

`LMPostContent` displays the main content of a post, including text, media, links, and polls.

<img
src={require('../../../../../static/img/reactNative/postContent.webp').default}
alt="LMFeedPostContent"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="30%"
/>

## Customisation

The `STYLES` class allows you to customize the appearance of the `LMPostContent`. You can set the styles in `postContent` inside of `postListStyle` in `STYLES`.

| Property               | Type                                                | Description                                                |
| ---------------------- | --------------------------------------------------- | ---------------------------------------------------------- |
| `textStyle`            | `TextStyle`                                         | Style applied to the main text content.                    |
| `visibleLines`         | `number`                                            | Number of visible lines before showing "Show More" option. |
| `showMoreText`         | [`LMTextProps`](../Fundamentals/LMFeedText.md)      | Props for the "Show More" text component.                  |
| `postContentViewStyle` | `ViewStyle`                                         | Style for the overall post content container.              |
| `postTopicStyle`       | `PostTopicStyle` | Object containing styles for topic text and its container. |

To see all the properties, visit [PostTopicStyle](https://github.com/LikeMindsCommunity/likeminds-feed-reactnative/blob/main/likeminds-feed-reactnative-integration/lmFeedProvider/types.ts)

### PostTopicStyle

| Property | Type        | Description                               |
| -------- | ----------- | ----------------------------------------- |
| `text`   | `TextStyle` | Style for the topic text.                 |
| `box`    | `ViewStyle` | Style for the container around the topic. |
