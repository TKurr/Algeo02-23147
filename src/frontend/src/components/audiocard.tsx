'use client';
import React, {useState, useEffect} from 'react';

export function AudioCard({index}){
    return (
        <div className="bg-gray-800 p-4 rounded-lg flex flex-col items-center">
            <img src="https://placehold.co/150x100" alt={`audio${index + 1}.wav`} className="w-full h-24 object-cover rounded-lg mb-2" />
            <p className="mb-2">audio{index + 1}.wav</p>
            <button className="bg-blue-600 hover:bg-blue-700 text-white py-1 px-2 rounded-full">
                <i className="fas fa-play"></i>
            </button>
        </div>
    );
};