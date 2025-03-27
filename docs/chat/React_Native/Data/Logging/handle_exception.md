---
sidebar_position: 1
title: Handle Execption
slug: /react-native/data/handle-execption
---

# Handle Execption

The LikeMinds Chat SDK provides a built-in logging system that captures and reports errors encountered during execution of our SDK. This system allows developers to configure logging preferences, handle errors effectively, and optionally share logs with LikeMinds for debugging purposes.

The `handleException()` method in LMChatLogger is responsible for capturing, logging and handling errors that occur within the application. It ensures that errors are recorded locally and handled as well.

## Steps to Handle Execption

you can log errors using the `handleException()` method. This method captures error details and processes them according to the logging configuration.

1. To log and handle an execption, use the `handleException()` method on the LMChatClient instance.
2. Pass the required parameters: `exception`, `stackTrace` and `severity`.
3. The log is saved in the Realm database and can be retrieved later using [getLogs()](./get_logs.md).

### Example Usage

```ts
lmChatClient?.handleException(
  error,
  {
    exception: error,
    trace: error?.stack,
  },
  LMSeverity.ERROR // severity of the error encountered
);
```

### Handle Exception Parameters

| Parameter    | Type                                        | Description                                          |
| ------------ | ------------------------------------------- | ---------------------------------------------------- |
| `exception`  | `Error`                                     | The error object to be logged.                       |
| `stackTrace` | [LMStackTrace](../Models/logging.md) | Contains `exception` message and `trace`.            |
| `severity`   | [LMSeverity](../Models/logging.md)      | The severity level of the error (INFO, ERROR, etc.). |
