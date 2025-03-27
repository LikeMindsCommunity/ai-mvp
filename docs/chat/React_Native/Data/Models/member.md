---
sidebar_position: 5
title: Member
slug: /react-native/data/models/member
---

List of parameters accessible in `Member` model

| Variable          | Type           | Description                               | Optional           |
| ----------------- | -------------- | ----------------------------------------- | ------------------ |
| `id`              | string         | User ID                                   |                    |
| `userUniqueId`    | string         | User's Unique ID                          |                    |
| `name`            | string         | User's Name                               |                    |
| `imageUrl`        | string         | User's Image URL                          | :heavy_check_mark: |
| `questionAnswers` | Question[]     | User's Question Answers                   | :heavy_check_mark: |
| `state`           | number         | User's State                              | :heavy_check_mark: |
| `isGuest`         | boolean        | Indicates if the user is a guest          |                    |
| `customIntroText` | string         | Custom Introduction Text                  | :heavy_check_mark: |
| `customClickText` | string         | Custom Click Text                         | :heavy_check_mark: |
| `memberSince`     | string         | User's Member Since Date                  | :heavy_check_mark: |
| `communityName`   | string         | Name of the Community                     | :heavy_check_mark: |
| `isOwner`         | boolean        | Indicates if the user is an owner         |                    |
| `customTitle`     | string         | Custom Title                              | :heavy_check_mark: |
| `menu`            | MemberAction[] | User's Menu Actions                       | :heavy_check_mark: |
| `communityId`     | number         | Community ID                              | :heavy_check_mark: |
| `chatroomId`      | number         | Chatroom ID                               | :heavy_check_mark: |
| `route`           | string         | User's Route                              | :heavy_check_mark: |
| `attendingStatus` | boolean        | Attending Status                          | :heavy_check_mark: |
| `hasProfileImage` | boolean        | Indicates if the user has a profile image |                    |
| `updatedAt`       | number         | Last Updated Timestamp                    | :heavy_check_mark: |
| `sdkClientInfo`   | SDKClientInfo  | SDK Client Information                    | :heavy_check_mark: |
| `uuid`            | string         | User's UUID                               |                    |

## Member Actions

List of parameters accessible in `MemberActions` model

| Variable | Type   | Description | Optional |
| -------- | ------ | ----------- | -------- |
| `title`  | string | Title       |          |
| `route`  | string | Route       |          |

### SDKClientInfo

List of parameters accessible in `SDKClientInfo` model

| Variable       | Type   | Description      | Optional           |
| -------------- | ------ | ---------------- | ------------------ |
| `user`         | string | User             |                    |
| `userUniqueId` | string | User's Unique ID |                    |
| `uuid`         | string | UUID             |                    |
| `communityId`  | number | Community ID     | :heavy_check_mark: |
| `community`    | number | Community        | :heavy_check_mark: |

### Question

List of parameters returned in `Question`

| Variable              | Type    | Description                             | Optional           |
| --------------------- | ------- | --------------------------------------- | ------------------ |
| `canAddOptions`       | boolean | Indicates if options can be added       |                    |
| `communityId`         | number  | Community ID                            | :heavy_check_mark: |
| `field`               | boolean | Field flag                              | :heavy_check_mark: |
| `helpText`            | string  | Help text                               | :heavy_check_mark: |
| `id`                  | number  | ID                                      | :heavy_check_mark: |
| `isAnswerEditable`    | boolean | Indicates if the answer is editable     |                    |
| `isCompulsory`        | boolean | Indicates if the question is compulsory | :heavy_check_mark: |
| `isHidden`            | boolean | Indicates if the question is hidden     | :heavy_check_mark: |
| `optional`            | boolean | Indicates if the question is optional   |                    |
| `questionTitle`       | string  | Title of the question                   |                    |
| `rank`                | number  | Rank of the question                    |                    |
| `state`               | number  | State of the question                   |                    |
| `tag`                 | null    | Tag (always null)                       |                    |
| `value`               | string  | Value                                   | :heavy_check_mark: |
| `memberId`            | string  | Member ID                               | :heavy_check_mark: |
| `directoryFields`     | boolean | Directory Fields flag                   | :heavy_check_mark: |
| `imageUrl`            | string  | Image URL                               | :heavy_check_mark: |
| `questionChangeState` | number  | Question Change State                   | :heavy_check_mark: |
