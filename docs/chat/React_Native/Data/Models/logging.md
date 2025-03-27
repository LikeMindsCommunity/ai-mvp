---
sidebar_position: 6
title: Error Logging
slug: /react-native/data/models/error-logging
---

## LMSeverity

The `LMSeverity` enum represents different levels of log severity.

| Value | Name      | Description                          |
| ----- | --------- | ------------------------------------ |
| `0`   | INFO      | General information logs.            |
| `1`   | DEBUG     | Debugging logs for developers.       |
| `2`   | NOTICE    | Important notices but not warnings.  |
| `3`   | WARNING   | Indicates potential issues.          |
| `4`   | ERROR     | Represents application errors.       |
| `5`   | CRITICAL  | Critical issues requiring attention. |
| `6`   | ALERT     | Immediate attention needed.          |
| `7`   | EMERGENCY | System-wide failure.                 |
| `8`   | DEFAULT   | Default severity level.              |

## LMSDKMeta

The `LMSDKMeta` object contains metadata related to the SDK, including version details.

| Property           | Type   | Description                        |
| ------------------ | ------ | ---------------------------------- |
| `coreVersion`      | string | The core version of the SDK.       |
| `dataLayerVersion` | string | The data layer version of the SDK. |

## LMStackTrace

The `LMStackTrace` object holds details about an error, including the exception message and stack trace.

| Property    | Type   | Description                   |
| ----------- | ------ | ----------------------------- |
| `exception` | string | The error message.            |
| `trace`     | string | The stack trace of the error. |
