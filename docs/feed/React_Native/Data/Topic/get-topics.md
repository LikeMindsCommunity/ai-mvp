---
sidebar_position: 1
title: Get Topics
slug: /react-native/data/topic/get-topics
---

The LikeMinds ReactNative Feed SDK offers a fundamental function for enhanced community engagement—categorizing posts and discussions into topics. This feature empowers users by providing easy access to a comprehensive list of topics within the community, fostering organized and insightful interactions, making the platform a hub for focused and meaningful discussions. This function allows fetching a list of all topics in the community.

## Steps to get topics

1. Use the `getTopics()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `GetTopicRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
try {
  const GetTopicRequest = GetTopicRequest.builder()
    .setIsEnabled(true) // whether to fetch enabled/disabled or all topics
    .setPage(1) // page number for paginated data
    .setPageSize(10) // page size for paginated data
    .setSearch("<SEARCH_STRING>") // text to search the topics
    .setSearchType("name") // type of search
    .setParentIds("[<LIST_OF_IDs>]") // list of parent Ids
    .setOrderBy([
      "number_of_posts_desc",
      "updated_at_desc",
      "alphabetically_desc",
      "priority_desc",
    ]) // list of value to specify the sorting order
    .build();

  const response = await lmFeedClient.getTopics(GetTopicRequest);
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

:::note
`isEnabled` key is nullable, if you want to fetch enabled topics send `isEnabled = true`. For disabled topics send `isEnabled = false` and to fetch all the existing topics send send `isEnabled = null`
:::

## Models

### GetTopicRequest

| **VARIABLE** | **TYPE** | **DESCRIPTION**                               | **OPTIONAL** |
| :----------- | :------- | :-------------------------------------------- | :----------: |
| isEnabled    | boolean  | Whether to fetch enabled/disables/all topics. |      ✔       |
| search       | string   | Input text to search topics.                  |      ✔       |
| searchType   | string   | Type of search.                               |      ✔       |
| page         | int      | Page number of paginated data.                |              |
| pageSize     | int      | Page size for paginated data.                 |              |
| parentIds    | string[] | List of parent Ids                            |      ✔       |
| orderBy      | string[] | List of value to specify the sorting order    |      ✔       |

### GetTopicResponse

| **VARIABLE**  | **TYPE**                                                  | **DESCRIPTION**                       | **OPTIONAL** |
| :------------ | :-------------------------------------------------------- | :------------------------------------ | :----------: |
| `topics`      | [Topic](../Models/topic-model)[]                          | List of topics.                       |              |
| `childTopics` | Record<string, [Topic](../Models/topic-model.md)[] >      | Map of all the child topics.          |      ✔       |
| `widgets`     | Record<string, [Widget](../Models/post-model.md/#widget)> | Map of the widget data for the topic. |      ✔       |
