'use client';

import React, { useState } from 'react';

export default function AudioSearcher() {
  const [selectedTab, setSelectedTab] = useState('Music');

  // Dummy data for audios
  const audios = [
    'audio1.wav',
    'audio2.wav',
    'audio3.wav',
    'audio4.wav',
    'audio5.wav',
    'audio6.wav',
    'audio7.wav',
    'audio8.wav',
    'audio9.wav',
    'audio10.wav',
    'audio11.wav',
    'audio12.wav',
  ];

  return (
    <div className="w-full h-screen bg-lavender-900 bg-opacity-45 text-white flex">
      {/* Sidebar */}
      <div className="w-[20%] h-full bg-lavender-800 bg-opacity-50 p-4 flex flex-col">
        <div className="mb-4">
          <img
            src="https://placehold.co/150x150"
            alt="Audio Thumbnail"
            className="w-full h-32 object-cover rounded-lg mb-4"
          />
          <p className="text-center mb-4">Audio_Name.wav</p>
          <button className="bg-lavender-600 hover:bg-lavender-700 text-white py-2 px-4 rounded-lg w-full mb-4">
            Upload
          </button>
        </div>
        <div className="space-y-2 mb-4">
          <button className="bg-lavender-600 hover:bg-lavender-700 text-white py-2 px-4 rounded-lg w-full">
            Audios
          </button>
          <button className="bg-lavender-600 hover:bg-lavender-700 text-white py-2 px-4 rounded-lg w-full">
            Pictures
          </button>
          <button className="bg-lavender-600 hover:bg-lavender-700 text-white py-2 px-4 rounded-lg w-full">
            Mapper
          </button>
        </div>
        <div className="mt-auto">
          <p>Audios: audios.zip</p>
          <p>Pictures: pictures.zip</p>
          <p>Mapper: mapper.txt</p>
          <p className="mt-4">Page 1 of 120</p>
        </div>
      </div>

      {/* Main Content */}
      <div className="w-[80%] h-full p-4 flex flex-col">
        {/* Tabs */}
        <div className="flex space-x-4 mb-4">
          <button
            onClick={() => setSelectedTab('Album')}
            className={`py-2 px-4 rounded-lg ${
              selectedTab === 'Album' ? 'bg-lavender-600' : 'bg-lavender-700'
            }`}
          >
            Album
          </button>
          <button
            onClick={() => setSelectedTab('Music')}
            className={`py-2 px-4 rounded-lg ${
              selectedTab === 'Music' ? 'bg-lavender-600' : 'bg-lavender-700'
            }`}
          >
            Music
          </button>
        </div>

        {/* Audio Grid */}
        <div className="grid grid-cols-4 gap-4 flex-1 overflow-y-auto">
          {audios.map((audio, index) => (
            <div
              key={index}
              className="bg-lavender-700 rounded-lg p-4 text-center flex flex-col items-center"
            >
              <div className="w-24 h-16 bg-gray-300 rounded-lg mb-2"></div>
              <p className="mb-2">{audio}</p>
              <button className="bg-lavender-500 hover:bg-lavender-600 text-white py-1 px-3 rounded-lg">
                ▶
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
