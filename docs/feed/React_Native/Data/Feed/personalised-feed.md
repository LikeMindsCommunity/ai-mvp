---
sidebar_position: 2
title: Get Personalised Feed
slug: /react-native/data/feed/personalised_feed
---

# Get Personalised Feed

The `getPersonalisedFeed()` function retrieves a personalized feed based on the provided request parameters.

## Steps to Get a Personalised Feed

1. Build a `getPersonalisedFeedRequest` object using the `GetPersonalisedFeedRequest` builder class.
2. Use the `getPersonalisedFeed()` function provided by the `lmFeedClient` object created earlier.
3. Use the response ([`LMResponse<GetPersonalisedFeed>`](../Models/response-wrapper.md)) as needed.

```tsx
import { GetPersonalisedFeedRequest } from "@likeminds.community/feed-rn";

try {
  const getPersonalisedFeedRequest = GetPersonalisedFeedRequest.builder()
    .setPage(payload.page)
    .setPageSize(payload.pageSize)
    .setShouldRecompute(page <= 1 ? true : false)
    .setShouldReorder(page <= 1 ? true : false)
    .build();
  const getPersonalisedFeedResponse = awaitlmFeedClient.getPersonalisedFeed(
    getPersonalisedFeedRequest
  );
} catch (error) {
  console.log(error);
}
```

## Models

### GetPersonalisedFeedRequest

The `GetPersonalisedFeedRequest` class represents a request to fetch a personalized feed.

List of parameters for the `GetPersonalisedFeedRequest` class:

| Variable          | Type    | Description                                           | Optional |
| ----------------- | ------- | ----------------------------------------------------- | -------- |
| `page`            | number  | The page number of the feed to retrieve.              |          |
| `pageSize`        | number  | The number of items per page.                         | &#10004; |
| `shouldRecompute` | boolean | Indicates whether the feed should be recomputed.      | &#10004; |
| `shouldReorder`   | boolean | Indicates whether the feed items should be reordered. | &#10004; |

### GetPersonalisedFeed

The `GetPersonalisedFeed` class represents the response of a personalized feed request.

List of parameters for the `GetPersonalisedFeed` class:

| Variable           | Type                                                  | Description                                        |
| ------------------ | ----------------------------------------------------- | -------------------------------------------------- |
| `posts`            | [Post](../Models/post-model.md)[]>                    | A list of posts included in the personalized feed. |
| `users`            | Record<string, [User](../Models/user-model.md)>       | A map of user IDs to user objects.                 |
| `topics`           | Record<string, [Topic](../Models/topic-model.md)>     | A map of topic IDs to topic objects.               |
| `widgets`          | Record<string, [Widget](../Models/post-model.md#widget)>   | A map of widget IDs to widget models.              |
| `filteredComments` | Record<string, [Comment](../Models/comment-model.md)> | A map of comment IDs to comment objects.           |
