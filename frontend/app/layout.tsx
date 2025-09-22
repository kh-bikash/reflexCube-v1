// frontend/app/layout.tsx
import './globals.css'; // Assuming you'll have a globals.css for styling

export const metadata = {
  title: 'AutoModeler',
  description: 'Generate AI models from prompts',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}