'use client';
import { useState } from 'react';
import Card from '@/components/audiocard';
import { midiPlayer } from '@/utils/midiPlayer';

interface Result {
  file_name: string;
  similarity_score: number;
}

export default function UploadMIDI() {
  const [file, setFile] = useState<File | null>(null);
  const [results, setResults] = useState<Result[] | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [currentPage, setCurrentPage] = useState<number>(1);

  const itemsPerPage = 9;
  const totalPages = results ? Math.ceil(results.length / itemsPerPage) : 1;

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0] || null;
    setFile(selectedFile);
  };

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
        setResults(data.results);
        setCurrentPage(1); // Reset to the first page
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

  const handlePlay = (fileName: string) => (isPlaying: boolean) => {
    if (isPlaying) {
      const fileUrl = `http://localhost:5000/get_midi/${fileName}`;
      midiPlayer.playFileFromURL(fileUrl, () => {
        console.log("Playback finished.");
      });
    } else {
      midiPlayer.stop();
      console.log("Playback stopped.");
    }
  };

  const handlePageChange = (newPage: number) => {
    setCurrentPage(newPage);
  };

  const paginatedResults = results?.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  return (
    <div className="min-h-screen bg-[#0b0e26] text-white text-center p-6 font-sans">
      <h1 className="text-3xl font-bold mb-6">MIDI File Comparison</h1>
      <input
        type="file"
        accept=".mid,.midi"
        onChange={handleFileChange}
        className="block mx-auto mb-4 text-white file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:bg-[#61dafb] file:text-[#0b0e26] hover:file:bg-[#3ca8e0] transition"
      />
      <button
        onClick={handleUpload}
        disabled={loading}
        className={`px-4 py-2 rounded font-bold transition ${
          loading
            ? 'bg-[#4b4e67] cursor-not-allowed'
            : 'bg-[#61dafb] text-[#0b0e26] hover:bg-[#3ca8e0]'
        }`}
      >
        {loading ? 'Uploading...' : 'Upload and Compare'}
      </button>

      {results && (
        <div>
          <h2 className="text-2xl font-bold text-[#61dafb] mt-8 mb-4">
            Comparison Results
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {paginatedResults?.map((result, index) => (
              <Card
                key={index}
                name={result.file_name}
                score={result.similarity_score}
                onPlay={handlePlay(result.file_name)}
              />
            ))}
          </div>
          <div className="flex justify-center items-center mt-4 space-x-2">
            <button
              onClick={() => handlePageChange(currentPage - 1)}
              disabled={currentPage === 1}
              className="px-4 py-2 bg-[#4b4e67] rounded text-white hover:bg-[#3ca8e0] transition disabled:opacity-50"
            >
              Previous
            </button>
            <span>
              Page {currentPage} of {totalPages}
            </span>
            <button
              onClick={() => handlePageChange(currentPage + 1)}
              disabled={currentPage === totalPages}
              className="px-4 py-2 bg-[#4b4e67] rounded text-white hover:bg-[#3ca8e0] transition disabled:opacity-50"
            >
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
