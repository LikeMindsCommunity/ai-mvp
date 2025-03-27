---
sidebar_position: 2
title: Get Logs
slug: /react-native/data/get-logs
---

# Get Logs

The `getLogs()` method on the LMChatClient allows you to retrieve all logs stored in the local database.

## Steps to Retrieve Logs

1. Use the `getLogs()` method on the LMChatClient instance.
2. The method fetches all stored logs and returns them.
3. The logs contain details such as timestamp, stack trace, SDK metadata, and severity level.

### Example Usage

```ts
const logs = await lmChatClient?.getLogs();
console.log(logs); // Logs stored in Realm DB;
```

### Get Logs Response

| Variable   | Type                                       | Description                                                       |
| ---------- | ------------------------------------------ | ----------------------------------------------------------------- |
| timestamp  | number                                     | The time when the log was created.                                |
| stackTrace | [LMStackTrace](../Models/logging.md) | Contains `exception` and `trace` details.                         |
| sdkMeta    | [LMSDKMeta](../Models/logging.md)    | Contains SDK version details (`coreVersion`, `dataLayerVersion`). |
| severity   | [LMSeverity](../Models/logging.md)   | The severity level of the log (INFO, ERROR, etc.).                |
