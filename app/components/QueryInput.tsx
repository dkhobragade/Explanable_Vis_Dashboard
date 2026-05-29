'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

interface QueryInputProps {
  onSubmit: (query: string) => void;
  disabled?: boolean;
}

export function QueryInput({ onSubmit, disabled }: QueryInputProps) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSubmit(query);
      setQuery('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="flex gap-2">
        <Input
          type="text"
          placeholder="Ask a question about the data... (e.g., 'Show wheat production trends')"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          disabled={disabled}
          className="flex-1 bg-slate-700 border-slate-600 text-white placeholder-slate-400"
        />
        <Button
          type="submit"
          disabled={disabled || !query.trim()}
          className="bg-blue-600 hover:bg-blue-700"
        >
          {disabled ? 'Loading...' : 'Search'}
        </Button>
      </div>
      <p className="text-xs text-slate-400">
        Natural language queries are parsed to understand your intent and select the best visualization.
      </p>
    </form>
  );
}
