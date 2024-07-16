# Frontend

## Tech Stack
- [Next.js](https://nextjs.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [TypeScript](https://www.typescriptlang.org/)
- [shadcn/ui](https://ui.shadcn.com/)

## Structure
- `app/` - Contains the main page and starting point of the application.
- `components/` - Contains the reusable components used throughout the application.
- `components/ui` - Contains the UI components from `shadcn/ui`.
- `components/image-classification.tsx` - Contains the image classification api call and stream processing.
- `lib/image-classification.types.ts` - Contains the types for the image classification API.

## API Stream Processing
The image classification API is called with the image data and the response is processed in a stream. 
The stream is used to update the UI with the classification results as they are received.
Each classification result contains a `data_description` which is used to determine the type of data being received.
Examples of data types include `model-producer`, `producer-url` or `estimated-price`.
For each data type, a different UI component is rendered to display the data.

## Branding
The application can be easily rebranded by configuring the `branding/branding.json` file.
The file contains the following fields:

- `name`: The name of the application or the company.
- `logo_url`: The URL of the logo image.
- `logo_alt`: The alt text for the logo image.
- `callout_title`: The title displayed on the main page.
- `callout_description`: The description displayed on the main page.

After configuring the branding file, the application will automatically update with the new branding.