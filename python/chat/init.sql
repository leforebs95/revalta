-- Create tables
CREATE TABLE IF NOT EXISTS chats (
    chat_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id INTEGER NOT NULL CHECK (user_id > 0),
    title TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    UNIQUE (chat_id, user_id)
);

CREATE TABLE IF NOT EXISTS messages (
    message_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chat_id UUID NOT NULL REFERENCES chats(chat_id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL CHECK (user_id > 0),
    content TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (chat_id, user_id) REFERENCES chats(chat_id, user_id)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_chats_user_id ON chats(user_id);
CREATE INDEX IF NOT EXISTS idx_messages_chat_user ON messages(chat_id, user_id);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at);

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
ALTER TABLE chats ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
CREATE POLICY chats_user_isolation ON chats
FOR ALL USING (check_user_access());

CREATE POLICY messages_user_isolation ON messages
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
GRANT ALL ON SCHEMA public TO local_chat_user;
GRANT ALL ON ALL TABLES IN SCHEMA public TO local_chat_user;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO local_chat_user;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO local_chat_user; 