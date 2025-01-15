import React, { useState } from 'react';
import { FileUp, Loader2 } from 'lucide-react';

interface FileUploadProps {
  onUpload: (file: File) => Promise<void>;
  loading?: boolean;
  error?: string | null;
  accept?: string;
  maxFileSize?: number;
}

const FileUpload: React.FC<FileUploadProps> = ({ 
  onUpload, 
  loading = false,
  error = null,
  accept = '.pdf',
  maxFileSize = 50 * 1024 * 1024 // 50MB default
}) => {
  const [file, setFile] = useState<File | null>(null);
  const [validationError, setValidationError] = useState<string>('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setValidationError('');
    const selectedFile = e.target.files?.[0];
    
    if (!selectedFile) return;

    // Validate file type
    if (!selectedFile.type.match(new RegExp(accept.replace('*', '.*')))) {
      setValidationError('Invalid file type');
      return;
    }

    // Validate file size
    if (selectedFile.size > maxFileSize) {
      setValidationError(`File must be less than ${maxFileSize / (1024 * 1024)}MB`);
      return;
    }

    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) return;
    await onUpload(file);
    setFile(null);
  };

  const displayError = validationError || error;

  return (
    <div className="border-2 border-dashed border-gray-300 rounded-lg p-6">
      <div className="flex flex-col items-center">
        <FileUp className="h-12 w-12 text-gray-400" />
        <label className="mt-4 cursor-pointer">
          <span className="mt-2 text-base leading-normal px-4 py-2 bg-nivaltaBlue text-white rounded-lg hover:bg-indigo-600 transition">
            Select File
          </span>
          <input
            type="file"
            className="hidden"
            accept={accept}
            onChange={handleFileChange}
          />
        </label>
      </div>

      {displayError && (
        <div className="mt-4 text-sm text-red-600">
          {displayError}
        </div>
      )}

      {file && (
        <div className="mt-4">
          <h3 className="font-medium mb-2">Selected File:</h3>
          <p className="text-sm text-gray-600">
            {file.name} ({(file.size / (1024 * 1024)).toFixed(2)}MB)
          </p>
          <button
            onClick={handleUpload}
            disabled={loading || !!validationError}
            className="mt-4 px-4 py-2 bg-nivaltaBlue text-white rounded-lg hover:bg-indigo-600 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            {loading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Uploading...
              </>
            ) : (
              'Upload File'
            )}
          </button>
        </div>
      )}
    </div>
  );
};

export default FileUpload;