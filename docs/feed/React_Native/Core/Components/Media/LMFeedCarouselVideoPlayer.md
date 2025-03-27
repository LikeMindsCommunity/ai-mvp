---
sidebar_position: 5
title: Carousel Video Player
slug: /react-native/core/components/media/carousel-video-player
---

## Overview

`LMVideoPlayer` is a component that provides a customizable video player for rendering and managing video playback. It supports various controls such as play, pause, fullscreen, and seeks functionalities, offering a seamless video viewing experience within the app.

<img
src={require('../../../../../static/img/reactNative/mediaLMCarouselVideoPlayer.webp').default}
alt="LMFeedPostContent"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="30%"
/>

## Customisation

The `STYLES` class allows you to customize the appearance of the `LMPostContent`. You can set the styles in `carouselScreenStyle` in `STYLES`.

| Property                | Type         | Description                                     |
| ----------------------- | ------------ | ----------------------------------------------- |
| `headerTitle`           | `TextStyle`  | Style for the video player's header title.      |
| `headerSubtitle`        | `TextStyle`  | Style for the video player's header subtitle.   |
| `sliderThumbImage`      | `string`     | Path to the image used for the slider thumb.    |
| `thumbTintColor`        | `string`     | Tint color for the slider thumb.                |
| `minimumTrackTintColor` | `string`     | Tint color for the minimum track of the slider. |
| `maximumTrackTintColor` | `string`     | Tint color for the maximum track of the slider. |
| `startTimeStyle`        | `TextStyle`  | Style for the video's start time text.          |
| `endTimeStyle`          | `TextStyle`  | Style for the video's end time text.            |
| `backIconPath`          | `string`     | Path to the image used for the back icon.       |
| `isBackIconLocalPath`   | `boolean`    | Whether the back icon path is a local path.     |
| `backIconStyle`         | `ImageStyle` | Style for the back icon.                        |
| `playIconPath`          | `string`     | Path to the image used for the play icon.       |
| `isPlayIconLocalPath`   | `boolean`    | Whether the play icon path is a local path.     |
| `playIconStyle`         | `ImageStyle` | Style for the play icon.                        |
| `pauseIconPath`         | `string`     | Path to the image used for the pause icon.      |
| `isPauseIconLocalPath`  | `boolean`    | Whether the pause icon path is a local path.    |
| `pauseIconStyle`        | `ImageStyle` | Style for the pause icon.                       |
| `muteIconPath`          | `string`     | Path to the image used for the mute icon.       |
| `isMuteIconLocalPath`   | `boolean`    | Whether the mute icon path is a local path.     |
| `muteIconStyle`         | `ImageStyle` | Style for the mute icon.                        |
| `unmuteIconPath`        | `string`     | Path to the image used for the unmute icon.     |
| `isUnmuteIconLocalPath` | `boolean`    | Whether the unmute icon path is a local path.   |
| `unmuteIconStyle`       | `ImageStyle` | Style for the unmute icon.                      |
