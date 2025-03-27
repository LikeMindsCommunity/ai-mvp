---
sidebar_position: 3
title: Flush Logs
slug: /react-native/data/flush-logs
---

# Flush Logs

The `flushlogs()` method on the LMChatLogger allows you to retrieve locally stored logs and send them to the LikeMinds backend. Once successfully pushed, the logs are cleared from the local database.

## Steps to Flush Log

1. Use the `flushlogs` method on the LMChatClient instance.
2. The method fetches all stored logs and sends them to the LikeMinds backend and clears all logs locally

### Example Usage

```ts
await lmChatClient?.flushlogs();
```
