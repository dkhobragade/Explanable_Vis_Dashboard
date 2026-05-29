'use client';

interface RecommendationExplanationProps {
  explanation: string;
  confidence: number;
  chartType: string;
}

export function RecommendationExplanation({
  explanation,
  confidence,
  chartType,
}: RecommendationExplanationProps) {
  const confidencePercentage = Math.round(confidence * 100);
  const confidenceColor =
    confidence >= 0.8
      ? 'bg-green-900/30 border-green-700 text-green-300'
      : confidence >= 0.6
      ? 'bg-yellow-900/30 border-yellow-700 text-yellow-300'
      : 'bg-orange-900/30 border-orange-700 text-orange-300';

  return (
    <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
      <div className="flex items-start justify-between mb-4">
        <h3 className="text-lg font-semibold text-white">Recommendation</h3>
        <div
          className={`px-3 py-1 rounded-full text-sm font-semibold border ${confidenceColor}`}
        >
          {confidencePercentage}% Confidence
        </div>
      </div>

      <div className="mb-4 p-3 bg-slate-700 rounded-lg">
        <p className="text-sm text-slate-300">
          <span className="font-semibold">Chart Type:</span>{' '}
          <span className="text-blue-400">{chartType.replace(/_/g, ' ')}</span>
        </p>
      </div>

      <div className="p-4 bg-slate-700/50 rounded-lg border border-slate-600">
        <p className="text-slate-200 text-sm leading-relaxed">{explanation}</p>
      </div>

      <div className="mt-4 text-xs text-slate-400">
        <p>
          This recommendation is based on the structure of your data and the intent
          extracted from your query using natural language processing.
        </p>
      </div>
    </div>
  );
}
