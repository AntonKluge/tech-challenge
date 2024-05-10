'use client';

import ImageDropzone from '@/components/image-dropzone';
import Typography from '@/components/typography';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { useState } from 'react';
import { toast } from 'sonner';

type ClassificationResult = {
  model: string;
  producer: string;
};

export default function Home() {
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [classificationResult, setClassificationResult] =
    useState<ClassificationResult | null>(null);

  const handleUploadImage = async (image: File) => {
    toast.promise(uploadImage(image), {
      loading: 'Uploading image...',
      success: 'Image uploaded successfully!',
      error: 'Failed to upload image.',
    });
  };

  const uploadImage = async (image: File) => {
    const formData = new FormData();
    formData.append('file', image);

    const res = await fetch('/api/classify', {
      method: 'POST',
      body: formData,
    });

    const data = await res.json();

    console.log(data);

    setClassificationResult(data);
    setIsDialogOpen(true);
  };

  return (
    <main className="flex min-h-screen w-full flex-col p-8">
      <Typography.H1>Recommerce</Typography.H1>

      <Alert className="my-7">
        <AlertTitle>
          🎉 Welcome to Our Style Snapshot Recommerce Platform! 🎉
        </AlertTitle>
        <AlertDescription>
          Perfect style is just a click away! Upload a snapshot, and let our
          cutting-edge AI discover your fashion desires.
          <br />
          Jump into our vast collection of preloved treasures and enjoy a
          shopping experience that is easy, eco-friendly, and excitingly unique.
          <br />
          Get started, add a fabulous preloved piece to your wardrobe, and join
          the fashion revolution.
          <br />
          <br />
          Happy shopping and happy planet-saving! 🌍 📸🛍️👗👕
        </AlertDescription>
      </Alert>

      <ImageDropzone onImageUpload={handleUploadImage} />

      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>We successfully classified your image 🎉</DialogTitle>
            <DialogDescription>
              Please keep in mind that this is a demo, and the classification
              results are not 100% accurate.
            </DialogDescription>
          </DialogHeader>
          <div className="flex flex-col gap-2 text-sm text-foreground">
            <p>
              <span className="font-bold">Model:</span>{' '}
              {classificationResult?.model}
            </p>
            <p>
              <span className="font-bold">Producer:</span>{' '}
              {classificationResult?.producer}
            </p>
          </div>
          <DialogFooter>
            <Button onClick={() => setIsDialogOpen(false)}>Close</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </main>
  );
}
