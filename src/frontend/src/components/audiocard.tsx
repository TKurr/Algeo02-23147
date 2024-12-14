// components/audiocard.tsx
'use client';
import React, {useState, useEffect} from "react";
import Image from "next/image";
import Link from "next/link";

export function AudioCard({songs} : {songs: any}) {
    const {name, artist, album, duration, image} = songs;
    const defaultImage = "/food.jpg"
    return ( 
        <div className="flex items-center p-4 bg-gray-300 rounded-lg shadow-md">
            <img 
                src={defaultImage} 
                alt={name} 
                className="w-16 h-16 rounded-md object-cover" 
            />
            <div className="ml-4">
                <div className="text-lg font-semibold text-black">{name}</div>
                <div className="text-gray-600">{artist}</div>
            </div>
            <div className="ml-auto flex items-center space-x-2">
                <button className="flex items-center px-3 py-1 bg-black text-white rounded-full">
                <i className="fab fa-apple mr-1"></i> Music
                </button>
                <i className="fas fa-ellipsis-v text-gray-600"></i>
            </div>
        </div>
    );
}