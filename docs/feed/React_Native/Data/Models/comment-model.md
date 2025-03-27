---
sidebar_position: 3
title: Comment
slug: /react-native/data/models/comment-model
---

| **VARIABLE**    | **TYPE**                                        | **DESCRIPTION**                                              | **OPTIONAL** |
| :-------------- | :---------------------------------------------- | :----------------------------------------------------------- | :----------: |
| `id`            | String                                          | Unique ID of the comment.                                    |              |
| `text`          | String                                          | Text content of the comment.                                 |              |
| `level`         | Int                                             | Level is 0 for comment and 1 for reply.                      |              |
| `isLiked`       | Bool                                            | `true` if the user has liked the comment, `false` otherwise. |              |
| `isEdited`      | Bool                                            | `true` if the comment was edited, `false` otherwise.         |              |
| `userId`        | String                                          | Unique ID of comment creator.                                |
| `uuid`          | String                                          | Unique ID of comment creator.                                |              |
| `likesCount`    | Int                                             | Number of users that liked the comment.                      |              |
| `commentsCount` | Int                                             | Number of users that replied on the comment.                 |              |
| `replies`       | [Comment](../Models/comment-model.md)[]         | Replies on the comment.                                      |      ✔       |
| `parentComment` | [Comment](../Models/comment-model.md)[]         | Parent comment of the reply.                                 |      ✔       |
| `menuItems`     | [MenuItem](../Models/post-model.md/#menuitem)[] | List of actions as menu items on the comment.                |              |
| `createdAt`     | Int                                             | Timestamp when the comment was created.                      |              |
| `updatedAt`     | Int                                             | Timestamp when the comment was last updated.                 |              |
| `tempId`        | String                                          | Temporary ID of comment.                                     |      ✔       |
