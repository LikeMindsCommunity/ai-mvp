---
sidebar_position: 5
title: Icon
slug: /react-native/core/components/fundamentals/icon
---

## Overview

`LMIcon` is a customizable icon component that supports various styles and sizes, allowing the display of icons from different sources. It provides flexibility in rendering icons and integrates easily into user interfaces with configurable properties for appearance and functionality.

<img
src={require('../../../../../static/img/reactNative/fundamentalLMIcon.webp').default}
alt="LMFeedPostContent"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="30%"
/>

## Customisation

| Property    | Type                                                                | Description                                                      |
| ----------- | ------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `iconUrl`   | `string`                                                            | Represents the URL of the icon.                                  |
| `assetPath` | `Object`                                                            | Represents the path of the local image.                          |
| `color`     | `string`                                                            | Represents the tint color of the icon.                           |
| `height`    | `number`                                                            | Represents the height of the icon.                               |
| `width`     | `number`                                                            | Represents the width of the icon.                                |
| `iconStyle` | `ImageStyle`                                                        | Represents the style of the icon.                                |
| `boxFit`    | `'center'` or `'contain'` or `'cover'` or `'repeat'` or `'stretch'` | Defines the fit behavior of the icon inside the surrounding box. |
| `boxStyle`  | `ViewStyle`                                                         | Represents the style of the view.                                |
