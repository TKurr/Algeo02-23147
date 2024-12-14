// components/Card.tsx
import React from "react";

interface CardProps {
  name: string;
  score: number;
}

const Card: React.FC<CardProps> = ({ name, score }) => {
  return (
    <div className="card">
      <div className="file-name">{name}</div>
      <div className="score">{score.toFixed(5)}</div>
      <style jsx>{`
        .card {
          background-color: #1e2348;
          border-radius: 8px;
          padding: 12px;
          text-align: center;
          box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .file-name {
          font-size: 14px;
          margin-bottom: 8px;
          color: #c0c5d6;
        }
        .score {
          font-size: 18px;
          font-weight: bold;
          color: #61dafb;
        }
      `}</style>
    </div>
  );
};

export default Card;
