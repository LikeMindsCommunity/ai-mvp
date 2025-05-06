-- Create github_tokens table
CREATE TABLE IF NOT EXISTS github_tokens (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    installation_id BIGINT NOT NULL,
    access_token TEXT NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    refresh_at TIMESTAMPTZ NOT NULL,
    scopes TEXT[] NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(user_id, installation_id)
);

-- Create github_repositories table
CREATE TABLE IF NOT EXISTS github_repositories (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    installation_id BIGINT NOT NULL REFERENCES github_tokens(installation_id),
    repo_id BIGINT NOT NULL,
    name TEXT NOT NULL,
    full_name TEXT NOT NULL,
    clone_url TEXT NOT NULL,
    default_branch TEXT NOT NULL,
    private BOOLEAN NOT NULL DEFAULT false,
    language TEXT,
    fetched_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(installation_id, repo_id)
);

-- Create indices for better query performance
CREATE INDEX IF NOT EXISTS idx_github_tokens_user_id ON github_tokens(user_id);
CREATE INDEX IF NOT EXISTS idx_github_repositories_user_id ON github_repositories(user_id);
CREATE INDEX IF NOT EXISTS idx_github_repositories_installation_id ON github_repositories(installation_id);

-- Enable RLS
ALTER TABLE github_tokens ENABLE ROW LEVEL SECURITY;
ALTER TABLE github_repositories ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for github_tokens
CREATE POLICY "Users can view their own tokens"
    ON github_tokens FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own tokens"
    ON github_tokens FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own tokens"
    ON github_tokens FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete their own tokens"
    ON github_tokens FOR DELETE
    USING (auth.uid() = user_id);

-- Create RLS policies for github_repositories
CREATE POLICY "Users can view repositories from their installations"
    ON github_repositories FOR SELECT
    USING (
        auth.uid() = user_id OR
        installation_id IN (
            SELECT installation_id FROM github_tokens WHERE user_id = auth.uid()
        )
    );

CREATE POLICY "Users can insert repositories for their installations"
    ON github_repositories FOR INSERT
    WITH CHECK (
        auth.uid() = user_id AND
        installation_id IN (
            SELECT installation_id FROM github_tokens WHERE user_id = auth.uid()
        )
    );

CREATE POLICY "Users can update repositories for their installations"
    ON github_repositories FOR UPDATE
    USING (
        auth.uid() = user_id AND
        installation_id IN (
            SELECT installation_id FROM github_tokens WHERE user_id = auth.uid()
        )
    )
    WITH CHECK (
        auth.uid() = user_id AND
        installation_id IN (
            SELECT installation_id FROM github_tokens WHERE user_id = auth.uid()
        )
    );

CREATE POLICY "Users can delete repositories for their installations"
    ON github_repositories FOR DELETE
    USING (
        auth.uid() = user_id AND
        installation_id IN (
            SELECT installation_id FROM github_tokens WHERE user_id = auth.uid()
        )
    );

-- Add comment for documentation
COMMENT ON TABLE github_tokens IS 'Stores GitHub App installation tokens for users';
COMMENT ON TABLE github_repositories IS 'Caches GitHub repositories available to users through their installations'; 