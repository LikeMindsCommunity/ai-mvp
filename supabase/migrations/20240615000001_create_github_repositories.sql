-- Migration to create a GitHub repositories table for tracking imported repos
-- This enables the system to manage GitHub repositories for code generation

-- Create the github_repositories table
CREATE TABLE IF NOT EXISTS "github_repositories" (
    "id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "user_id" UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    "project_id" UUID REFERENCES projects(id) ON DELETE SET NULL,
    "repo_name" TEXT NOT NULL,
    "repo_full_name" TEXT NOT NULL,
    "repo_url" TEXT NOT NULL,
    "default_branch" TEXT NOT NULL DEFAULT 'main',
    "selected_branch" TEXT,
    "clone_url" TEXT NOT NULL,
    "selected_path" TEXT,
    "status" TEXT NOT NULL DEFAULT 'pending' CHECK ("status" IN ('pending', 'cloning', 'analyzing', 'ready', 'error')),
    "error_message" TEXT,
    "last_synced_at" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT now(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT now(),
    "metadata" JSONB
);

-- Add comment to the table
COMMENT ON TABLE "github_repositories" IS 'Tracks GitHub repositories imported for code generation';

-- Create indices for faster lookups
CREATE INDEX IF NOT EXISTS "github_repositories_user_id_idx" ON "github_repositories" ("user_id");
CREATE INDEX IF NOT EXISTS "github_repositories_project_id_idx" ON "github_repositories" ("project_id");
CREATE INDEX IF NOT EXISTS "github_repositories_status_idx" ON "github_repositories" ("status");

-- RLS Policies: Only allow users to see and manage their own repositories
ALTER TABLE "github_repositories" ENABLE ROW LEVEL SECURITY;

-- Policy for selecting repositories (only your own)
CREATE POLICY "Users can view their own GitHub repositories" 
    ON "github_repositories" 
    FOR SELECT 
    USING (auth.uid() = user_id);

-- Policy for inserting repositories (only for yourself)
CREATE POLICY "Users can insert their own GitHub repositories" 
    ON "github_repositories" 
    FOR INSERT 
    WITH CHECK (auth.uid() = user_id);

-- Policy for updating repositories (only your own)
CREATE POLICY "Users can update their own GitHub repositories" 
    ON "github_repositories" 
    FOR UPDATE 
    USING (auth.uid() = user_id);

-- Policy for deleting repositories (only your own)
CREATE POLICY "Users can delete their own GitHub repositories" 
    ON "github_repositories" 
    FOR DELETE 
    USING (auth.uid() = user_id);

-- Trigger to automatically update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_github_repositories_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_github_repositories_updated_at
BEFORE UPDATE ON "github_repositories"
FOR EACH ROW
EXECUTE FUNCTION update_github_repositories_updated_at(); 