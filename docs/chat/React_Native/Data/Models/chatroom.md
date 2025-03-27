---
sidebar_position: 3
title: Chatroom
slug: /react-native/data/models/chatroom
---

List of parameters accessible in `Chatroom` model

| Variable                     | Type         | Description                  | Optional           |
| ---------------------------- | ------------ | ---------------------------- | ------------------ |
| `member`                     | Member       | Member                       |                    |
| `id`                         | string       | Chatroom ID                  |                    |
| `title`                      | string       | Title                        |                    |
| `createdAt`                  | number       | Creation Timestamp           | :heavy_check_mark: |
| `answerText`                 | string       | Answer Text                  | :heavy_check_mark: |
| `state`                      | number       | Chatroom State               |                    |
| `unseenCount`                | number       | Unseen Count                 | :heavy_check_mark: |
| `shareUrl`                   | string       | Share URL                    | :heavy_check_mark: |
| `communityId`                | string       | Community ID                 | :heavy_check_mark: |
| `communityName`              | string       | Community Name               | :heavy_check_mark: |
| `type`                       | number       | Chatroom Type                | :heavy_check_mark: |
| `about`                      | string       | About                        | :heavy_check_mark: |
| `header`                     | string       | Header                       | :heavy_check_mark: |
| `showFollowTelescope`        | boolean      | Show Follow Telescope        |                    |
| `showFollowAutoTag`          | boolean      | Show Follow AutoTag          |                    |
| `cardCreationTime`           | string       | Card Creation Time           | :heavy_check_mark: |
| `participantsCount`          | string       | Participants Count           | :heavy_check_mark: |
| `totalResponseCount`         | string       | Total Response Count         | :heavy_check_mark: |
| `muteStatus`                 | boolean      | Mute Status                  |                    |
| `followStatus`               | boolean      | Follow Status                | :heavy_check_mark: |
| `hasBeenNamed`               | boolean      | Has Been Named               |                    |
| `hasReactions`               | boolean      | Has Reactions                | :heavy_check_mark: |
| `date`                       | string       | Date                         | :heavy_check_mark: |
| `isTagged`                   | boolean      | Is Tagged                    | :heavy_check_mark: |
| `isPending`                  | boolean      | Is Pending                   | :heavy_check_mark: |
| `isPrivateMember`            | boolean      | Is Private Member            | :heavy_check_mark: |
| `isPinned`                   | boolean      | Is Pinned                    | :heavy_check_mark: |
| `isDeleted`                  | boolean      | Is Deleted                   | :heavy_check_mark: |
| `userId`                     | string       | User ID                      | :heavy_check_mark: |
| `deletedBy`                  | string       | Deleted By                   | :heavy_check_mark: |
| `deletedByMember`            | Member       | Deleted By Member            | :heavy_check_mark: |
| `deletedByUserId`            | string       | Deleted By User ID           | :heavy_check_mark: |
| `updatedAt`                  | number       | Updated Timestamp            | :heavy_check_mark: |
| `lastSeenConversationId`     | string       | Last Seen Conversation ID    | :heavy_check_mark: |
| `lastConversationId`         | string       | Last Conversation ID         | :heavy_check_mark: |
| `dateEpoch`                  | number       | Date Epoch                   | :heavy_check_mark: |
| `isSecret`                   | boolean      | Is Secret                    | :heavy_check_mark: |
| `secretChatroomParticipants` | number[]     | Secret Chatroom Participants | :heavy_check_mark: |
| `secretChatroomLeft`         | boolean      | Secret Chatroom Left         | :heavy_check_mark: |
| `topicId`                    | string       | Topic ID                     | :heavy_check_mark: |
| `topic`                      | Conversation | Topic                        | :heavy_check_mark: |
| `autoFollowDone`             | boolean      | Auto Follow Done             | :heavy_check_mark: |
| `isEdited`                   | boolean      | Is Edited                    | :heavy_check_mark: |
| `access`                     | number       | Access                       | :heavy_check_mark: |
| `memberCanMessage`           | boolean      | Member Can Message           | :heavy_check_mark: |
| `chatroomWithUserId`         | number       | Chatroom With User ID        | :heavy_check_mark: |
| `chatroomWithUserName`       | string       | Chatroom With User Name      | :heavy_check_mark: |
| `chatroomWithUser`           | Member       | Chatroom With User           | :heavy_check_mark: |
| `cohorts`                    | Cohort[]     | Cohorts                      | :heavy_check_mark: |
| `externalSeen`               | boolean      | External Seen                | :heavy_check_mark: |
| `unreadConversationCount`    | number       | Unread Conversation Count    | :heavy_check_mark: |
| `chatroomImageUrl`           | string       | Chatroom Image URL           | :heavy_check_mark: |
| `accessWithoutSubscription`  | boolean      | Access Without Subscription  | :heavy_check_mark: |
| `totalAllResponseCount`      | string       | Total All Response Count     | :heavy_check_mark: |
| `isConversationStored`       | boolean      | Is Conversation Stored       | :heavy_check_mark: |
| `chatRequestState`           | number       | Chat Request State           | :heavy_check_mark: |
| `chatRequestedBy`            | Member       | Chat Requested By            | :heavy_check_mark: |
| `chatRequestCreatedAt`       | number       | Chat Request Created At      | :heavy_check_mark: |
| `chatRequestedById`          | number       | Chat Requested By ID         | :heavy_check_mark: |

### Chatroom Actions

List of parameters accessible in `ChatroomActions` model

| Variable | Type   | Description    | Optional |
| -------- | ------ | -------------- | -------- |
| `id`     | number | Chatroom Id    |          |
| `title`  | string | Chatroom Title |          |

### Cohort

List of parameters returned in `Cohort`

| Variable       | Type     | Description     | Optional           |
| -------------- | -------- | --------------- | ------------------ |
| `id`           | number   | Cohort ID       | :heavy_check_mark: |
| `totalMembers` | number   | Total Members   | :heavy_check_mark: |
| `name`         | string   | Name            | :heavy_check_mark: |
| `members`      | Member[] | List of Members | :heavy_check_mark: |
