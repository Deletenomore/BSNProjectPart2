// app/layout.tsx
import '../public/styles.css';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <main className="container">
          <header>
            <h1>AI Data Interaction Platform</h1>
          </header>
          {children}
        </main>
      </body>
    </html>
  );
}
