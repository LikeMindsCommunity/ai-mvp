---
title: Get Report Tags
sidebar_position: 1
slug: /react-native/data/moderation/get-report-tags
---

To perform moderation functionalities, like reporting a post, use the `getReportTags` function. It is used to fetch report tags for moderation.

## Steps to Get Report Tags

1. Use the `getReportTags()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `GetReportTagRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
try {
  const getReportTagRequest = GetReportTagRequest.builder()
    .setType(type) // type of report tags to fetch
    .build();
  const response = await lmFeedClient.getReportTags(getReportTagRequest);
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

## Models

### GetReportTagRequest

| **VARIABLE** | **TYPE** | **DESCRIPTION**              | **OPTIONAL** |
| :----------- | :------- | :--------------------------- | :----------: |
| `type`       | int      | Type of report tags to fetch |              |

### GetReportTagResponse

| **VARIABLE** | **TYPE**                                                     | **DESCRIPTION**     | **OPTIONAL** |
| :----------- | :----------------------------------------------------------- | :------------------ | :----------: |
| `reportTags` | [Report Tags](../Moderation/get-report-tags.md/#report-tags) | List of Report Tags |              |

### Report Tags

| **VARIABLE** | **TYPE** | **DESCRIPTION**     | **OPTIONAL** |
| :----------- | :------- | :------------------ | :----------: |
| `id`         | int      | Id for Report Tag   |              |
| `name`       | string   | Name for Report Tag |              |
