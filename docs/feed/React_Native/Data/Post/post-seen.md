---
sidebar_position: 10
title: Post Seen
slug: /react-native/data/feed/post_seen
---

# Post Seen

The `postSeen()` function is used to mark a list of posts as seen.

## Steps to Post Seen

1. Build a `postSeenRequest` object using the `PostSeenRequest` builder class.
1. Use the `postSeen()` function provided by the `lmFeedClient` object created earlier.
1. Use the response ([`LMResponse<void>`](../Models/response-wrapper.md)) as needed.

```tsx
import { PostSeenRequest } from "@likeminds.community/feed-rn";

try {
  const postSeenRequest = PostSeenRequest.builder()
    .setPostIds(["post-id-1", "post-id-2", "post-id-3"])
    .build();
  const getPostSeenResponse = await lmFeedClient.postSeen(postSeenRequest);
} catch (error) {
  console.log(error);
}
```

## Models

### PostSeenRequest

The `PostSeenRequest` class represents a request to mark posts as seen.

List of parameters for the `PostSeenRequest` class:

| Variable      | Type           | Description                             | Optional |
| ------------- | -------------- | --------------------------------------- | -------- |
| `seenPostIDs` | `List<String>` | A list of post IDs that have been seen. |          |
