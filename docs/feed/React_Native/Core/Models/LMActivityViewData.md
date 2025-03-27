---
sidebar_position: 11
title: Activity View Data Model
slug: /react-native/core/models/activity-view-data-model
---

## LMActivityViewData

| **VARIABLE**         | **TYPE**                                                | **DESCRIPTION**                                | **OPTIONAL**       |
| -------------------- | ------------------------------------------------------- | ---------------------------------------------- | ------------------ |
| `id`                 | `string`                                                | Unique identifier for the activity             |                    |
| `isRead`             | `boolean`                                               | Indicates if the activity has been read        |                    |
| `actionOn`           | `string`                                                | The type of action that occurred               |                    |
| `actionBy`           | `string[]`                                              | List of user IDs who performed the action      |                    |
| `entityType`         | `number`                                                | Type of the associated entity                  |                    |
| `entityId`           | `string`                                                | ID of the associated entity                    |                    |
| `entityOwnerId`      | `string`                                                | ID of the owner of the associated entity       |                    |
| `action`             | `number`                                                | Numerical representation of the action         |                    |
| `cta`                | `string`                                                | Call to action text                            |                    |
| `activityText`       | `string`                                                | Text describing the activity                   |                    |
| `activityEntityData` | [`LMActivityEntityViewData`](#lmactivityentityviewdata) | Additional data related to the activity entity | :heavy_check_mark: |
| `activityByUser`     | [`LMUserViewData`](./LMUserViewData.md)                 | User who performed the activity                |                    |
| `createdAt`          | `number`                                                | Timestamp when the activity was created        |                    |
| `updatedAt`          | `number`                                                | Timestamp when the activity was last updated   |                    |
| `uuid`               | `string`                                                | Unique universal identifier for the activity   |                    |

## LMActivityEntityViewData

| **VARIABLE**    | **TYPE**                                              | **DESCRIPTION**                                   | **OPTIONAL**       |
| --------------- | ----------------------------------------------------- | ------------------------------------------------- | ------------------ |
| `id`            | `string`                                              | Unique identifier for the activity entity         |                    |
| `text`          | `string`                                              | Text content of the activity entity               |                    |
| `deleteReason`  | `string`                                              | Reason for deletion                               | :heavy_check_mark: |
| `deletedBy`     | `string`                                              | Identifier for the user who deleted the entity    | :heavy_check_mark: |
| `heading`       | `string`                                              | Heading for the activity entity                   | :heavy_check_mark: |
| `attachments`   | [`LMAttachmentViewData[]`](./LMAttachmentViewData.md) | List of attachments associated with the entity    | :heavy_check_mark: |
| `communityId`   | `number`                                              | ID of the community to which the entity belongs   |                    |
| `isEdited`      | `boolean`                                             | Indicates if the activity entity has been edited  |                    |
| `isPinned`      | `boolean`                                             | Indicates if the activity entity is pinned        | :heavy_check_mark: |
| `userId`        | `string`                                              | ID of the user who created the entity             |                    |
| `user`          | [`LMUserViewData`](./LMUserViewData.md)               | User details of the creator                       |                    |
| `replies`       | [`LMCommentViewData[]`](./LMCommentViewData.md)       | List of replies (comments) on the activity entity | :heavy_check_mark: |
| `level`         | `number`                                              | Depth level of the entity in a thread             | :heavy_check_mark: |
| `createdAt`     | `number`                                              | Timestamp of when the entity was created          |                    |
| `updatedAt`     | `number`                                              | Timestamp of when the entity was last updated     |                    |
| `uuid`          | `string`                                              | Unique universal identifier for the entity        |                    |
| `deletedByUUID` | `string`                                              | UUID of the user who deleted the entity           | :heavy_check_mark: |
| `postId`        | `string`                                              | ID of the related post                            | :heavy_check_mark: |
