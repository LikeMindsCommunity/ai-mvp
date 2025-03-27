---
sidebar_position: 5
title: Post Poll
slug: /react-native/core/components/poll/post-poll
---

## Overview

`LMPostPollUI` is a component responsible for rendering the user interface of a poll within a post. It displays the poll question, available options, and allows users to vote on one or multiple choices, depending on the poll configuration. The component supports functionalities like displaying the total number of votes, handling user selections, and showing the poll's results in real-time or after submission.

<img
src={require('../../../../../static/img/Poll/PollDisplayView.webp').default}
alt="LMFeedCreatePollQuestionView"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="40%"
/>

## Callbacks

- `onSubmitButtonClicked`: Triggered when the submit button for the poll is clicked.
- `onAddPollOptionsClicked`: Triggered when the user clicks to add additional options to the poll.
- `onPollOptionClicked`: Triggered when a specific poll option is selected or clicked.
- `onPollEditClicked`: Triggered when the user clicks to edit the poll.
- `onPollClearClicked`: Triggered when the user clears or removes options from the poll.

## Customisation

The `STYLES` class allows you to customize the appearance of the `LMPostContent`. You can set the styles in `pollStyles` in `STYLES`.

| Property                             | Type                  | Description                                                            |
| ------------------------------------ | --------------------- | ---------------------------------------------------------------------- |
| `pollQuestionStyles`                 | `React.CSSProperties` | Style for the poll question text.                                      |
| `pollOptionSelectedColor`            | `string`              | Color for the selected poll option.                                    |
| `pollOptionOtherColor`               | `string`              | Color for the non-selected poll options.                               |
| `pollOptionSelectedTextStyles`       | `React.CSSProperties` | Style for the text of the selected poll option.                        |
| `pollOptionOtherTextStyles`          | `React.CSSProperties` | Style for the text of non-selected poll options.                       |
| `pollOptionEmptyTextStyles`          | `React.CSSProperties` | Style for the text when there are no poll options.                     |
| `pollOptionAddedByTextStyles`        | `React.CSSProperties` | Style for the text indicating who added a poll option.                 |
| `votesCountStyles`                   | `React.CSSProperties` | Style for the votes count display.                                     |
| `memberVotedCountStyles`             | `React.CSSProperties` | Style for the member voted count display.                              |
| `pollInfoStyles`                     | `React.CSSProperties` | Style for the poll information text.                                   |
| `submitButtonStyles`                 | `React.CSSProperties` | Style for the submit button.                                           |
| `submitButtonTextStyles`             | `React.CSSProperties` | Style for the submit button text.                                      |
| `allowAddPollOptionButtonStyles`     | `React.CSSProperties` | Style for the button that allows adding more poll options.             |
| `allowAddPollOptionButtonTextStyles` | `React.CSSProperties` | Style for the text on the button that allows adding more poll options. |
| `editPollOptionsStyles`              | `React.CSSProperties` | Style for the edit poll options UI elements.                           |
| `editPollOptionsIcon`                | `string`              | Path or URL to the icon used for editing poll options.                 |
| `clearPollOptionsStyles`             | `React.CSSProperties` | Style for the clear poll options UI elements.                          |
| `clearPollOptionsIcon`               | `string`              | Path or URL to the icon used for clearing poll options.                |
| `hidePoll`                           | `boolean`             | To hide and show poll                                                  |
