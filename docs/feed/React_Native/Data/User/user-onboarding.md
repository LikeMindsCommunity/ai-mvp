---
sidebar_position: 5
title: User Onboarding
slug: /react-native/data/user/user-onboarding
---

To track a user's onboarding status upon app launch, the key `isUserOnboardingDone` stores a boolean value indicating whether onboarding is complete (true) or incomplete (false).

## Steps to get `isUserOnboardingDone` key

1. Use the `getIsUserOnboardingDone()` function provided by the `lmFeedClient` object created earlier.

```ts
try {
  let isUserOnboardingDone = await Client.myClient?.getIsUserOnboardingDone();
  if (isUserSet?.getData() == null) return false;
  return isUserSet.getData();
} catch (error) {
  return false;
}
```

## Steps to set `isUserOnboardingDone` key

1. Use the `setIsUserOnboardingDone()` function provided by the `lmFeedClient` object created earlier.
2. Call the above function with a boolean parameter i.e `true` or `false`.
3. Use the response as per your requirement.

```ts
try {
  const response = await Client.myClient?.setIsUserOnboardingDone(<"BOOLEAN_ONBOARDING_STATUS">);
  if (response?.getData() == true) return true;
  return false;
} catch (error) {
  return false;
}
```
