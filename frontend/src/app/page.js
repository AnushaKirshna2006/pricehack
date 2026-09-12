"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Search, Zap } from "lucide-react";

export default function LandingPage() {
  const [query, setQuery] = useState("");
  const router = useRouter();

  const handleSearch = (e) => {
    e.preventDefault();
    if (query.trim()) {
      window.__PRICEHACK_NAVIGATED__ = true;
      router.push(`/search?q=${encodeURIComponent(query.trim())}`);
    }
  };

  const PlatformIcon = ({ label, colorClass, logoSrc }) => (
    <div className={`flex flex-col items-center justify-center w-24 h-24 rounded-2xl bg-[#F7F7F7]/[0.05] backdrop-blur-md border border-[#F7F7F7]/20 shadow-lg hover:shadow-[0_0_20px_currentColor] hover:-translate-y-1 transition-all duration-300 cursor-pointer ${colorClass}`}>
      <div className="h-10 w-full flex items-center justify-center mb-2 px-3">
        <img src={logoSrc} alt={label} className="max-h-full max-w-full object-contain filter drop-shadow-lg" />
      </div>
      <span className="text-[10px] text-white font-medium font-bold uppercase tracking-widest">{label}</span>
    </div>
  );

  return (
    <main className="min-h-screen flex flex-col items-center justify-center text-white font-bold drop-shadow-lg font-sans bg-[#143109] relative selection:bg-[#AAAE7F]/40 overflow-hidden">
      
      {/* VIBRANT GLASS: Animated Background Orbs */}
      <div className="fixed inset-0 z-0 pointer-events-none overflow-hidden flex items-center justify-center">
        <div className="absolute w-[600px] h-[600px] rounded-full bg-[#AAAE7F]/30 blur-[150px] mix-blend-screen animate-blob"></div>
        <div className="absolute w-[500px] h-[500px] rounded-full bg-[#D0D6B3]/30 blur-[150px] mix-blend-screen animate-blob animation-delay-2000 translate-x-32"></div>
        <div className="absolute w-[700px] h-[700px] rounded-full bg-[#AAAE7F]/20 blur-[150px] mix-blend-screen animate-blob animation-delay-4000 -translate-x-32 translate-y-32"></div>
      </div>

      <div className="relative z-10 w-full max-w-3xl px-6 flex flex-col items-center">
        
        {/* Massive Logo */}
        <div className="flex flex-col sm:flex-row items-center space-y-4 sm:space-y-0 sm:space-x-4 mb-12 animate-in slide-in-from-bottom-8 fade-in duration-1000">
          <div className="p-3 sm:p-4 bg-gradient-to-br from-[#AAAE7F] to-[#D0D6B3] rounded-2xl shadow-[0_0_40px_rgba(170,174,127,0.5)] text-[#143109] transform -rotate-12 hover:rotate-0 transition-transform duration-500">
            <Zap className="w-10 h-10 sm:w-12 sm:h-12 fill-[#143109]" />
          </div>
          <h1 className="text-5xl sm:text-6xl font-black tracking-tighter text-white font-bold drop-shadow-lg drop-shadow-xl text-center">
            PriceHack
          </h1>
        </div>

        {/* Centered Search Bar */}
        <form onSubmit={handleSearch} className="w-full mb-12 sm:mb-16 animate-in slide-in-from-bottom-12 fade-in duration-1000 delay-150 fill-mode-both">
          <div className="relative flex items-center w-full bg-[#F7F7F7]/[0.05] backdrop-blur-2xl border border-[#F7F7F7]/20 focus-within:border-[#AAAE7F]/50 focus-within:shadow-[0_0_50px_rgba(170,174,127,0.3)] transition-all duration-500 rounded-2xl sm:rounded-3xl px-4 sm:px-8 py-4 sm:py-5 shadow-2xl">
            <Search className="h-6 w-6 sm:h-8 sm:w-8 text-[#D0D6B3] mr-3 sm:mr-5 flex-shrink-0" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search products (e.g. iPhone 15)..."
              className="block w-full bg-transparent text-lg sm:text-2xl font-medium text-white font-bold drop-shadow-lg placeholder-[#EFEFEF]/50 focus:outline-none"
            />
            <button type="submit" className="hidden"></button>
          </div>
        </form>

        {/* Platform Logos */}
        <div className="flex flex-col items-center animate-in slide-in-from-bottom-16 fade-in duration-1000 delay-300 fill-mode-both w-full">
          <p className="text-xs sm:text-sm font-bold text-white drop-shadow-md uppercase tracking-widest mb-4 sm:mb-6 drop-shadow-sm text-center">Scraping Live From</p>
          <div className="flex flex-wrap justify-center items-center gap-3 sm:gap-6 w-full">
            <PlatformIcon label="Amazon" colorClass="text-amber-500" logoSrc="/logos/amazon.svg" />
            <PlatformIcon label="Dubizzle" colorClass="text-red-500" logoSrc="/logos/dubizzle.svg" />
            <PlatformIcon label="Noon" colorClass="text-yellow-400" logoSrc="/logos/noon.svg" />
            <PlatformIcon label="eBay" colorClass="text-blue-500" logoSrc="/logos/ebay.svg" />
          </div>
        </div>

      </div>
    </main>
  );
}
