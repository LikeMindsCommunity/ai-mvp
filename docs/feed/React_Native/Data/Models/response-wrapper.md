---
title: Response Wrapper
sidebar_position: 1
slug: /react-native/data/models/response-wrapper
---

`LMResponse<T>` caters the base response for all the APIs. Each data function has its own response model which are wrapped inside `LMResponse<T>`.

:::note
All the `response` variables throughout the documentation are of type `LMResponse<T>`.
:::

The following table shows the structure of the wrapper `LMResponse<T>`.

| **VARIABLE**   | **TYPE** | **DESCRIPTION**                                                | **OPTIONAL** |
| :------------- | :------- | :------------------------------------------------------------- | :----------: |
| `success`      | Bool     | `true` if the API call was successful, `false` otherwise.      |              |
| `errorMessage` | String   | Error message in case the API fails.                           |      ✔       |
| `data`         | T        | Generic variable that holds the data received in API response. |      ✔       |
