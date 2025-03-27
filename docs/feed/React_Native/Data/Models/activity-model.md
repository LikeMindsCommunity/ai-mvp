---
sidebar_position: 5
title: Activity
slug: /react-native/data/models/activity-model
---

| **VARIABLE**         | **TYPE**                                                                | **DESCRIPTION**                                                         | **OPTIONAL** |
| :------------------- | :---------------------------------------------------------------------- | :---------------------------------------------------------------------- | :----------: |
| `id`                 | String                                                                  | ID of the activity.                                                     |              |
| `action`             | Int                                                                     | Action that triggered this activity.                                    |              |
| `actionBy`           | String[]                                                                | List of unique ids of users whose actions are included in the activity. |              |
| `actionOn`           | String                                                                  | ID of the user for whom this activity is generated.                     |              |
| `activityText`       | String                                                                  | Text content for the activity.                                          |              |
| `createdAt`          | Int                                                                     | Timestamp when the activity was created.                                |              |
| `cta`                | String                                                                  | Call to action for the activity.                                        |              |
| `entityId`           | String                                                                  | ID of the entity for which activity is generated.                       |              |
| `entityOwnerId`      | String                                                                  | ID of the entity creator for which activity is generated.               |              |
| `entityType`         | Int                                                                     | Type of entity for which activity is generated.                         |              |
| `isRead`             | Bool                                                                    | True if the notification is read already, false otherwise.              |              |
| `updatedAt`          | Int                                                                     | Timestamp when the activity was last updated.                           |              |
| `activityEntityData` | [ActivityEntityData](../Models/activity-model.md/#activity-entity-data) | Data of the entity.                                                     |      ✔       |
| `uuid`               | String                                                                  | Unique ID of like creator.                                              |              |

### Activity Entity Data

| **VARIABLE**    | **TYPE**                                            | **DESCRIPTION**                                   | **OPTIONAL** |
| :-------------- | :-------------------------------------------------- | :------------------------------------------------ | :----------: |
| `id`            | String                                              | ID of the entity.                                 |              |
| `text`          | String                                              | Text content in the entity.                       |              |
| `deleteReason`  | String                                              | Reason for deletion of entity.                    |      ✔       |
| `deletedByUUID` | String                                              | ID of the user who delete the entity.             |      ✔       |
| `heading`       | String                                              | Heading for the entity                            |      ✔       |
| `attachments`   | [Attachment](../Models/post-model.md/#attachment)[] | List of attachments in the entity.                |      ✔       |
| `communityId`   | Int                                                 | ID of the community where the entity was created. |              |
| `isEdited`      | Bool                                                | True if the entity was edited, false otherwise.   |              |
| `isPinned`      | Bool                                                | True if entity was pinned false otherwise.        |      ✔       |
| `postId`        | String                                              | ID of the post related to the entity.             |      ✔       |
| `userId`        | String                                              | ID of the entity creator.                         |              |
| `replies`       | [Comment](../Models/comment-model.md)[]             | List of replies to the entity.                    |      ✔       |
| `level`         | Int                                                 | Level of comment if entity is a comment.          |      ✔       |
| `createdAt`     | Int                                                 | Timestamp when the entity was created.            |              |
| `updatedAt`     | Int                                                 | Timestamp when the entity was last updated.       |              |
| `uuid`          | String                                              | Unique ID of entity creator.                      |              |
