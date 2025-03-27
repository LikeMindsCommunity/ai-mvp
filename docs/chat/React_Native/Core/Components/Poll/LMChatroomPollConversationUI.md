---
sidebar_position: 4
title: Poll Conversation UI
slug: /react-native/core/components/poll/poll-conversation-ui
---

## Overview

The `PollConversationUI` component renders the user interface for displaying and interacting with polls within chat conversations, allowing users to view poll questions, cast votes, and see real-time updates on poll statuses, all while ensuring an engaging and responsive experience in the LikeMinds chat application.

<img
src={require('../../../../../static/img/reactNative/lmPollConversationView.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## Customisations

The `PollConversationUI` can be customised using the [`chatBubbleStyles`](../Message/LMChatroomMessage.md/#customisations)

## Props

| Property                         | Type              | Description                                                  | Default | Required           |
| -------------------------------- | ----------------- | ------------------------------------------------------------ | ------- | ------------------ |
| `hue`                            | `number`          | (Optional) The hue value for color customization.            |         |                    |
| `text`                           | `string`          | The text displayed for the poll option.                      |         | :heavy_check_mark: |
| `votes`                          | `number`          | The number of votes received for this option.                | `0`     | :heavy_check_mark: |
| `optionArr`                      | [`Poll[]`](#poll) | Array of poll options.                                       |         | :heavy_check_mark: |
| `pollTypeText`                   | `string`          | The text describing the poll type.                           |         | :heavy_check_mark: |
| `submitTypeText`                 | `string`          | The text for the poll submission button.                     |         | :heavy_check_mark: |
| `addOptionInputField`            | `string`          | The current input value for adding a new option.             | `""`    | :heavy_check_mark: |
| `shouldShowSubmitPollButton`     | `boolean`         | Indicates whether the submit button should be shown.         | `false` | :heavy_check_mark: |
| `selectedPolls`                  | `number[]`        | Array of selected poll indices.                              |         | :heavy_check_mark: |
| `showSelected`                   | `boolean`         | Indicates if the selected options should be shown.           | `false` | :heavy_check_mark: |
| `allowAddOption`                 | `boolean`         | Controls whether users can add new options.                  | `true`  | :heavy_check_mark: |
| `shouldShowVotes`                | `boolean`         | Indicates if vote counts should be displayed.                | `true`  | :heavy_check_mark: |
| `hasPollEnded`                   | `boolean`         | Indicates if the poll has ended.                             | `false` | :heavy_check_mark: |
| `expiryTime`                     | `string`          | The expiration time for the poll.                            |         | :heavy_check_mark: |
| `toShowResults`                  | `boolean`         | Indicates if results should be displayed.                    | `false` | :heavy_check_mark: |
| `member`                         | `any`             | Information about the member participating in the poll.      |         | :heavy_check_mark: |
| `user`                           | `any`             | Information about the user interacting with the poll.        |         | :heavy_check_mark: |
| `isEdited`                       | `boolean`         | Indicates if the poll has been edited.                       | `false` | :heavy_check_mark: |
| `createdAt`                      | `string`          | Timestamp of when the poll was created.                      |         | :heavy_check_mark: |
| `pollAnswerText`                 | `string`          | The text for the poll answer.                                |         | :heavy_check_mark: |
| `isPollEnded`                    | `boolean`         | Indicates if the poll has ended.                             | `false` | :heavy_check_mark: |
| `isIncluded`                     | `boolean`         | Indicates if the poll is included in results.                | `true`  | :heavy_check_mark: |
| `multipleSelectNo`               | `any`             | (Optional) Number of multiple selections allowed.            |         |                    |
| `multipleSelectState`            | `number`          | Current state of multiple selections.                        | `0`     | :heavy_check_mark: |
| `showResultsButton`              | `boolean`         | Indicates if the results button should be shown.             | `true`  | :heavy_check_mark: |
| `pollType`                       | `number`          | The type of the poll (e.g., single-choice, multiple-choice). | `0`     | :heavy_check_mark: |
| `onNavigate`                     | `Function`        | Callback to navigate to a specified route.                   |         | :heavy_check_mark: |
| `setSelectedPollOptions`         | `Function`        | Callback to update the selected poll options.                |         | :heavy_check_mark: |
| `addPollOption`                  | `Function`        | Callback to add a new poll option.                           |         | :heavy_check_mark: |
| `submitPoll`                     | `Function`        | Callback to submit the poll.                                 |         | :heavy_check_mark: |
| `setShowSelected`                | `Function`        | Callback to set the visibility of selected options.          |         | :heavy_check_mark: |
| `setIsAddPollOptionModalVisible` | `Function`        | Callback to control the visibility of the add option modal.  |         | :heavy_check_mark: |
| `setAddOptionInputField`         | `Function`        | Callback to set the input field value for adding an option.  |         | :heavy_check_mark: |
| `openKeyboard`                   | `Function`        | Callback to open the keyboard on user interaction.           |         | :heavy_check_mark: |
| `longPressOpenKeyboard`          | `Function`        | Callback to open the keyboard on long press.                 |         | :heavy_check_mark: |
| `stringManipulation`             | `Function`        | Function to perform string manipulation.                     |         | :heavy_check_mark: |
| `resetShowResult`                | `Function`        | Callback to reset the display of poll results.               |         | :heavy_check_mark: |

### Poll

| Property     | Type      | Description                                | Default | Required           |
| ------------ | --------- | ------------------------------------------ | ------- | ------------------ |
| `id`         | `string`  | Unique identifier for the poll option.     |         | :heavy_check_mark: |
| `isSelected` | `boolean` | Indicates if the poll option is selected.  | `false` | :heavy_check_mark: |
| `percentage` | `number`  | The percentage of votes this option has.   | `0`     | :heavy_check_mark: |
| `noVotes`    | `number`  | The total number of votes for this option. | `0`     | :heavy_check_mark: |
