-- Migration to create a GitHub tokens table for storing OAuth tokens securely
-- This allows users to connect their GitHub accounts for repository integration

-- Create an extension for encryption if not exists (for token encryption)
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create the github_tokens table
CREATE TABLE IF NOT EXISTS "github_tokens" (
    "id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "user_id" UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    "access_token" TEXT NOT NULL,
    "refresh_token" TEXT,
    "token_type" TEXT NOT NULL DEFAULT 'bearer',
    "scope" TEXT,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT now(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT now(),
    "expires_at" TIMESTAMPTZ,
    "is_active" BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE("user_id")
);

-- Add comment to the table
COMMENT ON TABLE "github_tokens" IS 'Stores encrypted GitHub OAuth tokens for users';

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS "github_tokens_user_id_idx" ON "github_tokens" ("user_id");

-- RLS Policies: Only allow users to see and manage their own GitHub tokens
ALTER TABLE "github_tokens" ENABLE ROW LEVEL SECURITY;

-- Policy for selecting tokens (only your own)
CREATE POLICY "Users can view their own GitHub tokens" 
    ON "github_tokens" 
    FOR SELECT 
    USING (auth.uid() = user_id);

-- Policy for inserting tokens (only for yourself)
CREATE POLICY "Users can insert their own GitHub tokens" 
    ON "github_tokens" 
    FOR INSERT 
    WITH CHECK (auth.uid() = user_id);

-- Policy for updating tokens (only your own)
CREATE POLICY "Users can update their own GitHub tokens" 
    ON "github_tokens" 
    FOR UPDATE 
    USING (auth.uid() = user_id);

-- Policy for deleting tokens (only your own)
CREATE POLICY "Users can delete their own GitHub tokens" 
    ON "github_tokens" 
    FOR DELETE 
    USING (auth.uid() = user_id);

-- Trigger to automatically update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_github_tokens_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_github_tokens_updated_at
BEFORE UPDATE ON "github_tokens"
FOR EACH ROW
EXECUTE FUNCTION update_github_tokens_updated_at(); 