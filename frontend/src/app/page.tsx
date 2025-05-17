'use client';

import React, { useState } from 'react';

export default function Home() {
  const [text, setText] = useState('');

 const [result, setResult] = useState<{
    sentiment: string;
    likes: number;
    retweets: number;
    hashtags?: string[];  
  } | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    setLoading(true);
    setError('');
    setResult(null);
    

    try {
      const res = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });

      if (!res.ok) throw new Error('Server error');
      const data = await res.json();
      setResult(data);
    } catch (err: any) {
      setError('Failed to fetch prediction. Is the backend running?');
    }

    setLoading(false);
  };

  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-900 via-black to-gray-900 p-4">
      <div className="bg-white/10 backdrop-blur-md shadow-2xl border border-white/20 rounded-2xl p-8 w-full max-w-lg text-white transition-all duration-300">
        <h1 className="text-3xl font-bold mb-6 text-center tracking-wide">Sentiment & Engagement Predictor</h1>

        <textarea
          className="w-full bg-black/30 border border-gray-500 text-white rounded-xl p-3 mb-4 focus:outline-none focus:ring-2 focus:ring-purple-500"
          rows={5}
          placeholder="Write your tweet or comment here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <button
          onClick={handleSubmit}
          disabled={loading || !text}
          className="w-full bg-purple-600 hover:bg-purple-700 transition-all py-2 px-4 rounded-xl font-semibold text-white disabled:opacity-50"
        >
          {loading ? 'Analyzing...' : 'Predict Now 🚀'}
        </button>

        {error && (
          <p className="text-red-400 mt-4 text-sm text-center">{error}</p>
        )}
  {result && (
          <div className="mt-6 p-5 bg-white/10 border border-white/20 rounded-xl animate-fade-in">
            <p className="mb-2"><span className="font-semibold text-purple-400">Sentiment:</span> {result.sentiment}</p>
            <p className="mb-2"><span className="font-semibold text-blue-400">Estimated Likes:</span> {Math.round(result.likes)}</p>
            <p className="mb-2"><span className="font-semibold text-green-400">Estimated Retweets:</span> {Math.round(result.retweets)}</p>

            {result.hashtags && result.hashtags.length > 0 && (
              <div className="mt-3">
                <span className="font-semibold text-yellow-300">Suggested Hashtags: </span>
                {result.hashtags.map((tag, index) => (
                  <span
                    key={index}
                    className="inline-block bg-yellow-600 text-black rounded px-2 py-1 mr-2 mt-2"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </main>
  );
}