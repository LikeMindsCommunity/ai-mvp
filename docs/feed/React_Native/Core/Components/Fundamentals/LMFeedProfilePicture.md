---
sidebar_position: 5
title: Profile Picture
slug: /react-native/core/components/fundamentals/profile-picture
---

## Overview

The `LMProfilePicture` component is designed to display user profile pictures with customizable styling and behavior. It accepts properties such as `fallbackTextStyle`, `size`, and various styles for the profile picture itself. The component allows for a fallback option when the image fails to load, and it can trigger actions upon being tapped. This versatility makes it suitable for applications requiring user identification through profile images while maintaining a cohesive design across different interfaces.

<img
src={require('../../../../../static/img/reactNative/fundamentalLMProfilePicture.webp').default}
alt="LMFeedPostContent"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="30%"
/>

## Callbacks

- `onTap`: Callback to handle tap events trigerred by on clicking of the profile picture.

## Customisation

| Property               | Type                             | Description                                                              | Required           |
| ---------------------- | -------------------------------- | ------------------------------------------------------------------------ | ------------------ |
| `fallbackText`         | [`LMTextProps`](./LMFeedText.md) | This represents the text to show initials if image URL is not present    | :heavy_check_mark: |
| `imageUrl`             | `string`                         | This represents the URL of the image                                     |                    |
| `size`                 | `number`                         | This represents the circular size of the profile picture                 |                    |
| `onTap`                | `Function`                       | This represents the functionality to execute on click on profile picture |                    |
| `fallbackTextBoxStyle` | `ViewStyle`                      | This represents the initials view style which wraps the initials text    |                    |
| `profilePictureStyle`  | `ImageStyle`                     | This represents the profile picture image style                          |                    |
