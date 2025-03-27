---
sidebar_position: 5
title: Carousel
slug: /react-native/core/components/media/carousel
---

## Overview

The `LMCarousel` component is designed to display a horizontal carousel of media items. It allows users to swipe through images or videos effortlessly. The component supports various media formats and provides customization options for pagination, autoplay, and item styling, enhancing the user experience in applications that showcase multimedia content.

<img
src={require('../../../../../static/img/reactNative/mediaCarousel.webp').default}
alt="LMFeedPostContent"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="30%"
/>

## Callbacks

- `onCancel`: Callback function triggered when the cancel button is clicked, receiving the index of the item.

## Customisation

| Property                 | Type                                                       | Description                                                                |
| ------------------------ | ---------------------------------------------------------- | -------------------------------------------------------------------------- |
| `carouselStyle`          | `ViewStyle`                                                | Style for the carousel container.                                          |
| `paginationBoxStyle`     | `ViewStyle`                                                | Style for the pagination box (where page indicators are shown).            |
| `activeIndicatorStyle`   | `ViewStyle`                                                | Style for the active page indicator (e.g., active dot in pagination).      |
| `inactiveIndicatorStyle` | `ViewStyle`                                                | Style for the inactive page indicator (e.g., inactive dots in pagination). |
| `showCancel`             | `boolean`                                                  | Whether to show the cancel button for the carousel.                        |
| `onCancel`               | `Function`                                                 | Function to execute when the cancel button is pressed.                     |
| `cancelButton`           | [`CancelButton`](./LMFeedCarousel.md/#cancelbutton-object) | Object to customize the cancel button's properties (see table below).      |

### `CancelButton` Object

| Property      | Type                                                          | Description                                          |
| ------------- | ------------------------------------------------------------- | ---------------------------------------------------- |
| `text`        | [`LMTextProps`](../Fundamentals/LMFeedText.md/#customisation) | Customization for the text in the cancel button.     |
| `icon`        | [`LMIconProps`](../Fundamentals/LMFeedIcon.md/#customisation) | Customization for the icon in the cancel button.     |
| `onTap`       | `Function`                                                    | Function triggered when the cancel button is tapped. |
| `placement`   | `start` or `end`                                              | Position of the icon or text in the cancel button.   |
| `buttonStyle` | `ViewStyle`                                                   | Style for the cancel button container.               |
| `isClickable` | `boolean`                                                     | Determines if the cancel button is clickable.        |
