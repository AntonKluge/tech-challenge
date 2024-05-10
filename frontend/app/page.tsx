import Typography from '@/components/typography';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { UploadCloudIcon } from 'lucide-react';

export default function Home() {
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

      <div className="flex items-center justify-center w-full">
        <label className="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 dark:hover:bg-bray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600">
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
          <input id="dropzone-file" type="file" className="hidden" />
        </label>
      </div>
    </main>
  );
}
