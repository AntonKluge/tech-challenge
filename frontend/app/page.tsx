import branding from '@/branding/branding.json';
import ImageClassification from '@/components/image-classification';
import Typography from '@/components/typography';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';

export default function Home() {
  return (
    <main className="flex min-h-screen w-full flex-col p-8">
      <Typography.H1>{branding.name}</Typography.H1>

      <Alert className="my-7">
        <AlertTitle>{branding.callout_title}</AlertTitle>
        <AlertDescription>{branding.callout_description}</AlertDescription>
      </Alert>

      <ImageClassification />
    </main>
  );
}
