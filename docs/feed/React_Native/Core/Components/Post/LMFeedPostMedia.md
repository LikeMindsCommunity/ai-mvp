---
sidebar_position: 7
title: Post Media
slug: /react-native/core/components/post/post-media
---

## Overview

`LMPostMedia` is responsible for displaying media attachments such as images and videos within a post. It manages the layout, rendering, and interaction of the attached media, providing a rich multimedia experience for users.

<img
src={require('../../../../../static/img/reactNative/postMedia.webp').default}
alt="LMFeedPostContent"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="30%"
/>

## Customisation

The `STYLES` class allows you to customize the appearance of the `LMPostContent`. You can set the styles in `media` inside of `postListStyle` in `STYLES`.

| Property         | Type                                                                                    | Description                                   |
| ---------------- | --------------------------------------------------------------------------------------- | --------------------------------------------- |
| `postMediaStyle` | `ViewStyle`                                                                             | Style for the post media container.           |
| `image`          | [`LMImage`](../Media/LMFeedImage.md#customisation)                                      | Configuration for displaying images.          |
| `video`          | [`LMVideo`](../Media/LMFeedVideo.md#customisation)                   | Configuration for displaying videos.          |
| `carousel`       | [`LMCarousel`](../Media/LMFeedCarousel.md#customisation)      | Configuration for media carousel.             |
| `document`       | [`LMDocument`](../Media/LMFeedDocument.md#customisation)      | Configuration for displaying documents.       |
| `linkPreview`    | [`LMLinkPreview`](../Media/LMFeedLinkPreview.md#customisation) | Configuration for displaying link previews.   |
| `noPostView`     | `ViewStyle`                                                                             | Style for the view when no post is available. |
| `noPostText`     | `TextStyle`                                                                             | Style for the text when no post is available. |
| `listStyle`      | `ViewStyle`                                                                             | Style for the list of media items.            |
