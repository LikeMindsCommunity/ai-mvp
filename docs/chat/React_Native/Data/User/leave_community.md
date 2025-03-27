---
sidebar_position: 4
title: Leave Community
slug: /react-native/data/user/leave-community
---

# Leave Community

The Leave Community method allows users to gracefully exit a community by handling the necessary backend processes, such as updating membership records and adjusting access permissions. This function ensures a smooth user experience while departing from a community, maintaining data integrity and security.

## Leaving a community

1. For an user to leave a community, use the `leaveCommunity()` method of the client you initialised.
2. Pass in the required parameter `uuids` which is a list of string.
3. Process the response of type `LMResponse<Nothing>` as per your requirement.

```ts
const payload: any = {
  uuids: ["ENTER_LIST_OF_UUIDs_OF_USERS"],
};
const response = await lmChatClient.leaveCommunity(payload);

if (response.success) {
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

### Leave Community Payload

List of parameters supported.

| Variable | Type      | Description                                           | Optional           |
| -------- | --------- | ----------------------------------------------------- | ------------------ |
| `uuids`  | strings[] | List of uuids of user who want to leave the community | :heavy_check_mark: |
