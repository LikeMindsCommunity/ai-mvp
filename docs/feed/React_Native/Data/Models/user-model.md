---
sidebar_position: 5
title: User
slug: /react-native/data/models/user-model
---

| **VARIABLE**       | **TYPE**                        | **DESCRIPTION**                                   | **OPTIONAL** |
| :----------------- | :------------------------------ | :------------------------------------------------ | :----------: |
| `id`               | Int                             | ID of the user in community.                      |              |
| `imageUrl`         | String                          | Download url of user image.                       |              |
| `isGuest`          | Bool                            | `true` if the user is a guest, `false` otherwise. |              |
| `name`             | String                          | Name of the user.                                 |              |
| `organisationName` | String                          | Name of the organisation.                         |      ✔       |
| `sdkClientInfo`    | [SDKClientInfo](#sdkclientinfo) | Client side info of user                          |      ✔       |
| `isDeleted`        | Bool                            | `true` if user is deleted, `false` otherwise.     |      ✔       |
| `customTitle`      | String                          | Custom title of the user.                         |      ✔       |
| `userUniqueId`     | String                          | Unique ID of user.                                |
| `uuid`             | String                          | Unique ID of user.                                |              |
| `updatedAt`        | Int                             | Timestamp when the user was last updated.         |              |

### SDKClientInfo

| **VARIABLE**   | **TYPE** | **DESCRIPTION**                | **OPTIONAL** |
| :------------- | :------- | :----------------------------- | :----------: |
| `community`    | Int      | ID of the community.           |              |
| `user`         | Int      | Download url of member image.  |              |
| `userUniqueId` | String   | Client side Unique ID of user. |              |
| `uuid`         | String   | Client side Unique ID of user. |              |
