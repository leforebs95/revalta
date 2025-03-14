-- Enable RLS on tables
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_chunks ENABLE ROW LEVEL SECURITY;

-- Create policies for documents table
CREATE POLICY documents_user_isolation ON documents
    FOR ALL
    USING (user_id = current_setting('app.current_user_id')::integer);

-- Create policies for document_chunks table
CREATE POLICY chunks_user_isolation ON document_chunks
    FOR ALL
    USING (user_id = current_setting('app.current_user_id')::integer);

-- Create function to set user context
CREATE OR REPLACE FUNCTION set_user_id(p_user_id integer)
RETURNS void AS $$
BEGIN
    PERFORM set_config('app.current_user_id', p_user_id::text, false);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER; 