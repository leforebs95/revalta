import React, { useState, useEffect } from 'react';
import { AlertCircle, FileText, Trash2 } from 'lucide-react';
import { Alert, AlertDescription } from '../common/Alert';
import { documentsAPI } from '../../lib/api/documents';
import FileUpload from '../common/FileUpload';

interface Document {
  id: string;
  filename: string;
  url: string;
  uploaded_at: string;
}

const LabResults = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      const response = await documentsAPI.getDocuments();
      setDocuments(response.documents);
    } catch (err) {
      setError('Failed to fetch documents');
      console.error('Error fetching documents:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleUpload = async (files: File[]) => {
    try {
      setLoading(true);
      setError(null);
      await documentsAPI.uploadDocuments(files);
      await fetchDocuments();
    } catch (err) {
      setError('Failed to upload documents');
      console.error('Upload error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (documentId: string) => {
    try {
      setLoading(true);
      setError(null);
      await documentsAPI.deleteDocument(documentId);
      await fetchDocuments();
    } catch (err) {
      setError('Failed to delete document');
      console.error('Delete error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow-sm">
        <h2 className="text-xl font-semibold mb-4">Upload Lab Documents</h2>
        
        <FileUpload 
          onUpload={handleUpload}
          isUploading={loading}
          accept=".pdf"
        />

        {error && (
          <Alert variant="destructive" className="mt-4">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        <div className="mt-8">
          <h3 className="font-semibold mb-4">Your Documents</h3>
          <div className="space-y-4">
            {documents.map((doc) => (
              <div
                key={doc.id}
                className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
              >
                <div className="flex items-center gap-3">
                  <FileText className="h-5 w-5 text-gray-400" />
                  <div>
                    <p className="font-medium">{doc.filename}</p>
                    <p className="text-sm text-gray-500">
                      Uploaded on {new Date(doc.uploaded_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <a
                    href={doc.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-nivaltaBlue hover:text-indigo-600 text-sm"
                  >
                    View
                  </a>
                  <button
                    onClick={() => handleDelete(doc.id)}
                    className="text-red-500 hover:text-red-600"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>
            ))}
            {!loading && documents.length === 0 && (
              <p className="text-gray-500 text-center py-4">
                No documents uploaded yet
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LabResults;