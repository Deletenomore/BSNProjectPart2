// frontend/app/components/ResultDisplay.tsx
"use client";

import { useState, useEffect } from 'react';

export default function ResultDisplay() {
  const [results, setResults] = useState<string>('');

  useEffect(() => {
    async function fetchResults() {
      const res = await fetch('http://localhost:8000/results');
      const data = await res.json();
      setResults(data.results);
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
