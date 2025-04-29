# Use the official Android SDK image
FROM ubuntu:22.04

# Set environment variables
ENV ANDROID_HOME=/opt/android-sdk
ENV PATH=${PATH}:${ANDROID_HOME}/cmdline-tools/latest/bin:${ANDROID_HOME}/platform-tools

# Install required packages
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk \
    wget \
    unzip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Android SDK
RUN mkdir -p ${ANDROID_HOME}/cmdline-tools \
    && wget -q https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O /tmp/cmdline-tools.zip \
    && unzip -q /tmp/cmdline-tools.zip -d ${ANDROID_HOME}/cmdline-tools \
    && mv ${ANDROID_HOME}/cmdline-tools/cmdline-tools ${ANDROID_HOME}/cmdline-tools/latest \
    && rm /tmp/cmdline-tools.zip

# Accept licenses and install required SDK components
RUN yes | sdkmanager --licenses \
    && sdkmanager "platform-tools" \
    && sdkmanager "platforms;android-35" \
    && sdkmanager "build-tools;35.0.0"

# Define build argument for project name and directory
ARG PROJECT_NAME
ARG PROJECT_DIR

# Set working directory
WORKDIR /${PROJECT_NAME}

# Copy project files
COPY ${PROJECT_DIR} . 