---
sidebar_position: 7
title: Attachment View Data Model
slug: /react-native/core/models/attachment-view-data-model
---

## LMAttachmentViewData

| **VARIABLE**     | **TYPE**                                                | **DESCRIPTION**             | **OPTIONAL** |
| ---------------- | ------------------------------------------------------- | --------------------------- | ------------ |
| `attachmentMeta` | [`LMAttachmentMetaViewData`](#lmattachmentmetaviewdata) | Metadata for the attachment |              |
| `attachmentType` | `number`                                                | Type of the attachment      |              |

## LMAttachmentMetaViewData

| **VARIABLE**           | **TYPE**                                        | **DESCRIPTION**                                       | **OPTIONAL**       |
| ---------------------- | ----------------------------------------------- | ----------------------------------------------------- | ------------------ |
| `entityId`             | `string`                                        | ID of the associated entity                           | :heavy_check_mark: |
| `name`                 | `string`                                        | Name of the attachment                                | :heavy_check_mark: |
| `format`               | `string`                                        | Format of the attachment                              | :heavy_check_mark: |
| `size`                 | `number`                                        | Size of the attachment                                | :heavy_check_mark: |
| `duration`             | `number`                                        | Duration of the attachment (for video/audio files)    | :heavy_check_mark: |
| `pageCount`            | `number`                                        | Page count for documents                              | :heavy_check_mark: |
| `url`                  | `string`                                        | URL of the attachment                                 |                    |
| `thumbnailUrl`         | `string`                                        | URL for the thumbnail image                           | :heavy_check_mark: |
| `ogTags`               | [`LMOGTagsViewData`](#lmogtagsviewdata)         | Open Graph tags associated with the attachment        |                    |
| `coverImageUrl`        | `string`                                        | URL for the cover image                               | :heavy_check_mark: |
| `title`                | `string`                                        | Title of the attachment                               | :heavy_check_mark: |
| `body`                 | `string`                                        | Body content of the attachment                        | :heavy_check_mark: |
| `pollQuestion`         | `string`                                        | Question for a poll attachment                        | :heavy_check_mark: |
| `expiryTime`           | `number`                                        | Expiry time for the poll attachment                   | :heavy_check_mark: |
| `options`              | `string[]`                                      | Options for the poll                                  | :heavy_check_mark: |
| `multipleSelectState`  | [`PollMultiSelectState`](#pollmultiselectstate) | State for multiple selection in polls                 | :heavy_check_mark: |
| `pollType`             | [`PollType`](#polltype)                         | Type of poll (single/multiple choice)                 | :heavy_check_mark: |
| `multipleSelectNumber` | `number`                                        | Number of selections allowed in multiple select polls | :heavy_check_mark: |
| `isAnonymous`          | `boolean`                                       | Indicates if the poll is anonymous                    | :heavy_check_mark: |
| `allowAddOption`       | `boolean`                                       | Indicates if adding options is allowed                | :heavy_check_mark: |

## PollMultiSelectState

| **VARIABLE** | **TYPE**     | **DESCRIPTION**                                      |
| ------------ | ------------ | ---------------------------------------------------- |
| `EXACTLY`    | `"exactly"`  | Indicates the exact selection required.              |
| `AT_MAX`     | `"at_max"`   | Indicates the maximum number of selections allowed.  |
| `AT_LEAST`   | `"at_least"` | Indicates the minimum number of selections required. |

## PollType

| **VARIABLE** | **TYPE**     | **DESCRIPTION**                            |
| ------------ | ------------ | ------------------------------------------ |
| `INSTANT`    | `"instant"`  | Indicates that the selection is immediate. |
| `DEFERRED`   | `"deferred"` | Indicates that the selection is delayed.   |

## LMOGTagsViewData

| **VARIABLE**  | **TYPE** | **DESCRIPTION**                           | **OPTIONAL**       |
| ------------- | -------- | ----------------------------------------- | ------------------ |
| `description` | `string` | A brief description of the content        | :heavy_check_mark: |
| `title`       | `string` | The title of the content                  | :heavy_check_mark: |
| `url`         | `string` | The URL associated with the content       | :heavy_check_mark: |
| `image`       | `string` | The image URL associated with the content | :heavy_check_mark: |
