import ImageClassification from '@/components/image-classification';
import Typography from '@/components/typography';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';

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

      <ImageClassification />
    </main>
  );
}
