'use client';

import { useState } from 'react';
import { QueryInput } from './components/QueryInput';
import { ChartDisplay } from './components/ChartDisplay';
import { RecommendationExplanation } from './components/RecommendationExplanation';
import { LoadingSpinner } from './components/LoadingSpinner';

interface Recommendation {
  chart_type: string;
  confidence: number;
  data: any[];
  fields: string[];
  filters: Record<string, string[]>;
  temporal_field: string | null;
  explanation: string;
  rule_reason: string;
}

export default function Home() {
  const [query, setQuery] = useState('');
  const [recommendation, setRecommendation] = useState<Recommendation | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleQuery = async (inputQuery: string) => {
    setQuery(inputQuery);
    setLoading(true);
    setError(null);
    setRecommendation(null);

    try {
      console.log("[v0] Sending query to backend...", { query: inputQuery });
      
      const response = await fetch('http://localhost:8000/api/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: inputQuery,
          user_id: 'web-user',
        }),
      });

      console.log("[v0] Response status:", response.status);
      
      if (!response.ok) {
        let errorData;
        try {
          errorData = await response.json();
          console.log("[v0] Error data from server:", errorData);
        } catch {
          console.log("[v0] Could not parse error response");
          errorData = { detail: `HTTP ${response.status}: ${response.statusText}` };
        }
        throw new Error(errorData.detail || `Failed to get recommendation (HTTP ${response.status})`);
      }

      const data = await response.json();
      console.log("[v0] Recommendation received:", data);
      setRecommendation(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An error occurred';
      console.error("[v0] Error fetching recommendation:", err);
      
      // Provide more helpful error messages
      let displayMessage = errorMessage;
      if (errorMessage.includes('Failed to fetch')) {
        displayMessage = 'Cannot reach backend API at http://localhost:8000. Is it running? (Terminal 1 should show "Application startup complete")';
      } else if (errorMessage.includes('HTTP 500')) {
        displayMessage = 'Backend error. Check the backend terminal for error details.';
      } else if (errorMessage.includes('HTTP 400')) {
        displayMessage = 'Invalid query format or query too short (min 3 characters).';
      }
      
      setError(displayMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
            Intelligent Data Visualization
          </h1>
          <p className="text-xl text-slate-300">
            Ask questions about OECD agricultural data, get instant chart recommendations
          </p>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Panel: Input */}
          <div className="lg:col-span-1">
            <div className="bg-slate-800 rounded-lg border border-slate-700 p-6 shadow-xl">
              <h2 className="text-2xl font-bold text-white mb-4">Your Query</h2>
              
              <QueryInput
                onSubmit={handleQuery}
                disabled={loading}
              />

              {/* Example Queries */}
              {!recommendation && !error && (
                <div className="mt-8 p-4 bg-slate-700 rounded-lg">
                  <p className="text-sm font-semibold text-slate-300 mb-3">Try these queries:</p>
                  <ul className="space-y-2">
                    <li>
                      <button
                        onClick={() => handleQuery('Show wheat production trends over time')}
                        className="text-sm text-blue-400 hover:text-blue-300 text-left w-full"
                      >
                        • Show wheat production trends over time
                      </button>
                    </li>
                    <li>
                      <button
                        onClick={() => handleQuery('Compare maize production by country')}
                        className="text-sm text-blue-400 hover:text-blue-300 text-left w-full"
                      >
                        • Compare maize production by country
                      </button>
                    </li>
                    <li>
                      <button
                        onClick={() => handleQuery('What are the top wheat producing regions?')}
                        className="text-sm text-blue-400 hover:text-blue-300 text-left w-full"
                      >
                        • What are the top wheat producing regions?
                      </button>
                    </li>
                    <li>
                      <button
                        onClick={() => handleQuery('Which commodity outperform in the respective region from the available commodity')}
                        className="text-sm text-blue-400 hover:text-blue-300 text-left w-full"
                      >
                        • Which commodity outperform in the respective region from the available commodity
                      </button>
                    </li>
                    
                  </ul>
                </div>
              )}

              {/* Error Message */}
              {error && (
                <div className="mt-6 p-4 bg-red-900/30 border border-red-700 rounded-lg">
                  <p className="text-red-300 font-semibold">⚠️ Error:</p>
                  <p className="text-red-200 text-sm mt-1">{error}</p>
                  <p className="text-red-200 text-xs mt-3">
                    <strong>Troubleshooting tips:</strong>
                  </p>
                  <ul className="text-red-200 text-xs mt-2 space-y-1 ml-4">
                    <li>✓ Backend running on http://localhost:8000?</li>
                    <li>✓ Check backend terminal for error messages</li>
                    <li>✓ Both backend and frontend terminals open?</li>
                    <li>✓ Check browser console (F12) for details</li>
                  </ul>
                </div>
              )}
            </div>
          </div>

          {/* Right Panel: Results */}
          <div className="lg:col-span-1">
            {loading && <LoadingSpinner />}

            {recommendation && (
              <div className="space-y-6">
                {/* Explanation */}
                <RecommendationExplanation
                  explanation={recommendation.explanation}
                  confidence={recommendation.confidence}
                  chartType={recommendation.chart_type}
                />

                {/* Chart Display */}
                {recommendation.data && recommendation.data.length > 0 && (
                  <ChartDisplay
                    chartType={recommendation.chart_type}
                    data={recommendation.data}
                    fields={recommendation.fields}
                    temporalField={recommendation.temporal_field}
                  />
                )}

                {/* Data Summary */}
                {recommendation.data && (
                  <div className="bg-slate-800 rounded-lg border border-slate-700 p-4">
                    <p className="text-sm text-slate-400">
                      <span className="font-semibold">Data Points:</span> {recommendation.data.length}
                    </p>
                    <p className="text-sm text-slate-400 mt-1">
                      <span className="font-semibold">Fields:</span> {recommendation.fields.join(', ')}
                    </p>
                  </div>
                )}
              </div>
            )}

            {!loading && !recommendation && !error && (
              <div className="h-96 bg-slate-800 rounded-lg border border-slate-700 border-dashed flex items-center justify-center">
                <div className="text-center">
                  <p className="text-slate-400 mb-2">Submit a query to see the recommended chart</p>
                  <p className="text-slate-500 text-sm">Your visualization will appear here</p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="mt-12 pt-8 border-t border-slate-700 text-center text-slate-400">
          <p className="text-sm">
            Built with FastAPI, React, and intelligent chart recommendations
          </p>
        </div>
      </div>
    </main>
  );
}
