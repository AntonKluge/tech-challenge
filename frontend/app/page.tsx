import ImageClassification from '@/components/image-classification';
import Typography from '@/components/typography';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';

export default function Home() {
  return (
    <main className="flex min-h-screen w-full flex-col p-8">
      <Typography.H1>ReLoom</Typography.H1>

      <Alert className="my-7">
        <AlertTitle>🎉 Welcome to ReLoom! 🎉</AlertTitle>
        <AlertDescription>
          At ReLoom, we leverage AI to identify and price used clothing.
          <br />
          We classify your products from images, providing accurate brand
          identification and resale price predictions.
          <br />
          <br />
          Happy reselling and happy planet-saving! 🌍 📸🛍️👗👕
        </AlertDescription>
      </Alert>

      <ImageClassification />
    </main>
  );
}
