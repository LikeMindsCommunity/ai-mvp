---
sidebar_position: 3
title: Notification list
---

| Trigger name                         | Trigger Conditions                                                     | Notification Category | Notification Sub Category       | Message + CTA                                                                                                  | CTA Outcome                                                                        |
| ------------------------------------ | ---------------------------------------------------------------------- | --------------------- | ------------------------------- | -------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| User tagged                          | A member is tagged in a chat room                                      | Chatroom              | User Tagged                     | `user` tagged you! `chatroom name`: `message_text`                                                             | Relevant chat room                                                                 |
| User Reacted                         | A member reacts on a message                                           | Chatroom              | User Reacted                    | `user` reacted on your message with reaction                                                                   | Relevant chat room                                                                 |
| Response in followed chatroom        | A user chats in a followed chat room                                   | Chatroom              | User Responded                  | **`chatroom_name`** <br/>`user`: `message_text`                                                                | Relevant chat room                                                                 |
| A chat room pinned by the CM         | A chat room has been pinned on the community feed by a CM              | Chatroom              | Chatroom pinned by CM           | Chat room pinned! Your community manager `cm_first_name` has just pinned `chat_room_title` on everyone’s feed. | Chat room opened                                                                   |
| Topic in a chat room updated         | A chat room has been updated by either the CM or the chat room creator | Chatroom              | Topic updated                   | Topic updated! The topic of your followed chat room `chatroom_name` has just been updated.                     | Chat room opened with the current topic visible                                    |
| Secret Chat room (member)            | Secret chat room created                                               | Chatroom              | Member added to secret chatroom | Title: `community_name` You have been added to `chatroom_name`                                                 | Relevant chat room                                                                 |
| Secret Chat room (member)            | Member removed from secret chat room                                   | Chatroom              | Member Removed                  | Title: `community_name` <br/> You have been removed from `chatroom_name`                                       | Relevant chat room                                                                 |
| Secret Chat room (Community Manager) | Secret chat room created                                               | Chatroom              | Secret Chatroom Created         | Title: `community_name` user created a secret chat room                                                        | Relevant chat room                                                                 |
| Micro Poll                           | When Micro poll is posted                                              | Chatroom              | Micro poll created              | Title: Time to vote! <br/> Message: user started a poll in `chatroom_room_name` in `community_name`.           | CTAs: Vote (Opens poll room), Follow (Follows the chatroom and open the poll room) |

### Variable Description

| Variable             | Description                                                                              |
| -------------------- | ---------------------------------------------------------------------------------------- |
| `user`               | The username or name of the user who performed an action or was mentioned in the message |
| `chatroom_name`      | The name of the chatroom where the message or action took place                          |
| `message_text`       | The text content of a message                                                            |
| `reaction`           | The specific reaction used by a user on a message                                        |
| `event_room_name`    | The name of an event room or event being referred to                                     |
| `response_text`      | The text of a response or reply                                                          |
| `poll_room_name`     | The name or reference of a poll room                                                     |
| `poll_data`          | Data related to a poll, such as the available choices/options                            |
| `event_name`         | The name or title of an event                                                            |
| `community_name`     | The name of the community or group where the action or event occurs                      |
| `cm_first_name`      | The first name of the community manager who performed an action                          |
| `chat_room_title`    | The title or name of a chat room                                                         |
| `chat_text`          | The text content of a chat message                                                       |
| `chatroom_room_name` | The name of a chatroom or room where a poll or message was posted                        |

### Other relevant definitions

| Word | Definition                                                                              |
| ---- | --------------------------------------------------------------------------------------- |
| CTA  | Call-to-action, indicating a suggested action to be taken, such as accepting or viewing |
| CM   | Community Manager                                                                       |
