---
sidebar_position: 5
title: Header
slug: /react-native/core/components/fundamentals/header
---

## Overview

`LMHeader` is used to display the header of a screen. It contains the left and right component within it which are completely customisable.

<img
src={require('../../../../../static/img/reactNative/fundamentalLMHeader.webp').default}
alt="LMFeedPostContent"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="30%"
/>

## Callbacks

- `onBackPress`: Callback to handle tap events trigerred by on clicking of the back icon.

## Customisation

| Property              | Type                                           | Description                                                   |
| --------------------- | ---------------------------------------------- | ------------------------------------------------------------- |
| `heading`             | `string`                                       | The heading of the header.                                    |
| `rightComponent`      | `ReactElement`                                 | The component to be rendered on the right-side of the header. |
| `showBackArrow`       | `boolean`                                      | Boolean to decide whether to show back icon or not.           |
| `onBackPress`         | `Function`                                     | The function to be triggered on back press.                   |
| `subHeading`          | `string`                                       | The sub-heading of the header.                                |
| `backIcon`            | [`LMIconProps`](../Fundamentals/LMFeedIcon.md) | The back icon to be rendered.                                 |
| `subHeadingTextStyle` | `TextStyle`                                    | The text-styling for sub-heading.                             |
| `headingTextStyle`    | `TextStyle`                                    | The text-styling for heading.                                 |
| `headingViewStyle`    | `ViewStyle`                                    | The view-styling for heading.                                 |
