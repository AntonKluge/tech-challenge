'use client';

import {
  ClassificationProduct,
  ClassificationProductDescription,
} from '@/lib/image-classification.types';
import { useMemo, useState } from 'react';
import { toast } from 'sonner';
import {
  ClassificationCardContent,
  ClassificationCardEstimatedPrice,
  ClassificationCardModelProducer,
  ClassificationCardProducerUrl,
  ClassificationCardRetailPrice,
  ClassificationCardSecondHandOffers,
} from './image-classification-product-cards';
import ImageDropzone from './image-dropzone';

export default function ImageClassification() {
  const [showClassifyCard, setShowClassifyCard] = useState(false);
  const [classificationResult, setClassificationResult] = useState<
    ClassificationProduct[]
  >([]);

  const appendClassificationResult = (result: ClassificationProduct) => {
    setClassificationResult((prev) => [...prev, result]);
  };

  const handleUploadImage = async (image: File) => {
    toast.promise(uploadImage(image), {
      loading: 'Uploading image...',
      success: 'Image uploaded successfully!',
      error: 'Failed to upload image.',
    });
  };

  const uploadImage = async (image: File) => {
    return new Promise<void>((resolve) => {
      const formData = new FormData();
      formData.append('file', image);

      fetch('http://localhost:3002/classify', {
        method: 'POST',
        body: formData,
      })
        .then(async (response) => {
          const reader = response.body?.getReader();
          if (!reader) {
            throw new Error('Failed to get reader from response body');
          }

          setShowClassifyCard(true);

          const decoder = new TextDecoder('utf-8');
          let buffer = '';

          const processStream = async ({
            done,
            value,
          }: ReadableStreamReadResult<Uint8Array>): Promise<void> => {
            if (done) {
              return;
            }

            buffer += decoder.decode(value, { stream: true });

            const parts = buffer.split('\n\n');
            buffer = parts.pop() || '';

            parts.forEach((part) => {
              if (part.trim()) {
                const data = part.replace(/^data: /, '');

                const parsedData: ClassificationProduct = JSON.parse(data);

                appendClassificationResult(parsedData);
              }
            });

            return reader.read().then(processStream);
          };

          return reader.read().then(processStream);
        })
        .then(resolve);
    });
  };

  return (
    <>
      <ImageDropzone onImageUpload={handleUploadImage} />

      {showClassifyCard && (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mt-8">
          {classificationResult.map((result, index) => (
            <ClassificationCard key={index} data={result} />
          ))}
        </div>
      )}
    </>
  );
}

function ClassificationCard({ data }: { data: ClassificationProduct }) {
  const buildCard = useMemo(() => {
    switch (data.data_description) {
      case 'model-producer':
        return <ClassificationCardModelProducer data={data.data} />;
      case 'retail-price-details':
        return <ClassificationCardRetailPrice data={data.data} />;
      case 'second-hand-offers':
        return <ClassificationCardSecondHandOffers data={data.data} />;
      case 'producer-url':
        return <ClassificationCardProducerUrl data={data.data} />;
      case 'estimated-price':
        return <ClassificationCardEstimatedPrice data={data.data} />;
      default:
        return <ClassificationCardContent data={data.data} />;
    }
  }, [data]);

  const cardTitle: Record<ClassificationProductDescription, string> = {
    'model-producer': 'Model Producer',
    'retail-price-details': 'Retail Price Details',
    'second-hand-offers': 'Second Hand Offers',
    'producer-url': 'Producer URL',
    'estimated-price': 'Estimated Price',
    unknown: 'Unknown',
  };

  return (
    <div className="bg-white rounded-lg border-gray-200 border-[1px] p-4 max-h-64 overflow-auto">
      <h2 className="text-lg font-bold">{cardTitle[data.data_description]}</h2>
      {buildCard}
    </div>
  );
}
