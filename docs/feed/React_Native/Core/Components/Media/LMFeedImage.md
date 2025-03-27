---
sidebar_position: 5
title: Image
slug: /react-native/core/components/media/image
---

## Overview

`LMImage` is a customizable image rendering component used to display images within the application. It provides flexibility for adjusting how images are displayed, including options for different resizing modes and additional props. This component supports common image sources such as URLs and local resources, making it versatile for displaying images in various contexts like posts, galleries, or carousels.

<img
src={require('../../../../../static/img/reactNative/mediaLMImage.webp').default}
alt="LMFeedPostContent"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="30%"
/>

## Callbacks

- `onCancel`: Callback to handle tap events trigerred by on clicking of the cancel button.

## Customisation

| Property       | Type                                                                                        | Description                                              |
| -------------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| `height`       | `number`                                                                                    | Height of the image.                                     |
| `width`        | `number`                                                                                    | Width of the image.                                      |
| `imageStyle`   | `ImageStyle`                                                                                | Style for the image.                                     |
| `boxFit`       | `center` or `contain` or `cover` or `repeat` or `stretch`                                   | Defines how the image should be fitted in the box.       |
| `boxStyle`     | `ViewStyle`                                                                                 | Style for the container (box) that holds the image.      |
| `aspectRatio`  | `0` or `0.1` or `0.2` or `0.3` or `0.4` or `0.5` or `0.6` or `0.7` or `0.8` or `0.9` or `1` | Aspect ratio of the image.                               |
| `loaderWidget` | `React.ReactNode`                                                                           | Custom loader widget to show while the image is loading. |
| `errorWidget`  | `React.ReactNode`                                                                           | Custom error widget to show if the image fails to load.  |
| `showCancel`   | `boolean`                                                                                   | Whether to show a cancel button for the image view.      |
| `cancelButton` | [`CancelButton`](./LMFeedImage.md#cancelbutton-object)                                      | Object to customize the cancel button (see table below). |

### `CancelButton` Object

| Property      | Type                                                          | Description                                          |
| ------------- | ------------------------------------------------------------- | ---------------------------------------------------- |
| `text`        | [`LMTextProps`](../Fundamentals/LMFeedText.md/#customisation) | Customization for the text in the cancel button.     |
| `icon`        | [`LMIconProps`](../Fundamentals/LMFeedIcon.md/#customisation) | Customization for the icon in the cancel button.     |
| `onTap`       | `Function`                                                    | Function triggered when the cancel button is tapped. |
| `placement`   | `start` or `end`                                              | Position of the icon or text in the cancel button.   |
| `buttonStyle` | `ViewStyle`                                                   | Style for the cancel button container.               |
| `isClickable` | `boolean`                                                     | Determines if the cancel button is clickable.        |
