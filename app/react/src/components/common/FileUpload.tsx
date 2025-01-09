import React, { useState } from 'react';
import { FileUp, Loader2 } from 'lucide-react';

interface FileUploadProps {
  onUpload: (files: File[]) => Promise<void>;
  isUploading: boolean;
  accept?: string;
  multiple?: boolean;
}

const FileUpload: React.FC<FileUploadProps> = ({ 
  onUpload, 
  isUploading, 
  accept = '.pdf', 
  multiple = true 
}) => {
  const [files, setFiles] = useState<File[]>([]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = Array.from(e.target.files || []);
    const validFiles = selectedFiles.filter(file => {
      const fileType = file.type || '';
      return accept.split(',').some(type => 
        fileType.match(new RegExp(type.trim().replace('*', '.*')))
      );
    });
    setFiles(validFiles);
  };

  const handleUpload = async () => {
    if (!files.length) return;
    try {
      await onUpload(files);
      setFiles([]); // Clear files after successful upload
    } catch (error) {
      console.error('Upload failed:', error);
    }
  };

  return (
    <div className="border-2 border-dashed border-gray-300 rounded-lg p-6">
      <div className="flex flex-col items-center">
        <FileUp className="h-12 w-12 text-gray-400" />
        <label className="mt-4 cursor-pointer">
          <span className="mt-2 text-base leading-normal px-4 py-2 bg-nivaltaBlue text-white rounded-lg hover:bg-indigo-600 transition">
            Select Files
          </span>
          <input
            type="file"
            className="hidden"
            multiple={multiple}
            accept={accept}
            onChange={handleFileChange}
          />
        </label>
      </div>

      {files.length > 0 && (
        <div className="mt-4">
          <h3 className="font-medium mb-2">Selected Files:</h3>
          <ul className="space-y-2">
            {files.map((file, index) => (
              <li key={index} className="text-sm text-gray-600">
                {file.name}
              </li>
            ))}
          </ul>
          <button
            onClick={handleUpload}
            disabled={isUploading}
            className="mt-4 px-4 py-2 bg-nivaltaBlue text-white rounded-lg hover:bg-indigo-600 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            {isUploading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Uploading...
              </>
            ) : (
              'Upload Files'
            )}
          </button>
        </div>
      )}
    </div>
  );
};

export default FileUpload;