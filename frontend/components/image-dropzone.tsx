'use client';

import { cn } from '@/lib/utils';
import { Brain, Trash2, UploadCloudIcon } from 'lucide-react';
import { useCallback, useMemo, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Button } from './ui/button';

const CANDIDATE_IMAGE_MAX_FILE_SIZE_MB = 2;
const CANDIDATE_IMAGE_MAX_FILE_SIZE =
  CANDIDATE_IMAGE_MAX_FILE_SIZE_MB * 1024 * 1024;

const ACCEPTED_FILE_TYPES = {
  'image/jpeg': ['.jpg'],
  'image/png': ['.png'],
  'image/webp': ['.webp'],
};

type Props = {
  onImageUpload: (image: File) => void;
};

export default function ImageDropzone({ onImageUpload }: Props) {
  const [image, setImage] = useState<File | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (!acceptedFiles.length) return setImage(null);

    setImage(acceptedFiles[0]);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: ACCEPTED_FILE_TYPES,
    multiple: false,
    maxFiles: 1,
    maxSize: CANDIDATE_IMAGE_MAX_FILE_SIZE,
    noClick: !!image,
  });

  const selectedImageUrl = useMemo(() => {
    return image && URL.createObjectURL(image);
  }, [image]);

  const resetImage = () => {
    setImage(null);
  };

  return (
    <div className="flex items-center justify-center w-full">
      <label
        {...getRootProps()}
        className={cn(
          'relative overflow-hidden flex flex-col items-center justify-center w-full h-64 border-2 border-dashed rounded-lg transition-colors',
          isDragActive
            ? 'border-gray-500 bg-gray-100'
            : 'border-gray-300 bg-gray-50',
          !image && 'hover:bg-gray-100 cursor-pointer'
        )}
      >
        {!selectedImageUrl ? (
          <div className="flex flex-col items-center justify-center pt-5 pb-6">
            <UploadCloudIcon className="w-12 h-12 text-gray-400 dark:text-gray-500 mb-2" />
            <p className="mb-2 text-sm text-gray-500 dark:text-gray-400">
              <span className="font-semibold">Click to upload</span> or drag and
              drop
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Only Image files are supported
            </p>
          </div>
        ) : (
          <div className="flex flex-col gap-4 items-center justify-center h-full">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              className="object-contain h-1/2"
              src={selectedImageUrl}
              alt={image?.name ?? 'Selected Image'}
            />
            <div className="flex gap-4">
              <Button className="mt-2" onClick={resetImage} variant="outline">
                <Trash2 className="size-4 mr-1" />
                Remove
              </Button>
              <Button className="mt-2" onClick={() => onImageUpload(image!)}>
                <Brain className="size-4 mr-1" />
                Find Item
              </Button>
            </div>
          </div>
        )}
        <input {...getInputProps()} />
      </label>
    </div>
  );
}
