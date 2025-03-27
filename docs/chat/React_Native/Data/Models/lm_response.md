---
sidebar_position: 1
title: LMResponse
slug: /react-native/data/models/lm-response
---

This is a wrapper class for all the responses returned by the SDK. It contains the following parameters:

| Variable     | Type    | Description                            | Optional           |
| ------------ | ------- | -------------------------------------- | ------------------ |
| success      | bool    | API success status                     |                    |
| errorMessage | string? | Error message in case of failure       | :heavy_check_mark: |
| data         | dynamic | Object of specific response data class | :heavy_check_mark: |
