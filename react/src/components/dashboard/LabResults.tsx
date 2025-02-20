import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { AlertCircle, FileText, Trash2, RotateCw } from 'lucide-react';
import { Dialog, DialogTitle, DialogContent } from "../common/Dialog";
import { Alert, AlertDescription } from '../common/Alert';
import { documentsAPI } from '../../lib/api/uploads';
import { ocrAPI } from '../../lib/api/ocr';
import FileUpload from '../common/FileUpload';
import { useAuth } from '../../providers/AuthProvider';

interface Document {
  uploadId: string; 
  originalFilename: string;
  fileSize: number;
  createdAt: string;
  pages?: DocumentPage[];
}

interface DocumentPage {
  pageNumber: number;
  imageUrl: string;
  content: string;
}

interface DocumentStatus {
  fileId: string;
  status: string;
}

const LabResults = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [ocrStatuses, setOcrStatuses] = useState<{[key: string]: 'pending' | 'complete' | 'failed'}>({});
  const [selectedDoc, setSelectedDoc] = useState<Document | null>(null);
  const [totalPages, setTotalPages] = useState<number>(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [ocrText, setOcrText] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth();
  const navigate = useNavigate();

  const fetchDocuments = async () => {
    if (!user) return;
    try {
      setError(null);
      setLoading(true);

      // First get documents
      const docs = await documentsAPI.getUploads(user.userId);
      setDocuments(docs);
    } catch (err) {
      setError('Failed to fetch documents');
      console.error('Error fetching documents:', err);
    } finally {
      setLoading(false);
    }
    };
   
   useEffect(() => {
    fetchDocuments();
   }, [user]);

  const handleFileUpload = async (file: File) => {
    try {
      setError(null);
      setLoading(true);
      const uploadResponse = await documentsAPI.uploadFile(user.userId, file);
      setLoading(false);
      return uploadResponse;
    } catch (err) {
      setLoading(false);
      setError('Failed to upload document');
      throw err;
    }
  };

  const processOCR = async (fileId: string) => {
    try {
      setOcrStatuses(prev => ({...prev, [fileId]: 'pending'}));
      await ocrAPI.getPages(fileId);
      await ocrAPI.createPages(fileId);
      await ocrAPI.processPages(fileId)
      setOcrStatuses(prev => ({...prev, [fileId]: 'complete'}));
    } catch (err) {
      console.error('OCR processing error:', err);
      setOcrStatuses(prev => ({...prev, [fileId]: 'failed'}));
    }
  };

  const handleUpload = async (file: File) => {
    try {
      const uploadResponse = await handleFileUpload(file);
      await fetchDocuments();
      // Start OCR process but don't wait for it
      processOCR(uploadResponse.uploadId).catch(console.error);
    } catch (err) {
      console.error('Upload error:', err);
    }
  };

  const fetchPageText = async (doc: Document, pageNumber: number) => {
    console.log('Fetching page text:', pageNumber);
    try {
      setError(null);
      setLoading(true);
      const page = await ocrAPI.getPage(doc.uploadId, pageNumber-1);
      const combinedText = page.raw_data.text.join('\n');
      setOcrText(combinedText);
    } catch (err) {
      setError('Failed to fetch page text');
      console.error('Fetch page text error:', err);
    } finally {
      setLoading(false);
    }
  }
  
  const handleFileClick = async (doc: Document) => {
    navigate(`/dashboard/lab-results/${doc.uploadId}`);
  };

  const handlePageChange = async (pageNumber: number) => {
    console.log('Page change:', pageNumber);
    if (!selectedDoc) return;
    try {
      setCurrentPage(pageNumber);
      setLoading(true);
      fetchPageText(selectedDoc, pageNumber);
    } catch (err) {
      setError('Failed to fetch document pages');
      console.error('Fetch pages error:', err);
    } finally {
      setLoading(false);
    }
  }

  const handleRetry = async (documentId: string) => {
    try {
      setError(null);
      setLoading(true);
      await ocrAPI.retryFailedPages(documentId);
      await fetchDocuments();
    } catch (err) {
      setError('Failed to retry document processing');
      console.error('Retry error:', err);
    } finally {
      setLoading(false);
    }
  };
  const handleFileDelete = async (fileId: string) => {
    try {
      setError(null);
      setLoading(true);
      await documentsAPI.deleteUpload(fileId);
      setLoading(false);
      return true;
    } catch (err) {
      setLoading(false); 
      setError('Failed to delete document');
      throw err;
    }
   };
   
   const cleanupOCR = async (fileId: string) => {
    try {
      await ocrAPI.deletePages(fileId);
    } catch (err) {
      console.error('OCR cleanup error:', err);
    }
   };
   
   const handleDelete = async (fileId: string) => {
    try {
      await handleFileDelete(fileId);
      await fetchDocuments();
      // Cleanup OCR but don't block on it
      cleanupOCR(fileId).catch(console.error);
    } catch (err) {
      console.error('Delete error:', err);
    }
   };

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow-sm">
        <h2 className="text-xl font-semibold mb-4">Upload Lab Documents</h2>
        
        <FileUpload 
          onUpload={handleUpload}
          loading={loading}
          error={error}
          accept=".pdf"
          maxFileSize={50 * 1024 * 1024}
        />

        <div className="mt-8">
          <h3 className="font-semibold mb-4">Your Documents</h3>
          <div className="space-y-4">
            {documents.map((doc) => (
              <div
                key={doc.fileId}
                className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
              >
              <div className="flex items-center gap-3">
                  <button onClick={() => handleFileClick(doc)}>
                    <FileText className="h-5 w-5 text-gray-400" />
                  </button>
                  <div>
                    <p className="font-medium text-gray-500">{doc.originalFilename}</p>
                    <p className="text-sm text-gray-500">
                      Uploaded on {new Date(doc.createdAt).toLocaleDateString()}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <button
                    onClick={() => handleDelete(doc.uploadId)}
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