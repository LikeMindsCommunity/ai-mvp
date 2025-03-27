---
sidebar_position: 4
title: Insert Log
slug: /react-native/data/insert-log
---

# Insert Log

The `insertLog()` method on the LMChatClient allows you to save a log in the local database i.e Realm which could later be retrieved.

## Steps To Insert Log

1. To store a log, use the `insertLog()` method on the LMChatClient instance.
2. Pass the required parameters: `timestamp`, `stackTrace`, `sdkMeta`, and `severity`.
3. The log is saved in the Realm database and can be retrieved later using [getLogs()](./get_logs.md).

### Example Usage

```ts
const logEntry = {
  timestamp: Date.now(),
  stackTrace: { exception: "Error message", trace: "Stack trace details" },
  sdkMeta: { coreVersion: "1.0.0", dataLayerVersion: "2.1.0" },
  severity: LMSeverity.ERROR,
};

await lmChatClient?.insertLog(logEntry);
```

### Insert Log Parameters

| Variable   | Type                                        | Description                                                       |
| ---------- | ------------------------------------------- | ----------------------------------------------------------------- |
| timestamp  | number                                      | The time when the log was created.                                |
| stackTrace | [LMStackTrace](../Models/logging.md) | Contains `exception` and `trace` details.                         |
| sdkMeta    | [LMSDKMeta](../Models/logging.md)       | Contains SDK version details (`coreVersion`, `dataLayerVersion`). |
| severity   | [number](../Models/logging.md)          | The severity level of the log (INFO, ERROR, etc.).                |

