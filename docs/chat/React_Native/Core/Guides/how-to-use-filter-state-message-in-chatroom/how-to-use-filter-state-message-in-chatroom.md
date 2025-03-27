---
sidebar_position: 2
title: How to use Filter State Message in a Chatroom ?
slug: /react-native/core/guide/how-to-use-filter-state-message-in-chatroom
---

# How to use filter state message in Chatroom (React Native)

The LikeMinds Chat SDK provides flexibility to hide or show certain state messages in the chatroom for React Native applications. This guide will help you filter messages on the Chatroom screen.

---

### Enums For Conversation State

| **Enum**                       | **State** | **Type**                            | **Example**                                               |
| ------------------------------ | --------- | ----------------------------------- | --------------------------------------------------------- |
| `NORMAL`                       | 0         | Normal message                      | Hey                                                       |
| `FIRST_CONVERSATION`           | 1         | Chatroom first message              | Tony Stark started this chatroom                          |
| `MEMBER_JOINED_OPEN_CHATROOM`  | 2         | Member joins open chatroom          | Tony Stark joined this chatroom                           |
| `MEMBER_LEFT_OPEN_CHATROOM`    | 3         | Member leaves open chatroom         | Tony Stark left this chatroom                             |
| `MEMBER_ADDED_TO_CHATROOM`     | 7         | Member added in chatroom            | Nick Fury added Tony Stark                                |
| `MEMBER_LEFT_SECRET_CHATROOM`  | 8         | Member leaves secret chatroom       | Tony Stark left this chatroom                             |
| `MEMBER_REMOVED_FROM_CHATROOM` | 9         | Member is removed from a chatroom   | Nick Fury removed Tony Stark                              |
| `POLL`                         | 10        | Poll message                        | Nick Fury created a poll: "Who should lead the Avengers?" |
| `ALL_MEMBERS_ADDED`            | 11        | All members are added in a chatroom | Nick Fury added all members                               |
| `TOPIC_CHANGED`                | 12        | Chatroom topic changed              | Nick Fury changed current topic to "Hey"                  |

---
### Filtering Messages by State

You can filter out the messages you do not wish to show in the chatroom by specifying the states you want to hide. Follow these steps:

1. Create an array named `filterStateMessage`.
2. Add the state values you wish to hide.
3. Pass this array while creating the instance of the `lmChatClient`.

#### Code Example:

```tsx
import { ConversationState } from "@likeminds.community/chat-rn";
import { initiateLMClient } from "@likeminds.community/chat-rn-core";

// Define the conversation states to filter 
// Example Usage
const filterStateMessage = [
  ConversationState.MEMBER_JOINED_OPEN_CHATROOM,
  ConversationState.MEMBER_LEFT_OPEN_CHATROOM,
];

export const lmChatClient = initiateLMClient(filterStateMessage);
```
