---
sidebar_position: 3
title: Chat TextView
slug: /react-native/core/fundamentals/text-view
---

## Overview

`LMChatTextView` serves as a UI component designed for the purpose of rendering texts within a chat interface.

<img
src={require('../../../../../static/img/reactNative/lmTextView.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## Customisation/Props

The `LMChatTextView` component requires certain props, some of which are mandatory, while others are optional. Here is a breakdown of the available props along with their types:

| Parameter    | Type      | Description                                         | Optional           |
| ------------ | --------- | --------------------------------------------------- | ------------------ |
| maxLines     | number    | Defines the maximum lines to be displayed           | :heavy_check_mark: |
| textStyle    | TextStyle | Represents the style of the text                    | :heavy_check_mark: |
| selectable   | boolean   | Represents the selection behavior of the text       | :heavy_check_mark: |
| onTextLayout | Function  | Callback function executed on change of text layout | :heavy_check_mark: |
