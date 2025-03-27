---
sidebar_position: 6
title: Attachments
slug: /react-native/data/models/attachments
---

List of parameters accessible in `Attachment` model

| Variable                 | Type           | Description               | Optional           |
| ------------------------ | -------------- | ------------------------- | ------------------ |
| `id`                     | string         | ID                        | :heavy_check_mark: |
| `name`                   | string         | Name                      |                    |
| `url`                    | string         | URL                       |                    |
| `type`                   | string         | Type                      |                    |
| `index`                  | number         | Index                     | :heavy_check_mark: |
| `width`                  | number         | Width                     | :heavy_check_mark: |
| `height`                 | number         | Height                    | :heavy_check_mark: |
| `awsFolderPath`          | string         | AWS Folder Path           |                    |
| `localFilePath`          | string         | Local File Path           |                    |
| `thumbnailUrl`           | string         | Thumbnail URL             |                    |
| `thumbnailAWSFolderPath` | string         | Thumbnail AWS Folder Path |                    |
| `thumbnailLocalFilePath` | string         | Thumbnail Local File Path |                    |
| `meta`                   | AttachmentMeta | Attachment Metadata       |                    |
| `createdAt`              | number         | Creation Timestamp        |                    |
| `updatedAt`              | number         | Updated Timestamp         |                    |
| `fileUrl`                | string         | File URL                  |                    |

### Attachments Meta

List of parameters accessible in `AttachmentMeta` model

| Variable       | Type   | Description     | Optional           |
| -------------- | ------ | --------------- | ------------------ |
| `numberOfPage` | number | Number of Pages | :heavy_check_mark: |
| `size`         | number | Size            | :heavy_checkmark:  |
| `duration`     | number | Duration        | :heavy_check_mark: |
