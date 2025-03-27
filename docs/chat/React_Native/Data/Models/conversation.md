---
sidebar_position: 4
title: Conversation
slug: /react-native/data/models/conversation
---

List of parameters accessible in `Conversation` model

| Variable                  | Type         | Description                                                   | Optional           |
| ------------------------- | ------------ | ------------------------------------------------------------- | ------------------ |
| `id`                      | string       | Conversation ID                                               | :heavy_check_mark: |
| `chatroomId`              | string       | Chatroom ID                                                   | :heavy_check_mark: |
| `communityId`             | string       | Community ID                                                  |                    |
| `member`                  | Member       | Member object representing the participant                    |                    |
| `answer`                  | string       | Conversation answer                                           |                    |
| `createdAt`               | string       | Creation timestamp                                            | :heavy_check_mark: |
| `state`                   | number       | State of the conversation                                     |                    |
| `attachments`             | Attachment[] | List of attachments                                           | :heavy_check_mark: |
| `lastSeen`                | boolean      | Indicates if it was last seen                                 |                    |
| `ogTags`                  | LinkOGTags   | Open Graph Tags                                               | :heavy_check_mark: |
| `date`                    | string       | Date of the conversation                                      | :heavy_check_mark: |
| `isEdited`                | boolean      | Indicates if the conversation was edited                      |                    |
| `memberId`                | string       | Member ID                                                     | :heavy_check_mark: |
| `replyConversation`       | string       | ID of the reply conversation                                  | :heavy_check_mark: |
| `replyConversationId`     | string       | ID of the reply conversation                                  | :heavy_check_mark: |
| `lastUpdatedAt`           | number       | Last updated timestamp                                        |                    |
| `replyConversationObject` | Conversation | Reply conversation object                                     | :heavy_check_mark: |
| `deletedBy`               | string       | ID of the member who deleted the conversation                 |                    |
| `createdEpoch`            | number       | Creation epoch timestamp                                      |                    |
| `attachmentCount`         | number       | Number of attachments                                         | :heavy_check_mark: |
| `attachmentUploaded`      | boolean      | Indicates if attachments were uploaded                        |                    |
| `uploadWorkerUUID`        | string       | UUID of the upload worker                                     | :heavy_check_mark: |
| `temporaryId`             | string       | Temporary ID                                                  | :heavy_check_mark: |
| `localCreatedEpoch`       | number       | Local creation epoch timestamp                                | :heavy_check_mark: |
| `reactions`               | Reaction[]   | List of reactions                                             | :heavy_check_mark: |
| `isAnonymous`             | boolean      | Indicates if the conversation is anonymous                    |                    |
| `allowAddOption`          | boolean      | Indicates if adding options is allowed                        | :heavy_check_mark: |
| `pollType`                | number       | Poll type                                                     | :heavy_check_mark: |
| `pollTypeText`            | string       | Poll type text                                                | :heavy_check_mark: |
| `submitTypeText`          | string       | Submit type text                                              | :heavy_check_mark: |
| `expiryTime`              | number       | Expiry time                                                   | :heavy_check_mark: |
| `multipleSelectNo`        | number       | Number of multiple selects                                    | :heavy_check_mark: |
| `multipleSelectState`     | number       | Multiple select state                                         | :heavy_check_mark: |
| `polls`                   | Poll[]       | List of polls                                                 | :heavy_check_mark: |
| `toShowResults`           | boolean      | Indicates whether to show poll results                        | :heavy_check_mark: |
| `pollAnswerText`          | string       | Poll answer text                                              | :heavy_check_mark: |
| `replyChatroomId`         | string       | ID of the chatroom being replied to                           | :heavy_check_mark: |
| `replyId`                 | string       | Conversation ID of the conversation being responded to        | :heavy_check_mark: |
| `deviceId`                | string       | Device ID                                                     | :heavy_check_mark: |
| `hasFiles`                | boolean      | Indicates if there are attached files                         | :heavy_check_mark: |
| `hasReactions`            | boolean      | Indicates if there are reactions                              | :heavy_check_mark: |
| `lastUpdated`             | number       | Last updated timestamp                                        | :heavy_check_mark: |
| `deletedByMember`         | Member       | Member who deleted the conversation                           | :heavy_check_mark: |
| `deletedByUserId`         | string       | ID of the member who deleted the conversation                 | :heavy_check_mark: |
| `userId`                  | string       | User ID                                                       | :heavy_check_mark: |
| `cardId`                  | string       | Card ID                                                       | :heavy_check_mark: |
| `isInProgress`            | string       | Indicates that the conversation is actively being transmitted | :heavy_check_mark: |

### Link OG Tags

List of parameters accessible in `LinkOGTags` model

| Variable      | Type   | Description | Optional           |
| ------------- | ------ | ----------- | ------------------ |
| `title`       | string | Title       | :heavy_check_mark: |
| `image`       | string | Image       | :heavy_checkmark:  |
| `description` | string | Description | :heavy_check_mark: |
| `url`         | string | URL         | :heavy_check_mark: |

### Polls

List of parameters accessible in `Polls` model

| Variable     | Type    | Description                | Optional           |
| ------------ | ------- | -------------------------- | ------------------ |
| `id`         | string  | ID                         |                    |
| `text`       | string  | Text                       |                    |
| `isSelected` | boolean | Indicates if it's selected | :heavy_check_mark: |
| `percentage` | number  | Percentage                 | :heavy_check_mark: |
| `subText`    | string  | Subtext                    | :heavy_check_mark: |
| `noVotes`    | number  | Number of votes            | :heavy_check_mark: |
| `member`     | Member  | Member                     | :heavy_check_mark: |
| `userId`     | string  | User ID                    | :heavy_check_mark: |

### Reactions

List of parameters accessible in `Reactions` model

| Variable   | Type   | Description | Optional           |
| ---------- | ------ | ----------- | ------------------ |
| `member`   | Member | Member      | :heavy_check_mark: |
| `reaction` | string | Reaction    |                    |
