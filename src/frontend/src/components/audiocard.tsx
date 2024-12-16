import React, { useState } from "react";

interface CardProps {
  name: string;
  score: number;
  onPlay: (isPlaying: boolean) => void; // Pass the state to handle play/stop
  imageUrl: string;
}

const Card: React.FC<CardProps> = ({ name, score, onPlay, imageUrl }) => {
  const [isPlaying, setIsPlaying] = useState(false);

  const handleTogglePlay = () => {
    const newPlayState = !isPlaying;
    setIsPlaying(newPlayState);
    onPlay(newPlayState); // Notify parent whether to play or stop
  };

  return (
    <div className="p-4 bg-[#1e2139] rounded-lg shadow-md text-white text-center">
      <img
        src={imageUrl}
        alt={name}
        className="w-full h-48 object-cover rounded mb-4"
      />
      <h3 className="text-lg font-bold">{name}</h3>
      <button
        onClick={handleTogglePlay}
        className="mt-2 px-4 py-2 bg-[#61dafb] text-[#0b0e26] rounded hover:bg-[#3ca8e0] transition"
      >
        {isPlaying ? "Stop" : "Play"}
      </button>
    </div>
  );

  // return (
  //   <div className="bg-[#1e2348] text-center p-4 rounded-lg shadow-md">
  //     <div className="text-sm text-[#c0c5d6] mb-2">{name}</div>
  //     <button
  //       onClick={handleTogglePlay}
  //       className="mt-2 px-3 py-1 bg-[#61dafb] text-[#0b0e26] font-bold rounded hover:bg-[#3ca8e0] transition"
  //     >
  //       {isPlaying ? "Stop" : "Play"}
  //     </button>
  //   </div>
  // );
};

export default Card;
