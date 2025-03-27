---
title: Post
sidebar_position: 2
slug: /react-native/data/models/post-model
---

| **VARIABLE**    | **TYPE**                                | **DESCRIPTION**                                           | **OPTIONAL** |
| :-------------- | :-------------------------------------- | :-------------------------------------------------------- | :----------: |
| `id`            | String                                  | Unique ID of the post.                                    |              |
| `text`          | String                                  | Text content of the post.                                 |              |
| `attachments`   | [Attachment](#attachment)[]             | List of attached medias in the post. Maximum size is 10.  |      ✔       |
| `communityId`   | Int                                     | Unique ID of the community.                               |              |
| `isLiked`       | Bool                                    | `true` if the user has liked the post, `false` otherwise. |              |
| `isEdited`      | Bool                                    | `true` if the post was edited, `false` otherwise.         |              |
| `isPinned`      | Bool                                    | `true` if the post is pinned, `false` otherwise.          |              |
| `userId`        | String                                  | Unique ID of post creator.                                |
| `uuid`          | String                                  | Unique ID of post creator. creator.                       |              |
| `likesCount`    | Int                                     | Number of users that liked the post.                      |              |
| `commentsCount` | Int                                     | Number of users that commented on the post.               |              |
| `isSaved`       | Bool                                    | `true` if the user has saved the post, `false` otherwise. |              |
| `menuItems`     | [MenuItem](#menuitem)[]                 | List of actions as menu items on the post.                |              |
| `replies`       | [Comment](../Models/comment-model.md)[] | List of comments on the post.                             |      ✔       |
| `createdAt`     | Int                                     | Timestamp when the post was created.                      |              |
| `updatedAt`     | Int                                     | Timestamp when the post was last updated.                 |              |
| `heading`       | String                                  | Heading of the post.                                      |      ✔       |
| `tempId`        | String                                  | Temporary ID of post.                                     |      ✔       |
| `topicIds`      | String[]                                | List of ids of the topics added in the post.              |      ✔       |
| `isAnonymous`   | boolean                                 | `true` if the post is anonymous, `false` otherwise.       |      ✔       |
| `isHidden`      | boolean                                 | `true` if the post is hidden                              |      ✔       |

### Attachment

| **VARIABLE**     | **TYPE**                          | **DESCRIPTION**                                                                                                              | **OPTIONAL** |
| :--------------- | :-------------------------------- | :--------------------------------------------------------------------------------------------------------------------------- | :----------: |
| `attachmentType` | Int                               | Type of attachment. <br/> 1 - Image <br/> 2 - Video <br/> 3 - Document <br/> 4 - Link <br/> 5 - Custom widget <br/> 6 - Poll |              |
| `attachmentMeta` | [AttachmentMeta](#attachmentmeta) | Download url of attachment.                                                                                                  |              |

### AttachmentMeta

| **VARIABLE**           | **TYPE**                                            | **DESCRIPTION**                                                                                | **OPTIONAL** |
| :--------------------- | :-------------------------------------------------- | :--------------------------------------------------------------------------------------------- | :----------: |
| `name`                 | String                                              | Name of the attachment.                                                                        |      ✔       |
| `url`                  | String                                              | Download url of attachment.                                                                    |      ✔       |
| `format`               | String                                              | Format of attachment (pdf, etc.).                                                              |      ✔       |
| `size`                 | Int                                                 | Size of attachment in bytes.                                                                   |      ✔       |
| `duration`             | Int                                                 | Duration of video attachment in seconds.                                                       |      ✔       |
| `pageCount`            | Int                                                 | Number of pages in pdf attachment.                                                             |      ✔       |
| `ogTags`               | [OGTags](#ogtags)                                   | OGTags for link type attachment.                                                               |              |
| `thumbnailUrl`         | String                                              | Thumbnail url for the attached media.                                                          |      ✔       |
| `coverImageUrl`        | String                                              | Cover Image url for the attached media.                                                        |      ✔       |
| `title`                | String                                              | Title for the attached media.                                                                  |      ✔       |
| `body`                 | String                                              | Body for the attached media.                                                                   |      ✔       |
| `pollQuestion`         | String                                              | Poll question for the attached media.                                                          |      ✔       |
| `expiryTime`           | Int                                                 | Expiry time for the attached media, in case of poll.                                           |      ✔       |
| `options`              | String[]                                            | Poll options for the attached media.                                                           |      ✔       |
| `multipleSelectState`  | [PollMultipleSelectState](#pollmultipleselectstate) | It determines that how many choices a participant can or must select to submit their response. |      ✔       |
| `pollType`             | [PollType](#polltype)                               | It determines when the poll results are revealed to participants.                              |      ✔       |
| `multipleSelectNumber` | Int                                                 | Number of selectable options for the attached media, in case of poll.                          |      ✔       |
| `isAnonymous`          | Boolean                                             | If the attached media has be be anonymous.                                                     |      ✔       |
| `allowAddOption`       | Boolean                                             | If an user can add options to the attached media, in case of poll.                             |      ✔       |
| `entityId`             | String                                              | Entity id for the attached media.                                                              |      ✔       |
| `meta`                 | Record<string, any>                                 | Meta data for the custom widget.                                                               |      ✔       |

### PollMultipleSelectState

| **VARIABLE**              | **TYPE**                                         | **DESCRIPTION**                            | **OPTIONAL** |
| :------------------------ | :----------------------------------------------- | :----------------------------------------- | :----------: |
| `PollMultipleSelectState` | [enum](#enum-values-for-pollmultipleselectstate) | Enum representing the poll selection state |              |

### Enum Values for `PollMultipleSelectState`

| **VALUE**  | **DESCRIPTION**                      |
| :--------- | :----------------------------------- |
| `EXACTLY`  | The selection must match exactly     |
| `AT_MAX`   | The selection can be up to a maximum |
| `AT_LEAST` | The selection must meet a minimum    |

### PollType

| **VARIABLE** | **TYPE**                          | **DESCRIPTION**                 | **OPTIONAL** |
| :----------- | :-------------------------------- | :------------------------------ | :----------: |
| `PollType`   | [enum](#enum-values-for-polltype) | Enum representing the poll type |              |

### Enum Values for `PollType`

| **VALUE**  | **DESCRIPTION**                        |
| :--------- | :------------------------------------- |
| `INSTANT`  | Poll results are available immediately |
| `DEFERRED` | Poll results are revealed later        |

### OGTags

| **VARIABLE**  | **TYPE** | **DESCRIPTION**   | **OPTIONAL** |
| :------------ | :------- | :---------------- | :----------: |
| `title`       | String   | Link title.       |      ✔       |
| `image`       | String   | Link image url.   |      ✔       |
| `description` | String   | Link description. |      ✔       |
| `url`         | String   | Link url.         |      ✔       |

### MenuItem

| **VARIABLE** | **TYPE** | **DESCRIPTION**         | **OPTIONAL** |
| :----------- | :------- | :---------------------- | :----------: |
| `id`         | Int      | ID of the menu item.    |              |
| `title`      | String   | Title of the menu item. |              |

### Widget

| Variable           | Type            | Description                     | Optional           |
| ------------------ | --------------- | ------------------------------- | ------------------ |
| `id`               | string          | Id of the post.                 |                    |
| `lmMeta`           | Record<string,any> | LMMeta data of the post.        | :heavy_check_mark: |
| `createdAt`        | number            | Post creation date.             |                    |
| `metadata`         | Record<string,any> | Meta data of the post.          |                    |
| `parentEntityId`   | string          | Entity id of the parent post.   |                    |
| `parentEntityType` | string          | Entity type of the parent post. |                    |
| `updatedAt`        | number            | Post latest updation date.      |                    |

### FilteredComments

| **VARIABLE**    | **TYPE**                    | **DESCRIPTION**                                   | **OPTIONAL** |
| :-------------- | :-------------------------- | :------------------------------------------------ | :----------: |
| `id`            | string                      | Unique identifier for the feed item.              |              |
| `attachments`   | [Attachment[]](#attachment) | List of attachments associated with the post.     |      ✔       |
| `commentsCount` | number                      | Number of comments on the post.                   |              |
| `communityId`   | number                      | Identifier for the community of the post.         |              |
| `createdAt`     | number                      | Timestamp indicating when the post was created.   |              |
| `isEdited`      | boolean                     | Flag indicating if the post was edited.           |      ✔       |
| `isLiked`       | boolean                     | Indicates if the user has liked the post.         |      ✔       |
| `level`         | number                      | Depth level or hierarchy of the post.             |              |
| `likesCount`    | number                      | Total number of likes on the post.                |              |
| `menuItems`     | [MenuItem[]](#menuitem)     | List of menu items or actions available.          |      ✔       |
| `postId`        | string                      | Unique identifier for the post.                   |              |
| `tempId`        | string \| null              | Temporary ID used during post creation.           |      ✔       |
| `text`          | string                      | Text content of the post.                         |              |
| `updatedAt`     | number                      | Timestamp indicating the last update of the post. |              |
| `userId`        | string                      | ID of the user who created the post.              |              |
| `uuid`          | string                      | Universal unique identifier for the post.         |              |
