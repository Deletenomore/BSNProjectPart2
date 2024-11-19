// frontend/app/components/ResultDisplay.tsx
"use client";

import { useState, useEffect } from 'react';

export default function ResultDisplay() {
  const [results, setResults] = useState<string>('');
  const [error,setError]=useState<string |null>(null);

  useEffect(() => {
    async function fetchResults():Promise<void> {
     try{ 
      const res = await fetch('http://localhost:8000/results/', {
        method: 'GET', // Explicitly specify GET
      });

      console.log('Response status:', res.status); // Log response status

      if(!res.ok){
        throw new Error(`Failed to fecth results: ${res.status} ${res.statusText}`);
      }
      const data:{results:string} = await res.json();
      setResults(data.results);
    }catch (error:unknown){
        const message = error instanceof Error ? error.message:'Unknown error occurred';
        setError(message);
    }
  }
    fetchResults();
  }, []);

  return (
    <section className="result-display">
      <h2>Results</h2>
      <pre>{results}</pre>
    </section>
  );
}
