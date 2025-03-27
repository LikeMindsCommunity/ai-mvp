---
sidebar_position: 1
title: Post View Data Model
slug: /react-native/core/models/post-view-data-model
---

## LMPostViewData

| **VARIABLE**    | **TYPE**                                              | **DESCRIPTION**                                 | **OPTIONAL**       |
| --------------- | ----------------------------------------------------- | ----------------------------------------------- | ------------------ |
| `id`            | `string`                                              | Unique identifier for the post                  |                    |
| `attachments`   | [`LMAttachmentViewData[]`](./LMAttachmentViewData.md) | List of attachments related to the post         | :heavy_check_mark: |
| `commentsCount` | `number`                                              | Count of comments on the post                   |                    |
| `communityId`   | `number`                                              | Identifier for the community                    |                    |
| `createdAt`     | `number`                                              | Timestamp when the post was created             |                    |
| `isEdited`      | `boolean`                                             | Indicates if the post has been edited           |                    |
| `isLiked`       | `boolean`                                             | Indicates if the post is liked by the user      |                    |
| `isPinned`      | `boolean`                                             | Indicates if the post is pinned                 |                    |
| `isSaved`       | `boolean`                                             | Indicates if the post is saved                  |                    |
| `likesCount`    | `number`                                              | Count of likes on the post                      |                    |
| `menuItems`     | [`LMMenuItemsViewData[]`](./LMMenuItemsViewData.md)   | Menu items associated with the post             |                    |
| `replies`       | [`LMCommentViewData[]`](./LMCommentViewData.md)       | List of replies to the post                     | :heavy_check_mark: |
| `text`          | `string`                                              | Content of the post                             |                    |
| `updatedAt`     | `number`                                              | Timestamp when the post was last updated        |                    |
| `userId`        | `string`                                              | Identifier for the user who created the post    |                    |
| `uuid`          | `string`                                              | Universal unique identifier for the post        |                    |
| `user`          | [`LMUserViewData`](./LMUserViewData.md)               | User details of the person who created the post |                    |
| `topics`        | `string[]`                                            | List of topics associated with the post         | :heavy_check_mark: |
| `users`         | `string,`[`LMUserViewData`](./LMUserViewData.md)      | Map of users interacting with the post          |                    |
