---
sidebar_position: 5
title: Create Poll
slug: /react-native/core/components/poll/create-poll
---

## Overview

`CreatePollUI` is a component used to render the user interface for creating a new poll. It provides customizable fields for entering the poll question, adding poll options, and setting poll preferences (like allowing multiple selections). The component handles user input and updates the poll data structure dynamically as the user interacts with it.

<img
src={require('../../../../../static/img/Poll/CreatePoll.webp').default}
alt="LMFeedLikeListScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## Callbacks

- `onPollExpiryTimeClicked`: Triggered when the user clicks to view or edit the poll's expiry time.
- `onAddOptionClicked`: Triggered when the user clicks to add a new option to the poll.
- `onPollOptionCleared`: Triggered when a poll option is removed, providing the `index` of the cleared option.
- `onPollCompleteClicked`: Triggered when the user marks the poll as complete.

## Customisation

The `STYLES` class allows you to customize the appearance of the `LMFeedCreatePoll`. You can set the styles in `createPollStyle` in `STYLES`.

| Property                             | Type                  | Description                                                   |
| ------------------------------------ | --------------------- | ------------------------------------------------------------- |
| `pollQuestionsStyle`                 | `React.CSSProperties` | Style for the poll questions.                                 |
| `pollOptionsStyle`                   | `React.CSSProperties` | Style for the poll options.                                   |
| `pollExpiryTimeStyle`                | `React.CSSProperties` | Style for the poll expiry time text.                          |
| `pollAdvancedOptionTextStyle`        | `React.CSSProperties` | Style for the text of advanced poll options.                  |
| `pollAdvancedOptionExpandIcon`       | `string`              | Path or URL to the icon used for expanding advanced options.  |
| `pollAdvancedOptionMinimiseIcon`     | `string`              | Path or URL to the icon used for minimizing advanced options. |
| `pollAdvanceOptionsSwitchThumbColor` | `string`              | Color of the switch thumb in advanced options.                |
| `pollAdvanceOptionsSwitchTrackColor` | `string`              | Color of the switch track in advanced options.                |
| `shouldHideSeparator`                | `boolean`             | To show and hide separator.                                   |
