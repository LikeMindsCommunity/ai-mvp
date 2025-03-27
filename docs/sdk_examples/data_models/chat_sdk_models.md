# Chat SDK Data Models

This document outlines the key data models used in the LikeMinds Chat SDK, their structure, and relationships.

## Core Models

### User

The User model represents a user in the system.

```typescript
interface User {
  id: string;           // Unique identifier for the user
  name: string;         // Display name of the user
  profilePicUrl?: string; // URL to the user's profile picture
  isGuest: boolean;     // Whether the user is a guest
  isDeleted: boolean;   // Whether the user account has been deleted
  customFields?: Record<string, any>; // Custom user properties
}
```

### Conversation

The Conversation model represents a chat between users.

```typescript
interface Conversation {
  id: string;           // Unique identifier for the conversation
  title: string;        // Title/name of the conversation
  type: ConversationType; // Type of conversation (private, group, community)
  lastMessage?: Message; // The most recent message in the conversation
  participants: User[];  // Users participating in the conversation
  createdAt: number;    // Timestamp when the conversation was created
  updatedAt: number;    // Timestamp when the conversation was last updated
  unreadCount: number;  // Number of unread messages for the current user
  metadata?: Record<string, any>; // Additional conversation data
}

enum ConversationType {
  PRIVATE = 'private',   // One-to-one chat
  GROUP = 'group',       // Group chat
  COMMUNITY = 'community' // Community-wide chat
}
```

### Message

The Message model represents an individual message within a conversation.

```typescript
interface Message {
  id: string;           // Unique identifier for the message
  conversationId: string; // ID of the conversation this message belongs to
  sender: User;         // User who sent the message
  content: string;      // Text content of the message
  attachments: Attachment[]; // Files or media attached to the message
  state: MessageState;  // Current state of the message (sent, delivered, etc.)
  replyTo?: Message;    // If this is a reply, the original message
  reactions: Reaction[]; // Reactions to this message (likes, etc.)
  createdAt: number;    // Timestamp when the message was sent
  updatedAt: number;    // Timestamp when the message was last updated
  isDeleted: boolean;   // Whether the message has been deleted
  metadata?: Record<string, any>; // Additional message metadata
}

enum MessageState {
  SENDING = 'sending',   // Message is being sent
  SENT = 'sent',         // Message has been sent to the server
  DELIVERED = 'delivered', // Message has been delivered to recipient(s)
  READ = 'read',         // Message has been read
  FAILED = 'failed'      // Message failed to send
}
```

### Attachment

The Attachment model represents a file or media attachment on a message.

```typescript
interface Attachment {
  id: string;           // Unique identifier for the attachment
  type: AttachmentType; // Type of attachment
  url: string;          // URL to the attachment
  name: string;         // Original file name
  size: number;         // File size in bytes
  mimeType: string;     // MIME type of the file
  metadata?: Record<string, any>; // Additional attachment metadata
}

enum AttachmentType {
  IMAGE = 'image',
  VIDEO = 'video',
  AUDIO = 'audio',
  DOCUMENT = 'document',
  LOCATION = 'location',
  CONTACT = 'contact'
}
```

### Reaction

The Reaction model represents a reaction to a message.

```typescript
interface Reaction {
  id: string;           // Unique identifier for the reaction
  messageId: string;    // ID of the message this reaction is for
  user: User;           // User who added the reaction
  type: string;         // Type of reaction (e.g., 'like', 'heart', 'thumbsup')
  createdAt: number;    // Timestamp when the reaction was added
}
```

## Model Relationships

```
User
 ├── sends → Message
 ├── participates in → Conversation
 └── creates → Reaction

Conversation
 ├── contains → Message
 └── includes → User (participants)

Message
 ├── belongs to → Conversation
 ├── sent by → User
 ├── may reference → Message (for replies)
 ├── has → Attachment
 └── receives → Reaction

Attachment
 └── belongs to → Message

Reaction
 ├── belongs to → Message
 └── created by → User
```

## State Management

The SDK maintains local copies of these models and synchronizes with the server. Changes to models trigger events that can be listened to for real-time updates.

### Message Lifecycle

1. User creates a message (state: SENDING)
2. SDK attempts to send the message to the server
3. On successful sending, the state changes to SENT
4. When delivered to all recipients, the state changes to DELIVERED
5. When read by all recipients, the state changes to READ

If a failure occurs at any point, the state changes to FAILED, and the SDK provides retry mechanisms.

## Custom Fields

All primary models support custom fields via the `metadata` or `customFields` properties. These can be used to extend the models with application-specific data without modifying the core SDK. 