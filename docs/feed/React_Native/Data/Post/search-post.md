---
sidebar_position: 2
title: Search Post
slug: /react-native/data/feed/search_post
---

# Get Searched Posts

The `searchPosts()` function retrieves a feed based on the provided search query parameters.

## Steps to Get Searched Posts

1. Build a `SearchPostsRequest` object using the `SearchPostsRequest` builder class.
2. Use the `searchPosts()` function provided by the `lmFeedClient` object created earlier.
3. Use the response ([`LMResponse<SearchPostResponse>`](../Models/response-wrapper.md)) as needed.

```tsx
import { SearchPostsRequest } from "@likeminds.community/feed-rn";

try {
  const getSearchedPostsRequest = SearchPostsRequest.builder()
    .setPage(1)
    .setPageSize(PAGE_SIZE)
    .setSearch("<SEARCH_QUERY>")
    .setSearchType("<SEARCH_TYPE>")
    .build();
  const getSearchedPostsResponse = await lmFeedClient.searchPosts(
    getSearchedPostsRequest
  );
} catch (error) {
  console.log(error);
}
```

## Models

### Search Type

| Search Type | Type     | Description                                   |
| ----------- | -------- | --------------------------------------------- |
| `text`      | `string` | Searches post based on the content in posts.  |
| `heading`   | `string` | Searches posts based on the heading of posts. |

### SearchPostsRequest

The `SearchPostsRequest` class represents a request to fetch posts that match the search query.

List of parameters for the `SearchPostsRequest` class:

| Variable     | Type    | Description                                           | Optional |
| ------------ | ------- | ----------------------------------------------------- | -------- |
| `page`       | number  | The page number of the feed to retrieve.              |          |
| `pageSize`   | number  | The number of items per page.                         | &#10004; |
| `search`     | boolean | The search query based on which posts will be fetched | &#10004; |
| `searchType` | string  | The criteria based on which posts will be fetched     | &#10004; |

### SearchPostResponse

The `SearchPostResponse` class represents the response of a `searchPosts` request.

List of parameters for the `SearchPostResponse` class:

| Variable           | Type                                                     | Description                                        |
| ------------------ | -------------------------------------------------------- | -------------------------------------------------- |
| `posts`            | [Post](../Models/post-model.md)[]>                       | A list of posts included in the personalized feed. |
| `users`            | Record<string, [User](../Models/user-model.md)>          | A map of user IDs to user objects.                 |
| `topics`           | Record<string, [Topic](../Models/topic-model.md)>        | A map of topic IDs to topic objects.               |
| `widgets`          | Record<string, [Widget](../Models/post-model.md#widget)> | A map of widget IDs to widget models.              |
| `filteredComments` | Record<string, [Comment](../Models/comment-model.md)>    | A map of comment IDs to comment objects.           |
