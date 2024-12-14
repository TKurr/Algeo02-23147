'use client';
import { useState } from 'react';
import Card from '@/components/audiocard';

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
    <div className="container">
      <h1>MIDI File Comparison</h1>
      <input
        type="file"
        accept=".mid,.midi"
        onChange={handleFileChange}
      />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? 'Uploading...' : 'Upload and Compare'}
      </button>

      {/* Display Results in a Grid */}
      {results && (
        <div>
          <h2>Comparison Results</h2>
          <div className="card-container">
            {results.map((result, index) => (
              <Card
                key={index}
                name={result.file_name}
                score={result.similarity_score}
              />
            ))}
          </div>
        </div>
      )}

      {/* Styling */}
      <style jsx>{`
        .container {
          padding: 20px;
          text-align: center;
          background-color: #0b0e26;
          color: white;
          min-height: 100vh;
          font-family: Arial, sans-serif;
        }

        input {
          margin: 10px 0;
          color: white;
        }

        button {
          padding: 8px 16px;
          background-color: #61dafb;
          color: #0b0e26;
          border: none;
          border-radius: 4px;
          cursor: pointer;
          font-weight: bold;
          transition: background-color 0.3s;
        }

        button:disabled {
          background-color: #4b4e67;
          cursor: not-allowed;
        }

        button:hover:not(:disabled) {
          background-color: #3ca8e0;
        }

        .card-container {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
          gap: 16px;
          margin-top: 20px;
        }

        h2 {
          margin-top: 20px;
          color: #61dafb;
        }
      `}</style>
    </div>
  );
}
