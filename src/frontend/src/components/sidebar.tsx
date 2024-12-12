'use client';

import React, {useState, useEffect} from 'react';

export function Sidebar(){
        return (
            <div className="flex">
            {/* Sidebar */}
            <div className="w-3/4 p-2">
                <div className="bg-gray-800 p-4 rounded-lg mb-4">
                    <img
                        src="https://placehold.co/150x150"
                        alt="Audio Thumbnail"
                        className="w-full h-32 object-cover rounded-lg mb-2"
                    />
                    <p className="text-center mb-2">Audio_Name.wav</p>
                    <button className="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg w-full mb-4">
                        Upload
                    </button>
                    <div className="space-y-2">
                        <button className="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg w-full">
                            Audios
                        </button>
                        <button className="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg w-full">
                            Pictures
                        </button>
                        <button className="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg w-full">
                            Mapper
                        </button>
                    </div>
                </div>
                <div className="bg-gray-800 p-4 rounded-lg">
                    <p>Audios: audios.zip</p>
                    <p>Pictures: pictures.zip</p>
                    <p>Mapper: mapper.txt</p>
                </div>
                <div className="bg-gray-800 p-4 rounded-lg mt-4">
                    <p>Page 1 of 120</p>
                </div>
            </div>
            </div>
        );
    };