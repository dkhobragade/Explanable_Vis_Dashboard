'use client';

export function LoadingSpinner() {
  return (
    <div className="bg-slate-800 rounded-lg border border-slate-700 p-8">
      <div className="flex flex-col items-center justify-center h-96">
        <div className="relative w-16 h-16 mb-6">
          <div className="absolute inset-0 rounded-full border-4 border-slate-600"></div>
          <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-blue-500 border-r-blue-500 animate-spin"></div>
        </div>
        <p className="text-slate-300 font-medium">Processing your query...</p>
        <p className="text-slate-400 text-sm mt-2">Analyzing data and generating recommendation</p>
      </div>
    </div>
  );
}
