---
sidebar_position: 1
title: Members List
slug: /react-native/data/chatroom/direct-messages/members-list
---

# Members List

LikeMinds React Native Chat SDK offers a convenient feature that enables the retrieval of a list of members for direct messaging (DM) functionality.

## Steps to get the list of members in the community

1. To fetch the list of the members, use the method `getAllMembers()` provided by the client you initialised.
2. Pass the required parameters `page`.
3. Process the response as per your requirement.

```ts
// get show_list value from `checkDMStatus` method
const memberPayload: any = {
  page: 1,
};

const cmPayload: any = {
  page: 1,
  memberState: 1, //for CM
};
const response = await lmChatClient?.getAllMembers(
  show_list === 1 ? memberPayload : cmPayload
);

if (response.success) {
  // your function to process the response data
  processResponse();
} else {
  // your function to process error message
  processError(response);
}
```

### Get All Members Payload

List of parameters for the `getAllMembers()` function.

| Variable      | Type   | Description             | Optional           |
| ------------- | ------ | ----------------------- | ------------------ |
| `page`        | number | Page int                |                    |
| `memberState` | int    | State of logged in user | :heavy_check_mark: |

### Get All Members Response

List of parameters in the response.

| Variable | Type   | Description     |
| -------- | ------ | --------------- |
| members  | object | List of members |

# Search in Members List

LikeMinds React Native Chat SDK offers a powerful feature that allows you to easily search within the members list, facilitating efficient discovery of specific members for direct messaging (DM) functionality.

## Steps to search members in a community

1. To search the list of the members, use the method `searchMembers()` provided by the client you initialised.
2. Pass the required parameters `page`, `pageSize`, `search` and `searchType`.
3. Process the response as per your requirement.

```ts
// get show_list value from `checkDMStatus` method
const memberPayload: any = {
  search: searchString, // string that you have searched
  searchType: "name", // type of search
  page: 1,
  pageSize: 10, // list of members you want in a page
};

const cmPayload: any = {
  search: searchString, // string that you have searched
  searchType: "name", // type of search
  page: 1,
  pageSize: 10, // list of members you want in a page
  memberStates: "[1]", // for CM
};

const response = await lmChatClient?.searchMembers(
  show_list === 1 ? memberPayload : cmPayload
);

if (response.success) {
  // your function to process the response data
  processResponse();
} else {
  // your function to process error message
  processError(response);
}
```

### Search Members Payload

List of parameters for the `searchMembers()` function.

| Variable      | Type   | Description                        | Optional           |
| ------------- | ------ | ---------------------------------- | ------------------ |
| `page`        | number | Page int                           |                    |
| `search`      | string | String that you have searched      |                    |
| `searchType`  | string | Type of search                     |                    |
| `pageSize`    | number | List of members you want in a page |                    |
| `memberState` | number | State of logged in user            | :heavy_check_mark: |

### Search Members Response

List of parameters in the response.

| Variable | Type   | Description     |
| -------- | ------ | --------------- |
| members  | object | List of members |
