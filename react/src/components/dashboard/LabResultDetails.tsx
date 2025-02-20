import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { ChevronLeft, ChevronRight, AlertCircle } from 'lucide-react';
import { ocrAPI } from '../../lib/api/ocr';

interface Page {
 pageNumber: number;
 status: 'complete' | 'pending' | 'failed';
}

const LabResultDetails = () => {
 const { docId } = useParams();
 const [pages, setPages] = useState<Page[]>([]);
 const [currentPage, setCurrentPage] = useState(0);
 const [currentPageText, setCurrentPageText] = useState<string>('');
 const [loading, setLoading] = useState(true);
 const [error, setError] = useState<string | null>(null);

 const [stats, setStats] = useState({
   complete: 0,
   pending: 0,
   failed: 0
 });

 useEffect(() => {
   const fetchPages = async () => {
     try {
       setLoading(true);
       const response = await ocrAPI.getPages(docId!);
       setPages(response);
       
       // Calculate stats
       const statusCounts = response.reduce((acc, page) => {
         acc[page.status]++;
         return acc;
       }, { complete: 0, pending: 0, failed: 0 });
       
       setStats(statusCounts);
     } catch (err) {
       console.error('Error fetching pages:', err);
       setError('Failed to load document pages');
     } finally {
       setLoading(false);
     }
   };

   if (docId) {
     fetchPages();
   }
 }, [docId]);

 useEffect(() => {
   if (docId && pages.length > 0) {
     fetchPageText(0);
   }
 }, [docId, pages]);

 const fetchPageText = async (pageNumber: number) => {
   try {
     setError(null);
     setLoading(true);
     const page = await ocrAPI.getPage(docId!, pageNumber);
     const combinedText = page.raw_data.text.join('\n');
     setCurrentPageText(combinedText);
   } catch (err) {
     setError('Failed to fetch page text');
     console.error('Fetch page text error:', err);
   } finally {
     setLoading(false);
   }
 };

 const handlePageChange = async (pageNumber: number) => {
   if (pageNumber >= 0 && pageNumber < pages.length) {
     setCurrentPage(pageNumber);
     await fetchPageText(pageNumber);
   }
 };

 if (loading && pages.length === 0) return <div>Loading...</div>;
 if (error && pages.length === 0) return <div className="text-red-500">{error}</div>;

 const currentPageData = pages[currentPage];

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
           <h3 className="font-medium">Page {currentPage + 1}</h3>
           <div className="flex gap-2">
             <button
               onClick={() => handlePageChange(currentPage - 1)}
               disabled={currentPage === 0}
               className="p-2 rounded hover:bg-gray-100 disabled:opacity-50"
             >
               <ChevronLeft className="h-5 w-5" />
             </button>
             <span className="py-2">
               {currentPage + 1} / {pages.length}
             </span>
             <button
               onClick={() => handlePageChange(currentPage + 1)}
               disabled={currentPage === pages.length - 1}
               className="p-2 rounded hover:bg-gray-100 disabled:opacity-50"
             >
               <ChevronRight className="h-5 w-5" />
             </button>
           </div>
         </div>
         <div className="bg-gray-100 h-96">
           <img
             src={`/api/ocr/pages/${docId}/${currentPage}/image`}
             alt={`Page ${currentPage + 1}`}
             className="w-full h-full object-contain"
           />
         </div>
       </div>

       {/* OCR Text */}
       <div className="border rounded p-4">
         <div className="flex justify-between items-center mb-4">
           <h3 className="font-medium text-black">Extracted Text</h3>
           {currentPageData.status === 'failed' && (
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