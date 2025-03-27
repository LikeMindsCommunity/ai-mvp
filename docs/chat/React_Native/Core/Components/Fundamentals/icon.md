---
sidebar_position: 3
title: Chat Icon
slug: /react-native/core/fundamentals/icon
---

## Overview

`LMChatIcon` serves as a UI component designed for the purpose of rendering icons, including group icon, user icon and other icons within a chat interface.

<img
src={require('../../../../../static/img/reactNative/lmIcon.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## Customisation/Props

The `LMChatIcon` component requires certain props, some of which are mandatory, while others are optional. Here is a breakdown of the available props along with their types:

| Parameter | Type                                                      | Description                                         | Optional           |
| --------- | --------------------------------------------------------- | --------------------------------------------------- | ------------------ |
| iconUrl   | string                                                    | Represents the URL of the icon                      | :heavy_check_mark: |
| assetPath | object                                                    | Represents the path of the local image              | :heavy_check_mark: |
| color     | string                                                    | Represents the tint color of the icon               | :heavy_check_mark: |
| height    | number                                                    | Represents the height of the icon                   | :heavy_check_mark: |
| width     | number                                                    | Represents the width of the icon                    | :heavy_check_mark: |
| iconStyle | ImageStyle                                                | Represents the style of the icon                    | :heavy_check_mark: |
| boxFit    | "center" \| "contain" \| "cover" \| "repeat" \| "stretch" | Defines the fit behavior of the icon inside the box | :heavy_check_mark: |
| boxStyle  | ViewStyle                                                 | Represents the style of the view                    | :heavy_check_mark: |
