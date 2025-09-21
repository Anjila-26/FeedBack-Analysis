'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';

interface Feedback {
  user_id?: string;
  rating: number;
  comment: string;
  timestamp?: string;
  category?: string;
}

interface BasicInsights {
  statistics: any;
  average_rating: number;
  average_sentiment: number;
  common_keywords: string[];
}

interface AIInsights {
  ai_insights: any;
  statistics: any;
}

const AdminDashboard: React.FC = () => {
  const [allFeedback, setAllFeedback] = useState<Feedback[]>([]);
  const [basicInsights, setBasicInsights] = useState<BasicInsights | null>(null);
  const [aiInsights, setAIInsights] = useState<AIInsights | null>(null);
  const [priorityIssues, setPriorityIssues] = useState<any>(null);
  const [featureRequests, setFeatureRequests] = useState<any>(null);
  const [selectedFeedbackId, setSelectedFeedbackId] = useState<number>(1);
  const [individualAnalysis, setIndividualAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState<{ [key: string]: boolean }>({});
  const [error, setError] = useState<string>('');

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  const makeRequest = async (endpoint: string, method: string = 'GET', body?: any) => {
    try {
      const response = await fetch(`${API_URL}${endpoint}`, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: body ? JSON.stringify(body) : undefined,
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (err) {
      throw err;
    }
  };

  const handleRequest = async (key: string, requestFn: () => Promise<any>, setter: (data: any) => void) => {
    setLoading(prev => ({ ...prev, [key]: true }));
    setError('');
    try {
      const data = await requestFn();
      setter(data);
    } catch (err) {
      setError(`${key} failed: ${err instanceof Error ? err.message : 'Unknown error'}`);
    } finally {
      setLoading(prev => ({ ...prev, [key]: false }));
    }
  };

  const testRootEndpoint = async () => {
    await handleRequest('root', () => makeRequest('/'), (data) => {
      alert(`Root endpoint response: ${JSON.stringify(data, null, 2)}`);
    });
  };

  const fetchAllFeedback = async () => {
    await handleRequest('allFeedback', () => makeRequest('/feedback/all'), (data) => {
      // Handle the API response structure: { feedback: [...], count: number }
      setAllFeedback(data.feedback || []);
    });
  };

  const fetchBasicInsights = async () => {
    await handleRequest('basicInsights', () => makeRequest('/feedback/basic-insights'), setBasicInsights);
  };

  const fetchAIInsights = async () => {
    await handleRequest('aiInsights', () => makeRequest('/feedback/ai-insights'), setAIInsights);
  };

  const fetchPriorityIssues = async () => {
    await handleRequest('priorityIssues', () => makeRequest('/feedback/priority-issues'), setPriorityIssues);
  };

  const fetchFeatureRequests = async () => {
    await handleRequest('featureRequests', () => makeRequest('/feedback/feature-requests'), setFeatureRequests);
  };

  const analyzeIndividualFeedback = async () => {
    await handleRequest('individualAnalysis',
      () => makeRequest(`/feedback/analyze/${selectedFeedbackId}`, 'POST'),
      setIndividualAnalysis
    );
  };

  useEffect(() => {
    fetchAllFeedback();
  }, []);

  return (
    <div className="min-h-screen bg-white p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-black tracking-wider text-black">ADMIN DASHBOARD</h1>
            <div className="w-24 h-1 bg-black mt-2"></div>
          </div>
          <Link
            href="/"
            className="px-6 py-3 bg-black text-white font-bold tracking-wide hover:bg-gray-800 transition-colors"
          >
            ← BACK TO FEEDBACK FORM
          </Link>
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-6 p-4 bg-red-100 border-2 border-red-500 text-red-700 font-medium">
            {error}
          </div>
        )}

        {/* Endpoint Testing Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">

          {/* Root Endpoint Test */}
          <div className="border-4 border-black p-6">
            <h2 className="text-xl font-bold mb-4 text-black">🔧 ROOT ENDPOINT TEST</h2>
            <button
              onClick={testRootEndpoint}
              disabled={loading.root}
              className="w-full px-4 py-3 bg-black text-white font-bold tracking-wide hover:bg-gray-800 disabled:bg-gray-400 transition-colors"
            >
              {loading.root ? 'Testing...' : 'TEST GET /'}
            </button>
          </div>

          {/* All Feedback */}
          <div className="border-4 border-black p-6">
            <h2 className="text-xl font-bold mb-4 text-black">📋 ALL FEEDBACK ({Array.isArray(allFeedback) ? allFeedback.length : 0})</h2>
            <button
              onClick={fetchAllFeedback}
              disabled={loading.allFeedback}
              className="w-full px-4 py-3 bg-black text-white font-bold tracking-wide hover:bg-gray-800 disabled:bg-gray-400 transition-colors mb-4"
            >
              {loading.allFeedback ? 'Loading...' : 'REFRESH FEEDBACK'}
            </button>
            <div className="max-h-40 overflow-y-auto bg-gray-50 p-3 text-sm">
              {Array.isArray(allFeedback) && allFeedback.length > 0 ? (
                allFeedback.map((feedback, index) => (
                  <div key={index} className="mb-2 p-2 bg-white border text-black">
                    <strong>#{index + 1}</strong> - Rating: {feedback.rating}/5 - {feedback.category}
                    <br />
                    <span className="text-gray-600">{feedback.comment?.substring(0, 50) || 'No comment'}...</span>
                  </div>
                ))
              ) : (
                <p className="text-gray-500">No feedback available. Submit some feedback first!</p>
              )}
            </div>
          </div>

          {/* Basic Insights */}
          <div className="border-4 border-black p-6">
            <h2 className="text-xl font-bold mb-4 text-black">📊 BASIC INSIGHTS</h2>
            <button
              onClick={fetchBasicInsights}
              disabled={loading.basicInsights}
              className="w-full px-4 py-3 bg-black text-white font-bold tracking-wide hover:bg-gray-800 disabled:bg-gray-400 transition-colors mb-4"
            >
              {loading.basicInsights ? 'Loading...' : 'GET BASIC INSIGHTS'}
            </button>
            {basicInsights && (
              <div className="bg-gray-50 p-3 text-sm text-black">
                <p><strong>Avg Rating:</strong> {basicInsights.average_rating?.toFixed(2) || 'N/A'}</p>
                <p><strong>Avg Sentiment:</strong> {basicInsights.average_sentiment?.toFixed(2) || 'N/A'}</p>
                <p><strong>Keywords:</strong> {basicInsights.common_keywords?.join(', ') || 'None'}</p>
              </div>
            )}
          </div>

          {/* AI Insights */}
          <div className="border-4 border-black p-6">
            <h2 className="text-xl font-bold mb-4 text-black">🤖 AI INSIGHTS</h2>
            <button
              onClick={fetchAIInsights}
              disabled={loading.aiInsights}
              className="w-full px-4 py-3 bg-black text-white font-bold tracking-wide hover:bg-gray-800 disabled:bg-gray-400 transition-colors mb-4"
            >
              {loading.aiInsights ? 'Analyzing...' : 'GET AI INSIGHTS'}
            </button>
            {aiInsights && (
              <div className="bg-gray-50 p-3 text-sm max-h-32 overflow-y-auto text-black">
                <pre className="whitespace-pre-wrap">
                  {JSON.stringify(aiInsights.ai_insights, null, 2)}
                </pre>
              </div>
            )}
          </div>

          {/* Priority Issues */}
          <div className="border-4 border-black p-6">
            <h2 className="text-xl font-bold mb-4 text-black">🚨 PRIORITY ISSUES</h2>
            <button
              onClick={fetchPriorityIssues}
              disabled={loading.priorityIssues}
              className="w-full px-4 py-3 bg-red-600 text-white font-bold tracking-wide hover:bg-red-700 disabled:bg-gray-400 transition-colors mb-4"
            >
              {loading.priorityIssues ? 'Analyzing...' : 'GET PRIORITY ISSUES'}
            </button>
            {priorityIssues && (
              <div className="bg-red-50 p-3 text-sm max-h-32 overflow-y-auto text-black">
                <pre className="whitespace-pre-wrap">
                  {JSON.stringify(priorityIssues, null, 2)}
                </pre>
              </div>
            )}
          </div>

          {/* Feature Requests */}
          <div className="border-4 border-black p-6">
            <h2 className="text-xl font-bold mb-4 text-black">💡 FEATURE REQUESTS</h2>
            <button
              onClick={fetchFeatureRequests}
              disabled={loading.featureRequests}
              className="w-full px-4 py-3 bg-blue-600 text-white font-bold tracking-wide hover:bg-blue-700 disabled:bg-gray-400 transition-colors mb-4"
            >
              {loading.featureRequests ? 'Analyzing...' : 'GET FEATURE REQUESTS'}
            </button>
            {featureRequests && (
              <div className="bg-blue-50 p-3 text-sm max-h-32 overflow-y-auto text-black">
                <pre className="whitespace-pre-wrap">
                  {JSON.stringify(featureRequests, null, 2)}
                </pre>
              </div>
            )}
          </div>

        </div>

        {/* Individual Feedback Analysis */}
        <div className="border-4 border-black p-6">
          <h2 className="text-xl font-bold mb-4 text-black">🔍 INDIVIDUAL FEEDBACK ANALYSIS</h2>
          <div className="flex gap-4 mb-4">
            <div className="flex-1">
              <label className="block text-sm font-bold mb-2 text-black">FEEDBACK ID:</label>
              <input
                type="number"
                min="1"
                max={Array.isArray(allFeedback) ? allFeedback.length : 1}
                value={selectedFeedbackId}
                onChange={(e) => setSelectedFeedbackId(Number(e.target.value))}
                className="w-full p-3 border-4 border-black text-lg font-medium tracking-wide text-black focus:outline-none focus:bg-gray-50"
              />
            </div>
            <div className="flex-none">
              <label className="block text-sm font-bold mb-2 text-black">&nbsp;</label>
              <button
                onClick={analyzeIndividualFeedback}
                disabled={loading.individualAnalysis}
                className="px-6 py-3 bg-purple-600 text-white font-bold tracking-wide hover:bg-purple-700 disabled:bg-gray-400 transition-colors"
              >
                {loading.individualAnalysis ? 'Analyzing...' : 'ANALYZE'}
              </button>
            </div>
          </div>
          {individualAnalysis && (
            <div className="bg-purple-50 p-4 text-sm max-h-40 overflow-y-auto text-black">
              <h3 className="font-bold mb-2">Analysis Result:</h3>
              <pre className="whitespace-pre-wrap">
                {JSON.stringify(individualAnalysis, null, 2)}
              </pre>
            </div>
          )}
        </div>

        {/* API Status */}
        <div className="mt-8 text-center text-sm text-gray-600">
          <p>API Endpoint: <code className="bg-gray-100 px-2 py-1 rounded">{API_URL}</code></p>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;