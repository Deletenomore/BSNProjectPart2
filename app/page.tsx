// app/page.tsx
import FileUpload from './components/FileUpload';
import Chatbot from './components/Chatbot';
import ResultDisplay from './components/ResultDisplay';

export default function Home() {
  return (
    <div>
      <FileUpload />
      <Chatbot />
      <ResultDisplay />
    </div>
  );
}
