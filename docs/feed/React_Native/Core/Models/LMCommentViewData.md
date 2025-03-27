---
sidebar_position: 2
title: Comment View Data Model
slug: /react-native/core/models/comment-view-data-model
---

## LMCommentViewData

| **VARIABLE**             | **TYPE**                                            | **DESCRIPTION**                             | **OPTIONAL**       |
| ------------------------ | --------------------------------------------------- | ------------------------------------------- | ------------------ |
| `id`                     | `string`                                            | Unique identifier for the comment           |                    |
| `Id`                     | `string`                                            | Alternative identifier (optional)           | :heavy_check_mark: |
| `postId`                 | `string`                                            | ID of the associated post                   |                    |
| `isEdited`               | `boolean`                                           | Indicates if the comment has been edited    |                    |
| `isLiked`                | `boolean`                                           | Indicates if the comment is liked           |                    |
| `text`                   | `string`                                            | Content of the comment                      |                    |
| `userId`                 | `string`                                            | ID of the user who made the comment         |                    |
| `level`                  | `number`                                            | Depth level of the comment (for nesting)    |                    |
| `likesCount`             | `number`                                            | Number of likes the comment has received    |                    |
| `repliesCount`           | `number`                                            | Number of replies to the comment            |                    |
| `user`                   | [`LMUserViewData`](./LMUserViewData.md)             | User information of the comment creator     |                    |
| `updatedAt`              | `number`                                            | Timestamp of the last update                |                    |
| `createdAt`              | `number`                                            | Timestamp of when the comment was created   |                    |
| `menuItems`              | [`LMMenuItemsViewData[]`](./LMMenuItemsViewData.md) | Menu items associated with the comment      |                    |
| `replies`                | [`LMCommentViewData[]`](./LMCommentViewData.md)     | Replies to this comment                     | :heavy_check_mark: |
| `parentComment`          | [`LMCommentViewData`](./LMCommentViewData.md)       | Parent comment if this is a reply           | :heavy_check_mark: |
| `parentId`               | `string`                                            | ID of the parent comment                    | :heavy_check_mark: |
| `alreadySeenFullContent` | `boolean`                                           | Indicates if the full content has been seen | :heavy_check_mark: |
| `uuid`                   | `string`                                            | Unique identifier for the comment (UUID)    |                    |
| `tempId`                 | `string`                                            | Temporary ID for comment operations         | :heavy_check_mark: |
