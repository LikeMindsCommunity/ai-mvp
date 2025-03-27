---
sidebar_position: 5
title: Button
slug: /react-native/core/components/fundamentals/button
---

## Overview

`LMButton` is a customizable button component that supports text and icon display, with options to define actions, style, placement, and active/inactive states. It also allows for different content when the button is active and includes flexibility in design and interaction.

<img
src={require('../../../../../static/img/reactNative/fundamentalLMButton.webp').default}
alt="LMFeedPostContent"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="30%"
/>

## Callbacks

- `onTap`: Callback to handle tap events trigerred by on clicking on the button.

## Customisation

| Property      | Type                             | Description                                           | Required           |
| ------------- | -------------------------------- | ----------------------------------------------------- | ------------------ |
| `text`        | [`LMTextProps`](./LMFeedText.md) | Represents the text displayed on the button           |                    |
| `icon`        | [`LMIconProps`](./LMFeedIcon.md) | Represents the icon displayed on the button           |                    |
| `onTap`       | `Function`                       | Functionality executed when the button is clicked     | :heavy_check_mark: |
| `placement`   | `'start'` or `'end'`             | Placement of the icon on the button                   |                    |
| `isActive`    | `boolean`                        | Represents the active/inactive state of the button    |                    |
| `activeIcon`  | [`LMIconProps`](./LMFeedIcon.md) | Icon displayed when the button is in the active state |                    |
| `activeText`  | [`LMTextProps`](./LMFeedText.md) | Text displayed when the button is in the active state |                    |
| `buttonStyle` | `ViewStyle`                      | Style of the button                                   |                    |
| `isClickable` | `boolean`                        | Indicates if the button is clickable or disabled      |                    |
