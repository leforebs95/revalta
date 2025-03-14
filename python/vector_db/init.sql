-- Enable the vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create tables
CREATE TABLE IF NOT EXISTS documents (
    document_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id INTEGER NOT NULL CHECK (user_id > 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    UNIQUE (document_id, user_id)
);

CREATE TABLE IF NOT EXISTS document_chunks (
    chunk_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES documents(document_id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL CHECK (user_id > 0),
    chunk_seq_number INTEGER NOT NULL,
    chunk_text TEXT NOT NULL,
    embedding vector(384) NOT NULL,
    chunk_metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (document_id, user_id) REFERENCES documents(document_id, user_id)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_documents_user_id ON documents(user_id);
CREATE INDEX IF NOT EXISTS idx_chunks_user_id ON document_chunks(user_id);
CREATE INDEX IF NOT EXISTS idx_chunks_document_user ON document_chunks(document_id, user_id);

-- Function to check if operation is allowed
CREATE OR REPLACE FUNCTION check_user_access()
RETURNS boolean AS $$
BEGIN
    -- Allow access if current_user_id is not set (system operations)
    -- or if it matches the row's user_id
    RETURN (
        CASE 
            WHEN current_setting('app.current_user_id', TRUE) IS NULL THEN TRUE
            ELSE user_id = current_setting('app.current_user_id')::integer
        END
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Enable Row Level Security
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_chunks ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
CREATE POLICY documents_user_isolation ON documents
FOR ALL USING (check_user_access());

CREATE POLICY chunks_user_isolation ON document_chunks
FOR ALL USING (check_user_access());

-- Function to set user context
CREATE OR REPLACE FUNCTION set_user_id(p_user_id integer)
RETURNS void AS $$
BEGIN
    -- NULL is valid for system operations
    PERFORM set_config('app.current_user_id', 
        CASE WHEN p_user_id IS NULL 
        THEN NULL 
        ELSE p_user_id::text 
        END, 
        false);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Grant necessary permissions to the application user
GRANT ALL ON SCHEMA public TO local_vector_user;
GRANT ALL ON ALL TABLES IN SCHEMA public TO local_vector_user;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO local_vector_user;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO local_vector_user; 