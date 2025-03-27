---
sidebar_position: 2
title: Member State
slug: /react-native/data/user/member-state
---

The `getMemberState` function is used to fetch the member state of the current user. It provides information about the user's status, creation timestamp, edit requirements, and more.

## Steps to Get Member State

1. Use the `getMemberState()` function provided by the `lmFeedClient` object created earlier.
2. Use the response as per your requirement

```js
try {
  const response = await lmFeedClient.getMemberState();
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

## Models

### GetMemberStateResponse

| **VARIABLE**   | **TYPE**                                                  | **DESCRIPTION**                                           | **OPTIONAL** |
| :------------- | :-------------------------------------------------------- | :-------------------------------------------------------- | :----------: |
| `createdAt`    | string                                                    | Timestamp of when the member state was created            |      ✔       |
| `editRequired` | boolean                                                   | Indicates if edit is required                             |      ✔       |
| `member`       | [User](../Models/user-model.md)                           | Details of the member                                     |      ✔       |
| `memberRights` | [MemberRight](../User/get-member-state.md/#member-rights) | Object of the community.                                  |      ✔       |
| `state`        | int                                                       | Member State                                              |      ✔       |
| `toolState`    | int                                                       | Logout response in case the user doesn't have the access. |      ✔       |

### Member Rights

| **VARIABLE** | **TYPE**                                                          | **DESCRIPTION**                       | **OPTIONAL** |
| :----------- | :---------------------------------------------------------------- | :------------------------------------ | :----------: |
| `id`         | boolean                                                           | Whether topic is enabled or disabled. |      ✔       |
| `isLocked`   | string                                                            | Input text to search topics.          |      ✔       |
| `isSelected` | string                                                            | Type of search.                       |      ✔       |
| `title`      | string                                                            | Title of Member Right                 |      ✔       |
| `subtitle`   | string                                                            | Subtitle of Member Right              |      ✔       |
| `state`      | [MemberRightState](../User/get-member-state.md/#memberrightstate) | State of Member Right                 |      ✔       |

### MemberRightState

```js
enum MemberRightsState {
    Unknown = -1,
    ModerateChatRooms = 0,
    ModerateMembers = 1,
    EditCommunityDetails = 2,
    ViewMemberContactInfo = 3,
    AddCommunityManager = 4,
    ModerateDMSetting = 5,
    ModerateFeedAndComment = 6
}
```
