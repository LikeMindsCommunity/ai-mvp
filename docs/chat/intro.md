---
slug: /
sidebar_position: 1
title: "Overview"
---

## Introduction

[![Simple HLD](../static/img/simple_hld.webp)](https://app.eraser.io/workspace/NB7otbW5v56uysKmHYQu)

Welcome to the LikeMinds Chat SDK Getting Started Guide! In this guide, we will walk you through the initial steps to integrate and utilize the LikeMinds Chat SDK in your application. LikeMinds is a powerful platform that enables developers to seamlessly integrate chat functionalities into their applications, enhancing user engagement and communication.
The chat feature allows users to have real-time conversations within your application. It supports features such as sending text messages, media attachments, typing indicators, read receipts, and more.

This guide is designed to provide you with an overview of the LikeMinds Chat SDK and its components. We will cover the setup process, including obtaining an API key from the LikeMinds dashboard, and explain the key concepts and functionalities you need to know to get started quickly.

## Components of LikeMinds

The LikeMinds Chat SDK comprises various components that provide a seamless chat experience. These components include:

1. **Frontend SDKs:** SDKs that power chat inside your application to provide your users a seamless in-app Chat experience. We also have open-source UI kits to help you get up and running effortlessly.
2. **Dashboard:** The LikeMinds dashboard provides options to setup manage users, channels, and features and setup permissions. The dashboard also features moderation capabilities.
3. **Backend REST APIs:** The Backend REST APIs provide the infra to power the in-app chat experience with scalable realtime communication.

![HLD](../static/img/LM_HLD@latest.png)

## Architecture of the SDK

The **LikeMinds Chat SDK** is designed to be modular and flexible, allowing developers to customize every aspect of the chat experience. This document outlines the architecture of the SDK, including its layers, components, and how to implement customizations.

![Architecture Diagram](/img/architecture.png)


The SDK is divided into three layers and components to promote separation of concerns and ease of customization:

1. **Core Layer** - Handles initialization, configuration, and business logic of chat functionalities.
2. **UI Layer** - Gives access to all the widgets required to build the chat screens (in core).
3. **Data Layer** - An API layer that provides access to our backend APIs, models and services.

### Core Layer

#### Purpose
The Core package serves as the backbone of the SDK, managing all business logic, state management, networking, and coordination between different components. It ensures that the application functions seamlessly, handling data processing, user interactions, and integration with backend services.

This is the first layer you will be working with when you are starting to integrate the LikeMinds SDK. It also gives access to all the other layers as well (UI and Data).

#### Structure and Components
The Core package is segmented into various modules, each addressing specific functionalities:
- **Views**: Constructs screens by integrating UI components with business logic.
- **State Management**: Implements the patterns for managing application state.
- **Convertors and Models**: Handles data conversion between different layers and defines data models.
- **Utilities and Services**: Provides utility functions, networking, and notification handling.


### UI Layer

#### Purpose
The UI package is dedicated to building and managing the user interface components of the SDK. It encapsulates all visual elements, ensuring a consistent and reusable set of widgets and UI atoms that can be leveraged across different screens and functionalities. You can combine any combination of these widgets (like molecules) to make any kind of experiences you want. 

#### Structure and Components
The UI package is organized into various directories, each focusing on specific UI elements:
- **Common Widgets**: Reusable UI components like text, icons, tiles, buttons, and more.
- **Conversation**: Widgets specific to chat conversations, like chat bubbles.
- **Polls and Reactions**: UI elements for handling polls and user reactions.
- **Media**: Components handling different media types like images, videos, documents, GIFs, and voice notes.
- **Extras**: Supplementary UI elements such as app bars, loaders, chips, etc.
- **Shimmers**: Placeholder animations for loading states.

### Data Layer

#### Purpose
The Data package is responsible for handling all data-related functionalities, including API requests, data processing, and integration with backend services. It ensures that the application can fetch, store, and manage data efficiently, providing a robust foundation for the SDK's core functionalities.

#### Structure and Components
The Data package is organized into various directories, each focusing on specific data-related functionalities:
- **Client**: The main class that exposes all APIs as public functions. 
- **Models**: Defines data models and structures used throughout the SDK.
- **Services**: Implements API requests, data processing, and integration with backend services.
- **Repositories**: Manages data storage, retrieval, and synchronization.


## Generate API Key

You'll need an API key to integrate the LikeMinds Chat SDK into your application. Follow these steps to obtain your API key from the LikeMinds dashboard:

1. Go to [LikeMinds Dashboard](https://dashboard.likeminds.community) and sign in to your account. You can create one using your work email address if you don't have an account.
   If you are a first time user you would see an option to **“Add your first app”.** You can do so by clicking on the given button

   ![LikeMinds Dashboard](../static/img/dashboard-create-new-app.webp)

2. Now you can navigate to the settings on the sidebar. Under general section you should be able to see an auto generated API key for your account.

   ![Get New API key](../static/img/get-api-key.webp)

3. Make sure to securely store your API key, as it will be required for authentication when making requests to the LikeMinds APIs.

You are now all set to integrate LikeMinds Chat to in your mobile/web application. Check the respective documentation guides for your application.

## SDK size

| Tech Stack                                      | Size    |
| ----------------------------------------------- | ------- |
| Android                                         | 12.3 MB |
| iOS                                             | 14.3 MB |
| Flutter (Android)                               | 4.6 MB  |
| Flutter (iOS)                                   | 7.1 MB  |
| ReactNative (Android, with all dependencies)    | 11.7 MB |
| ReactNative (Android, without all dependencies) | 7.9 MB  |
| ReactNative (iOS, with all dependencies)        | 7.8 MB  |
| ReactNative (iOS, without all dependencies)     | 5.9 MB  |
| ReactJS                                         | 1.2 MB  |
