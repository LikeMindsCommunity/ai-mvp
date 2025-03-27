---
sidebar_position: 5
title: Video
slug: /react-native/core/components/media/video
---

## Overview

The `LMVideo` component is designed to handle video playback within the application. It supports various video formats and provides controls for play, pause, and seeking, allowing users to interactively engage with video content.

<img
src={require('../../../../../static/img/reactNative/mediaLMVideo.webp').default}
alt="LMFeedPostContent"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="30%"
/>

## Callbacks

- `onCancel`: Callback to handle tap events trigerred by on clicking of the cancel button.

## Customisation

| Property       | Type                                                                                        | Description                                              |
| -------------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| `height`       | `number`                                                                                    | Height of the video.                                     |
| `width`        | `number`                                                                                    | Width of the video.                                      |
| `videoStyle`   | `ViewStyle`                                                                                 | Style for the video container.                           |
| `boxFit`       | `stretch` or `contain` or `cover` or `none`                                                 | Defines how the video should fit in the container.       |
| `boxStyle`     | `ViewStyle`                                                                                 | Style for the container (box) that holds the video.      |
| `aspectRatio`  | `0` or `0.1` or `0.2` or `0.3` or `0.4` or `0.5` or `0.6` or `0.7` or `0.8` or `0.9` or `1` | Aspect ratio of the video.                               |
| `showControls` | `boolean`                                                                                   | Whether to show the video controls.                      |
| `looping`      | `boolean`                                                                                   | Whether the video should loop.                           |
| `loaderWidget` | `React.ReactNode`                                                                           | Custom loader widget to show while the video is loading. |
| `errorWidget`  | `React.ReactNode`                                                                           | Custom error widget to show if the video fails to load.  |
| `playButton`   | `React.ReactNode`                                                                           | Custom play button to show for the video.                |
| `pauseButton`  | `React.ReactNode`                                                                           | Custom pause button to show for the video.               |
| `autoPlay`     | `boolean`                                                                                   | Whether the video should autoplay.                       |
| `showCancel`   | `boolean`                                                                                   | Whether to show a cancel button for the video view.      |
| `onCancel`     | `Function`                                                                                  | Function to execute when the cancel button is pressed.   |

### `CancelButton` Object

| Property      | Type                                                          | Description                                          |
| ------------- | ------------------------------------------------------------- | ---------------------------------------------------- |
| `text`        | [`LMTextProps`](../Fundamentals/LMFeedText.md/#customisation) | Customization for the text in the cancel button.     |
| `icon`        | [`LMIconProps`](../Fundamentals/LMFeedIcon.md/#customisation) | Customization for the icon in the cancel button.     |
| `onTap`       | `Function`                                                    | Function triggered when the cancel button is tapped. |
| `placement`   | `start` or `end`                                              | Position of the icon or text in the cancel button.   |
| `buttonStyle` | `ViewStyle`                                                   | Style for the cancel button container.               |
| `isClickable` | `boolean`                                                     | Determines if the cancel button is clickable.        |
