'use client'
import { useState } from 'react';

interface Result {
  file_name: string;
  similarity_score: number;
}

export default function UploadMIDI() {
  const [file, setFile] = useState<File | null>(null);
  const [results, setResults] = useState<Result[] | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  // Handle file selection
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0] || null;
    setFile(selectedFile);
  };

  // Upload file to the backend Flask API
  const handleUpload = async () => {
    if (!file) {
      alert('Please select a MIDI file first!');
      return;
    }

    const formData = new FormData();
    formData.append('query_file', file);

    try {
      setLoading(true);
      const response = await fetch('http://localhost:5000/compare_midi', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setResults(data.results); // Store the results
      } else {
        alert(`Error: ${data.error}`);
      }
    } catch (error) {
      console.error('Upload failed:', error);
      alert('Failed to connect to the server.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>MIDI File Comparison</h1>
      <input
        type="file"
        accept=".mid,.midi"
        onChange={handleFileChange}
      />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? 'Uploading...' : 'Upload and Compare'}
      </button>

      {results && (
        <div>
          <h2>Comparison Results</h2>
          <ul>
            {results.map((result, index) => (
              <li key={index}>
                {result.file_name}: {result.similarity_score}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
