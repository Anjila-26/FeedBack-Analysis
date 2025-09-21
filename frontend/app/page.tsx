'use client';

import React, { useState } from 'react';
import Link from 'next/link';

interface Feedback {
  user_id?: string;
  rating: number;
  comment: string;
  timestamp?: string;
  category?: string;
}

const FeedbackInterface: React.FC = () => {
  const [feedback, setFeedback] = useState<Feedback>({
    rating: 0,
    comment: '',
    category: 'general'
  });
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (feedback.rating === 0 || !feedback.comment.trim() || !feedback.user_id?.trim()) {
      return;
    }

    const finalFeedback: Feedback = {
      ...feedback,
      timestamp: new Date().toISOString()
    };

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/feedback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(finalFeedback),
      });

      if (response.ok) {
        console.log('Feedback submitted successfully:', finalFeedback);
        setSubmitted(true);

        // Reset form after 3 seconds
        setTimeout(() => {
          setSubmitted(false);
          setFeedback({
            rating: 0,
            comment: '',
            category: 'general'
          });
        }, 3000);
      } else {
        console.error('Failed to submit feedback');
        alert('Failed to submit feedback. Please try again.');
      }
    } catch (error) {
      console.error('Error submitting feedback:', error);
      alert('Error submitting feedback. Please check your connection and try again.');
    }
  };

  const handleRatingClick = (rating: number) => {
    setFeedback(prev => ({ ...prev, rating }));
  };

  if (submitted) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center p-4">
        <div className="max-w-md w-full text-center">
          <div className="text-6xl mb-4">⚓</div>
          <h2 className="text-3xl font-black mb-4 tracking-wider text-black">ARIGATOU!</h2>
          <p className="text-lg font-medium text-black">Your feedback has set sail!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white p-4 flex items-center justify-center">
      <div className="max-w-2xl w-full">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex justify-between items-start mb-4">
            <div></div>
            <div className="text-center">
              <div className="text-6xl mb-4">⚓</div>
              <h1 className="text-4xl font-black tracking-wider mb-2 text-black">FEEDBACK</h1>
              <div className="w-24 h-1 bg-black mx-auto"></div>
            </div>
            <Link
              href="/admin"
              className="px-4 py-2 bg-gray-800 text-white text-sm font-bold tracking-wide hover:bg-black transition-colors"
            >
              ADMIN →
            </Link>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-8">
          {/* User ID */}
          <div>
            <label className="block text-lg font-bold tracking-wide mb-3 text-black">
              NAKAMA ID
            </label>
            <input
              type="text"
              value={feedback.user_id || ''}
              onChange={(e) => setFeedback(prev => ({ ...prev, user_id: e.target.value }))}
              className="w-full p-4 border-4 border-black bg-white text-lg font-medium tracking-wide text-black focus:outline-none focus:bg-gray-50 transition-colors"
              placeholder="Your name..."
              required
            />
          </div>

          {/* Rating */}
          <div>
            <label className="block text-lg font-bold tracking-wide mb-4 text-black">
              POWER LEVEL RATING
            </label>
            <div className="flex gap-2 justify-center">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  key={star}
                  type="button"
                  onClick={() => handleRatingClick(star)}
                  className={`w-16 h-16 border-4 border-black transition-all duration-200 font-black text-2xl ${
                    feedback.rating >= star 
                      ? 'bg-black text-white' 
                      : 'bg-white text-black hover:bg-gray-100'
                  }`}
                >
                  ★
                </button>
              ))}
            </div>
            <div className="text-center mt-2 text-sm font-medium tracking-wide text-black">
              {feedback.rating === 0 && "Select your power level"}
              {feedback.rating === 1 && "WEAK"}
              {feedback.rating === 2 && "GETTING STRONGER"}
              {feedback.rating === 3 && "DECENT FIGHTER"}
              {feedback.rating === 4 && "STRONG WARRIOR"}
              {feedback.rating === 5 && "PIRATE KING LEVEL!"}
            </div>
          </div>

          {/* Category */}
          <div>
            <label className="block text-lg font-bold tracking-wide mb-3 text-black">
              REPORT TYPE
            </label>
            <div className="grid grid-cols-3 gap-2">
              {[
                { value: 'bug', label: 'BUG' },
                { value: 'feature', label: 'FEATURE' },
                { value: 'general', label: 'GENERAL' }
              ].map((cat) => (
                <button
                  key={cat.value}
                  type="button"
                  onClick={() => setFeedback(prev => ({ ...prev, category: cat.value }))}
                  className={`p-3 border-4 border-black font-bold tracking-wider transition-all ${
                    feedback.category === cat.value
                      ? 'bg-black text-white'
                      : 'bg-white text-black hover:bg-gray-100'
                  }`}
                >
                  {cat.label}
                </button>
              ))}
            </div>
          </div>

          {/* Comment */}
          <div>
            <label className="block text-lg font-bold tracking-wide mb-3 text-black">
              YOUR MESSAGE TO THE CREW
            </label>
            <textarea
              value={feedback.comment}
              onChange={(e) => setFeedback(prev => ({ ...prev, comment: e.target.value }))}
              rows={6}
              required
              className="w-full p-4 border-4 border-black bg-white text-lg font-medium tracking-wide text-black resize-none focus:outline-none focus:bg-gray-50 transition-colors"
              placeholder="Share your adventure with us..."
            />
          </div>

          {/* Submit */}
          <div className="text-center pt-4">
            <button
              type="submit"
              disabled={feedback.rating === 0 || !feedback.comment.trim() || !feedback.user_id?.trim()}
              className="px-12 py-4 bg-black text-white font-black text-xl tracking-wider border-4 border-black hover:bg-white hover:text-black transition-all duration-200 disabled:bg-gray-300 disabled:text-gray-500 disabled:border-gray-300 disabled:cursor-not-allowed"
            >
              SET SAIL! ⚓
            </button>
          </div>
        </form>

        {/* Footer */}
        <div className="text-center mt-12 text-sm font-medium tracking-wider opacity-60 text-black">
          "THE ONE PIECE IS REAL!" - WHITEBEARD
        </div>
      </div>
    </div>
  );
};

export default FeedbackInterface;