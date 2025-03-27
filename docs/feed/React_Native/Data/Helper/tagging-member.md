---
title: Tagging
sidebar_position: 1
slug: /react-native/data/helper/tagging
---

The getTaggingList function is used to fetch the tagging list, including group tags and user tags.

## Steps to get tagging list

1. Use the `getTaggingList()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `GetTaggingListRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
try {
  const getTaggingListRequest = GetTaggingListRequest.builder()
    .setSearchName("Hulk") // text to search the user
    .setPage(1) // page number for paginated data
    .setPageSize(20) // page size for paginated data
    .build();
  const response = await lmFeedClient.getTaggingList(getTaggingListRequest);
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

:::tip
Use a debounce operator on search input to reduce unnecessary or duplicate search requests triggered by rapidly changing input.
:::

## Models

### GetTaggingListRequest

| **VARIABLE** | **TYPE** | **DESCRIPTION**                       | **OPTIONAL** |
| :----------- | :------- | :------------------------------------ | :----------: |
| `searchName` | string   | Input text to search a member.        |              |
| `page`       | int      | Page number of paginated search data. |              |
| `pageSize`   | int      | Page size for paginated search data.  |              |

### GetTaggingListResponse

| **VARIABLE** | **TYPE**                              | **DESCRIPTION**      | **OPTIONAL** |
| :----------- | :------------------------------------ | :------------------- | :----------: |
| `members`    | List<[User](../Models/user-model.md)> | List of the members. |              |
