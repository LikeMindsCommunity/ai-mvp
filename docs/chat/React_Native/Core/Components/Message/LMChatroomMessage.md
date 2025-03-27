---
sidebar_position: 4
title: Message Bubble
slug: /react-native/core/components/message/message-bubble
---

## Overview

The `Messages` component in this file is responsible for rendering the list of chat messages within a chatroom. It handles message rendering, updates, and the layout for displaying user messages, media, and interactions like replies or reactions. The component likely manages message-related features like timestamps, avatars, and typing indicators.

<img
src={require('../../../../../static/img/reactNative/lmChatBubble.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## Callbacks

- `onTapToUndoProp`: Triggered when the user taps to undo an action. Executes the provided function when the undo action is performed.

## Customisations

| Property                            | Type                                                  | Description                                     |
| ----------------------------------- | ----------------------------------------------------- | ----------------------------------------------- |
| `borderRadius`                      | `number`                                              | Defines the border radius of message bubbles    |
| `sentMessageBackgroundColor`        | `string`                                              | Background color of sent messages               |
| `receivedMessageBackgroundColor`    | `string`                                              | Background color of received messages           |
| `selectedBackgroundColor`           | `string`                                              | Background color when a message is selected     |
| `selectedMessageBackgroundColor`    | `string`                                              | Background color of the selected message        |
| `textStyles`                        | [`TextStyles`](#textstyles)                           | Styles for message text                         |
| `linkTextColor`                     | `string`                                              | Color of the hyperlink text                     |
| `taggingTextColor`                  | `string`                                              | Color of the tagging text                       |
| `selectedMessagesBackgroundColor`   | `string`                                              | Background color for multiple selected messages |
| `stateMessagesTextStyles`           | [`StateMessagesTextStyles`](#statemessagestextstyles) | Styles for state messages text                  |
| `messageReceivedHeader`             | [`MessageReceivedHeader`](#messagereceivedheader)     | Styles for message received header              |
| `dateStateMessage`                  | [`DateStateMessage`](#datestatemessage)               | Styles for date state message text              |
| `playPauseBoxIcon`                  | [`PlayPauseBoxIcon`](#playpauseboxicon)               | Styles for play/pause icon box                  |
| `voiceNoteSlider`                   | [`VoiceNoteSlider`](#voicenoteslider)                 | Styles for voice note slider                    |
| `pollVoteSliderColor`               | [`PollVoteSliderColor`](#pollvoteslidercolor)         | Styles for poll vote slider                     |
| `imageVideoAttachmentsBorderRadius` | `number`                                              | Border radius for image/video attachments       |
| `retryButtonStyle`                  | [`retryButtonStyle`](#retrybuttonstyle)               | Styles for the retry button                     |

### TextStyles

| Property     | Type     | Description             |
| ------------ | -------- | ----------------------- |
| `fontSize`   | `number` | Font size of the text   |
| `fontStyle`  | `string` | Font style of the text  |
| `fontFamily` | `string` | Font family of the text |

### StateMessagesTextStyles

| Property          | Type     | Description                           |
| ----------------- | -------- | ------------------------------------- |
| `fontSize`        | `number` | Font size of the state message text   |
| `fontStyle`       | `string` | Font style of the state message text  |
| `fontFamily`      | `string` | Font family of the state message text |
| `color`           | `string` | Color of the state message text       |
| `backgroundColor` | `string` | Background color of the state message |

### MessageReceivedHeader

| Property                  | Type                                                  | Description                         |
| ------------------------- | ----------------------------------------------------- | ----------------------------------- |
| `senderNameStyles`        | [`SenderNameStyles`](#sendernamestyles)               | Styles for the sender's name        |
| `senderDesignationStyles` | [`SenderDesignationStyles`](#senderdesignationstyles) | Styles for the sender's designation |

#### SenderNameStyles

| Property     | Type     | Description                      |
| ------------ | -------- | -------------------------------- |
| `fontSize`   | `number` | Font size of the sender's name   |
| `fontFamily` | `string` | Font family of the sender's name |
| `color`      | `string` | Color of the sender's name       |

#### SenderDesignationStyles

| Property     | Type     | Description                             |
| ------------ | -------- | --------------------------------------- |
| `fontSize`   | `number` | Font size of the sender's designation   |
| `fontFamily` | `string` | Font family of the sender's designation |
| `color`      | `string` | Color of the sender's designation       |

### DateStateMessage

| Property          | Type     | Description                                |
| ----------------- | -------- | ------------------------------------------ |
| `fontSize`        | `number` | Font size of the date state message        |
| `fontFamily`      | `string` | Font family of the date state message      |
| `color`           | `string` | Color of the date state message            |
| `backgroundColor` | `string` | Background color of the date state message |

### PlayPauseBoxIcon

| Property          | Type     | Description                             |
| ----------------- | -------- | --------------------------------------- |
| `backgroundColor` | `string` | Background color of play/pause icon box |

### VoiceNoteSlider

| Property                | Type     | Description                              |
| ----------------------- | -------- | ---------------------------------------- |
| `minimumTrackTintColor` | `string` | Color of the minimum track of the slider |
| `thumbTintColor`        | `string` | Color of the thumb of the slider         |

### PollVoteSliderColor

| Property          | Type     | Description                              |
| ----------------- | -------- | ---------------------------------------- |
| `backgroundColor` | `string` | Background color of the poll vote slider |

### RetryButtonStyle

| Property    | Type        | Description                                |
| ----------- | ----------- | ------------------------------------------ |
| `textStyle` | `TextStyle` | Text size of the text to retry button text |
| `viewStyle` | `ViewStyle` | View style of the retry button             |

## Props

| Property          | Type       | Description                                              | Required           |
| ----------------- | ---------- | -------------------------------------------------------- | ------------------ |
| `item`            | `any`      | The data item being rendered.                            | :heavy_check_mark: |
| `index`           | `number`   | The index of the current item in the list.               | :heavy_check_mark: |
| `isStateIncluded` | `boolean`  | Indicates if the state is included for the current item. | :heavy_check_mark: |
| `isIncluded`      | `boolean`  | Indicates if the item is included.                       | :heavy_check_mark: |
| `onTapToUndoProp` | `Function` | Callback triggered when the user taps to undo an action. |                    |
