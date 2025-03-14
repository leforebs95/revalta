import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ChevronLeft, ChevronRight, AlertCircle } from 'lucide-react';
import { ocrAPI } from '../../lib/api/ocr';
import { useAuth } from '../../hooks/useAuth';

interface Page {
  fileId: string;
  pageId: string;
  pageNumber: number;
  textContent: string;
  status: 'complete' | 'pending' | 'failed';
}

const LabResultDetails = () => {
  const { docId } = useParams();
  const navigate = useNavigate();
  const { user, isLoading } = useAuth();
  const [pages, setPages] = useState<Page[]>([]);
  const [currentPage, setCurrentPage] = useState<Page | undefined>();
  const [currentPageText, setCurrentPageText] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [stats, setStats] = useState({
    complete: 0,
    pending: 0,
    failed: 0
  });

  useEffect(() => {
    if (!isLoading && !user) {
      navigate('/login');
      return;
    }

    const fetchPages = async () => {
      try {
        setLoading(true);
        const response = await ocrAPI.getDocument(docId!);
        const filteredPages = response.map((page: any) => ({
          pageId: page.page_id,
          pageNumber: page.page_number,
          textContent: page.text_content,
          fileId: page.file_id
        }));
        setPages(filteredPages);
        if (filteredPages.length > 0) {
          setCurrentPage(filteredPages[0]);
          setCurrentPageText(filteredPages[0].textContent);
        }
         
        // Calculate stats
        const statusCounts = await ocrAPI.getStatus(docId!);
        setStats(statusCounts);
      } catch (err) {
        console.error('Error fetching pages:', err);
        setError('Failed to load document pages');
      } finally {
        setLoading(false);
      }
    };

    if (docId && !isLoading) {
      fetchPages();
    }
  }, [docId, user, navigate, isLoading]);

  const handlePageChange = async (pageNumber: number) => {
    if (pageNumber >= 0 && pageNumber < pages.length) {
      const page = pages.find(p => p.pageNumber === pageNumber);
      if (page) {
        setCurrentPage(page);
        setCurrentPageText(page.textContent);
      }
    }
  };

  if (loading && pages.length === 0) return <div>Loading...</div>;
  if (error && pages.length === 0) return <div className="text-red-500">{error}</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-semibold">Document Details</h2>
        <div className="flex gap-4">
          <div className="px-4 py-2 bg-green-100 rounded text-black">
            <span className="font-medium">{stats.complete}</span> Complete
          </div>
          <div className="px-4 py-2 bg-yellow-100 rounded text-black">
            <span className="font-medium">{stats.pending}</span> Pending
          </div>
          <div className="px-4 py-2 bg-red-100 rounded text-black">
            <span className="font-medium">{stats.failed}</span> Failed
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        {/* Page View */}
        <div className="border rounded p-4">
          <div className="flex justify-between items-center mb-4">
            <h3 className="font-medium">Page {currentPage?.pageNumber ? currentPage.pageNumber + 1 : 0}</h3>
            <div className="flex gap-2">
              <button
                onClick={() => handlePageChange(currentPage?.pageNumber ?? 0 - 1)}
                disabled={!currentPage || currentPage.pageNumber === 0}
                className="p-2 rounded hover:bg-gray-100 disabled:opacity-50"
              >
                <ChevronLeft className="h-5 w-5" />
              </button>
              <span className="py-2">
                {currentPage?.pageNumber ? currentPage.pageNumber + 1 : 0} / {pages.length}
              </span>
              <button
                onClick={() => handlePageChange(currentPage?.pageNumber ?? 0 + 1)}
                disabled={!currentPage || currentPage.pageNumber === pages.length - 1}
                className="p-2 rounded hover:bg-gray-100 disabled:opacity-50"
              >
                <ChevronRight className="h-5 w-5" />
              </button>
            </div>
          </div>
          <div className="bg-gray-100 h-96">
            {currentPage && (
              <img
                src={`/api/ocr/page/${currentPage.pageId}/image`}
                alt={`Page ${currentPage.pageNumber + 1}`}
                className="w-full h-full object-contain"
              />
            )}
          </div>
        </div>

        {/* OCR Text */}
        <div className="border rounded p-4">
          <div className="flex justify-between items-center mb-4">
            <h3 className="font-medium text-black">Extracted Text</h3>
            {currentPage?.status === 'failed' && (
              <div className="flex items-center text-red-500">
                <AlertCircle className="h-4 w-4 mr-2" />
                OCR Failed
              </div>
            )}
          </div>
          <div className="bg-gray-100 h-96 p-4 overflow-auto whitespace-pre-wrap text-black">
            {loading ? (
              'Loading...'
            ) : error ? (
              <div className="text-red-500">{error}</div>
            ) : (
              currentPageText
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LabResultDetails;