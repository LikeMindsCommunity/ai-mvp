---
sidebar_position: 3
title: Chat TextInput
slug: /react-native/core/fundamentals/text-input
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Overview

`LMChatTextInput` is a UI component specifically crafted to facilitate message input within a chat interface. It functions as an interactive input box, allowing users to seamlessly compose messages as part of their chat experience. Additionally, it supports features like tagging and media, enhancing user interaction by enabling users to mention others or share multimedia content within the chat.

<img
src={require('../../../../../static/img/reactNative/lmSimpleInputBox.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## Customisation/Props

The `LMChatTextInput` component requires certain props, some of which are mandatory, while others are optional. Here is a breakdown of the available props along with their types:

| Parameter            | Type                                             | Description                                                          | Optional           |
| -------------------- | ------------------------------------------------ | -------------------------------------------------------------------- | ------------------ |
| inputText            | string                                           | Represents the text to be displayed on the text input                |                    |
| onType               | (value: string) => void                          | Callback function called when the text input's text changes          |                    |
| partTypes            | `PartType[]`                                     | Array of part types                                                  | :heavy_check_mark: |
| inputRef             | `Ref<TextInput>`                                 | Reference to the text input component                                | :heavy_check_mark: |
| containerStyle       | `StyleProp<ViewStyle>`                           | Style for the container of the text input                            | :heavy_check_mark: |
| inputTextStyle       | TextStyle                                        | Style for the input text                                             | :heavy_check_mark: |
| placeholderText      | string                                           | Text to be displayed before any text is entered                      | :heavy_check_mark: |
| placeholderTextColor | string                                           | Color of the placeholder text                                        | :heavy_check_mark: |
| autoCapitalize       | "none" \| "sentences" \| "words" \| "characters" | Auto capitalization behavior of the input text                       | :heavy_check_mark: |
| keyboardType         | "default" \| "number-pad" \| "decimal-pad"       | Type of keyboard to be opened                                        | :heavy_check_mark: |
| plainTextStyle       | `StyleProp<TextStyle>`                           | Style for plain text (not placeholder or input text)                 | :heavy_check_mark: |
| multilineField       | boolean                                          | Indicates if the input text should be multi-lined or not             | :heavy_check_mark: |
| secureText           | boolean                                          | Indicates if the entered text should be hidden (e.g., for passwords) | :heavy_check_mark: |
| disabled             | boolean                                          | Indicates if the text input is editable or not                       | :heavy_check_mark: |
| autoFocus            | boolean                                          | Checks if the text input should be in focus by default               | :heavy_check_mark: |
