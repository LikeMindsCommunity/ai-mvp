---
sidebar_position: 5
title: User View Data Model
slug: /react-native/core/models/user-view-data-model
---

## LMUserViewData

| **VARIABLE**       | **TYPE**                                              | **DESCRIPTION**                                    | **OPTIONAL**       |
| ------------------ | ----------------------------------------------------- | -------------------------------------------------- | ------------------ |
| `id`               | `number`                                              | Unique identifier for the user                     |                    |
| `name`             | `string`                                              | Name of the user                                   |                    |
| `imageUrl`         | `string`                                              | URL of the user's profile image                    |                    |
| `userUniqueId`     | `string`                                              | Unique identifier for the user                     |                    |
| `sdkClientInfo`    | [`LMSDKClientInfoViewData`](#lmsdkclientinfoviewdata) | SDK client information for the user                |                    |
| `uuid`             | `string`                                              | Universal unique identifier for the user           |                    |
| `isGuest`          | `boolean`                                             | Indicates if the user is a guest                   |                    |
| `updatedAt`        | `number`                                              | Timestamp of the last update                       |                    |
| `customTitle`      | `string`                                              | Custom title assigned to the user                  |                    |
| `organisationName` | `string` or `null`                                    | Name of the organization or null if not applicable | :heavy_check_mark: |

## LMSDKClientInfoViewData

| **VARIABLE**   | **TYPE** | **DESCRIPTION**                            |
| -------------- | -------- | ------------------------------------------ |
| `community`    | `number` | Identifier for the community               |
| `user`         | `number` | Identifier for the user                    |
| `userUniqueId` | `string` | Unique identifier for the user             |
| `uuid`         | `string` | Universal unique identifier for the client |
