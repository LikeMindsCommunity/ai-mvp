---
sidebar_position: 2
title: Setup Notifications
---

# Setup Notifications using FCM HTTP v1

Firebase will be deprecating the legacy FCM APIs and replacing them with the new HTTP v1 API. This also introduces changes to the way the firebase project is authenticated on server-side. For more information please refer to the official announcement by Firebase [here](https://firebase.google.com/docs/cloud-messaging/migrate-v1)

From now, instead of a firebase server key, a JSON file that contains the authentication information related to the project will be required for the notification service to work.

## Firebase Integration

LikeMind SDK now requires service account credentials in the form of a json file that can be obtained from the gcp service account associated to your firebase project to send notifications for messages and other things.

### Step 1: Generate Service Account File for FCM

1.  Go to [Firebase Console](https://console.firebase.google.com/). If you don't have a Firebase project, please create a new project.

     <img src="/img/fcm_server_key_1.png" alt="FCM Server - Firebase Console"/>

2.  Select your project and move to **Project Overview**

3.  Click on the settings icon and select **Project Settings**

     <img src="/img/fcm_server_key_2.png" alt="FCM Server - Project Settings"/>

4.  Go to **Cloud Messaging > Manage service accounts**. clicking this link will take you to the service account section in your gcp console. Make sure you are logged in to gcp from the correct account.

     <img src="/img/fcm_http_v1_1.png" alt="FCM Server - Manage Service Accounts"/>

5.  Click on the name of the service account that is attached to your firebase project. This will take you to the page where service account details can be accessed.

     <img src="/img/fcm_http_v1_2.png" alt="FCM Server - Service Account Details"/>

6.  On clicking the keys tab, you will see the buton that allows you to generate new keys.

     <img src="/img/fcm_http_v1_3.png" alt="FCM Server - Service Account Keys"/>

7.  Click **ADD KEY** and choose **Create new key > JSON > CREATE**

     <img src="/img/fcm_http_v1_4.png" alt="FCM Server - Create Key"/>
     <img src="/img/fcm_http_v1_5.png" alt="FCM Server - Key Type"/>

8.  The JSON file that includes the credentials to your gcp service account should now be downloaded to your system. Keep this file safe.

    <img src="/img/fcm_http_v1_6.png" alt="FCM Server - Service Account JSON File"/>

9.  The final step is to upload the JSON file to the LikeMinds server. The file can be uploaded either from the dashboard itself or by manually calling the upload API. The manual upload consists of the following steps:

    a. Generate OTP using GET `/otp/generate` and params - `country_code` , `mobile_no` ***(dashboard user mobile no.)***

    ```bash
    curl --location 'https://auth.likeminds.community/otp/generate?country_code=91&mobile_no=1234567890'
    ```

    b. Generate `auth_token` using GET `/otp/verify` and params - `country_code` , `mobile_no` ***(dashboard user mobile no.)*** & `otp`.

    ```bash
    curl --location 'https://auth.likeminds.community/otp/verify?country_code=<your_country_code>&mobile_no=<your_mobile_number>&otp=<your_otp>'
    ```

    c. Update `gcp_service_account_file` using API - PUT `/sdk/project` with Headers: `Authorization:<auth_token generated above>` , `x-api-key: <api_key of community>` & Request Body: `gcp_service_account_file : <service account json file contents>`

    ```bash
    curl --location --request PUT 'https://auth.likeminds.community/sdk/project' \
    --header 'Authorization: <auth_token>' \
    --header 'x-api-key: <api_key>' \
    --header 'x-platform-type: dashboard' \
    --data-raw '{
        "gcp_service_account_file": {
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "client_email": "firebase-adminsdk@your-project-name.iam.gserviceaccount.com",
            "client_id": "1071026063271489",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk%40your-project-name.iam.gserviceaccount.com",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCnONrfmEW5eMAQ\nYBJh9jYzJ0WA7W6KU04k9O8KloDYuGshxgkGkbuovAycYqCWO5fz0dA4KjUWiMCz\nV1ACr+rL86SrXQaTx1KipHpQmZ+Lf8JpK1xRgNthdFH7Qzl9i7cq8Rxtl5h2ny/o\nI/qaznMfTcPy+hBxRaIj7RwZpk5MkCfDLJXrUmak23kH0IXgmQEm7v5NjTrQvJr+\nStU1DuR9uWEmoug8UWE2d//NwyJX2r7KJ00TKeVOMBGq/o0yQOjw/z20pgMRIzwg\neErKjmCJv+q7AiCLb61UzMYtVJBifETbt1jhVVYduwd+xKZEOpm29P8oEk\nQbwulHh7gkgb8bEfffFNtPw7jN7q21zEWC8ZxEU2KQHgHQwYe+fRIxrN9euNMY6D\neRYXSFoqm0qXZ4N5ofJapiH1eLBNA6u+s2jrnHfFsv+Ga3aKqLqvzLkqHqWKavd5\nHGw52Z7Fo2BKAetSw9NBh246Taf798pczg==\n-----END PRIVATE KEY-----\n",
            "private_key_id": "0310b75bf8c217d4983965200",
            "project_id": "your-project-name",
            "token_uri": "https://oauth2.googleapis.com/token",
            "type": "service_account",
            "universe_domain": "googleapis.com"
        }
    }'
    ```

    :::info

    Note: Make sure to replace api*key , auth_token & gcp_service_account_file contents.*

    :::
