---
title: Post Report
sidebar_position: 2
slug: /react-native/data/moderation/post-report
---

Used to report a Post/Comment with appropriate reasons.

## Steps to Report a Post/Comment

1. Use the `report()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `PostReportRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
try {
  const postReportRequest = PostReportRequest.builder()
    .setEntityId(entityId) // entitiy id to be reported
    .setUuid(uuid) // uuid to be reported
    .setEntityType(entityType) // entitiy type to be reported
    .setTagId(tagId) // tagId for the post
    .setReason(reason) // optional reason
    .build();
  const response = await lmFeedClient.postReport(postReportRequest);
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

## Models

### PostReportRequest

| **VARIABLE** | **TYPE** | **DESCRIPTION**                   |    **OPTIONAL**    |
| :----------- | :------- | :-------------------------------- | :----------------: |
| `entityId`   | string   | Unique identifier for the entity  |                    |
| `uuid`       | string   | Universally unique identifier     |                    |
| `entityType` | number   | Type of the entity                |                    |
| `tagId`      | number   | Identifier for the associated tag |                    |
| `reason`     | string   | Reason or context for the entity  | :heavy_check_mark: |
