---
sidebar_position: 3
title: Like Item View Data Model
slug: /react-native/core/models/like-item-view-data-model
---

## LMLikeItemViewData

| **VARIABLE** | **TYPE**                                         | **DESCRIPTION**                         |
| ------------ | ------------------------------------------------ | --------------------------------------- |
| `likes`      | [`LMLikeViewData[]`](#lmlikeviewdata)            | Array of likes associated with the item |
| `totalCount` | `number`                                         | Total number of likes                   |
| `users`      | `string,`[`LMUserViewData`](./LMUserViewData.md) | Mapping of user IDs to user information |

## LMLikeViewData

| **VARIABLE** | **TYPE**                                | **DESCRIPTION**                          |
| ------------ | --------------------------------------- | ---------------------------------------- |
| `id`         | `string`                                | Unique identifier for the like           |
| `createdAt`  | `number`                                | Timestamp when the like was created      |
| `updatedAt`  | `number`                                | Timestamp when the like was last updated |
| `userId`     | `string`                                | ID of the user who liked                 |
| `uuid`       | `string`                                | Universally unique identifier            |
| `user`       | [`LMUserViewData`](./LMUserViewData.md) | Object representing user details         |
