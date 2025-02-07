import React, { useState, useEffect } from 'react';
import { AlertCircle, FileText, Trash2, RotateCw } from 'lucide-react';
import { Dialog, DialogTitle, DialogContent } from "../common/Dialog";
import { Alert, AlertDescription } from '../common/Alert';
import { documentsAPI } from '../../lib/api/files';
import { ocrAPI } from '../../lib/api/ocr';
import FileUpload from '../common/FileUpload';
import { useAuth } from '../../providers/AuthProvider';

interface Document {
  fileId: string; 
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
  const [documentStatuses, setDocumentStatuses] = useState<DocumentStatus[]>([]);
  const [selectedDoc, setSelectedDoc] = useState<Document | null>(null);
  const [totalPages, setTotalPages] = useState<number>(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [ocrText, setOcrText] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth();

  const fetchDocumentsWithStatus = async () => {
    if (!user) return;
    try {
      setError(null);
      setLoading(true);

      // First get documents
      const docs = await documentsAPI.getFiles(user.userId);
      setDocuments(docs);

      // Then try to get statuses
      try {
        const statusPromises = docs.map(async (doc) => {
          const status = await ocrAPI.getStatus(doc.fileId);
          return {
            ...doc,
            status
          };
        });
        const docsWithStatus = await Promise.all(statusPromises); 
        setDocuments(docsWithStatus);
        return docsWithStatus;
      } catch (statusErr) {
        setError('Failed to fetch document statuses');
        console.error('Error fetching statuses:', statusErr);
        return docs; // Return docs without status on error
      }

    } catch (err) {
      setError('Failed to fetch documents');
      console.error('Error fetching documents:', err);
    } finally {
      setLoading(false);
    }
    };
   
   useEffect(() => {
    fetchDocumentsWithStatus();
   }, [user]);

  const handleUpload = async (file: File) => {
    try {
      setError(null);
      setLoading(true);
      await documentsAPI.uploadFile(user.userId, file);
      await fetchDocumentsWithStatus();
    } catch (err) {
      setError('Failed to upload document');
      console.error('Upload error:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchPageText = async (doc: Document, pageNumber: number) => {
    try {
      setError(null);
      setLoading(true);
      const page = await ocrAPI.getPage(doc.fileId, currentPage-1);
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
    try {
      setSelectedDoc(doc);
      setCurrentPage(1);
      setLoading(true);
      const pages = await ocrAPI.getPages(doc.fileId);
      setTotalPages(pages.length);
      fetchPageText(doc, currentPage);
    } catch (err) {
      setError('Failed to fetch document pages');
      console.error('Fetch pages error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handlePageChange = async (pageNumber: number) => {
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
      await fetchDocumentsWithStatus();
    } catch (err) {
      setError('Failed to retry document processing');
      console.error('Retry error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (documentId: string) => {
    try {
      setError(null);
      setLoading(true);
      await documentsAPI.deleteFile(documentId);
      await ocrAPI.deletePages(documentId);
      await fetchDocumentsWithStatus();
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
                    onClick={() => handleRetry(doc.fileId)} 
                    className="text-gray-500 hover:text-gray-600"
                  >
                    <RotateCw className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => handleDelete(doc.fileId)}
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
      <Dialog open={selectedDoc !== null} onOpenChange={() => setSelectedDoc(null)}>
        <DialogTitle>
          <DialogContent className="min-w-[800px]">
            <div className="grid grid-cols-2 gap-4">
              <div className="border rounded p-4">
                <h3 className="font-medium mb-2">Page {currentPage}</h3>
                <div className="bg-gray-100 h-96">
                  {selectedDoc && (
                    <img
                      src={`/api/ocr/pages/${selectedDoc.fileId}/${currentPage-1}/image`}
                      alt={`Page ${currentPage}`}
                      className="w-full h-full object-contain"
                    />
                  )}
                </div>
              </div>
              <div className="border rounded p-4">
                <h3 className="font-medium mb-2">OCR Text</h3>
                <div className="bg-gray-100 h-96 text-black whitespace-pre-wrap overflow-auto p-4">
                  {ocrText}
                </div>
              </div>
            </div>
            <div className="flex justify-center gap-4 mt-4">
              <button
                onClick={() => handlePageChange(currentPage - 1)}
                className="px-4 py-2 border rounded"
                disabled={currentPage === 1}
              >
                Previous
              </button>
              <button
                onClick={() => handlePageChange(currentPage + 1)}
                className="px-4 py-2 border rounded"
                disabled={currentPage === totalPages || loading}
              >
                Next
              </button>
            </div>
          </DialogContent>
        </DialogTitle>
      </Dialog>
    </div>
  );
};

export default LabResults;