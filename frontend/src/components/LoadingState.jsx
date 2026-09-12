"use client";

import { RefreshCw } from "lucide-react";

export default function LoadingState() {
  return (
    <div className="w-full mt-12 flex flex-col items-start justify-center p-8">
      <RefreshCw className="h-6 w-6 text-[#D0D6B3] animate-spin mb-4" />
      <h3 className="text-lg font-semibold text-white font-bold drop-shadow-lg mb-2">Compiling Market Data</h3>
      <p className="text-sm text-white drop-shadow-md max-w-sm">
        Our engine is currently indexing live prices from Amazon, eBay, Noon, and Dubizzle to find the absolute best deals.
      </p>
    </div>
  );
}
