"use client";

import { useState, useMemo, useEffect, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { Search, RefreshCw, ChevronDown, ChevronUp, Check, Zap, Globe, SlidersHorizontal, Share2 } from "lucide-react";
import LoadingState from "@/components/LoadingState";
import ProductCard from "@/components/ProductCard";
import PriceChart from "@/components/PriceChart";

const ALL_PLATFORMS = ['Amazon', 'Dubizzle', 'Noon', 'eBay'];

const CURRENCIES = {
  USD: { rate: 1, symbol: "$" },
  AED: { rate: 3.67, symbol: "د.إ " },
  EUR: { rate: 0.92, symbol: "€" },
  GBP: { rate: 0.79, symbol: "£" }
};

function SearchDashboard() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const initialQuery = searchParams.get("q") || "";

  const [query, setQuery] = useState(initialQuery);
  const [isLoading, setIsLoading] = useState(false);
  const [rawResults, setRawResults] = useState(null);
  const [hasInitialFetched, setHasInitialFetched] = useState(false);

  const initialCurrency = searchParams.get("currency") || "USD";
  const initialPlatforms = searchParams.get("platforms") ? searchParams.get("platforms").split(',') : ALL_PLATFORMS;
  const initialMaxPrice = searchParams.get("maxPrice") ? parseInt(searchParams.get("maxPrice")) : 20000;
  const initialSortBy = searchParams.get("sortBy") || "";
  const initialConditions = searchParams.get("conditions") ? searchParams.get("conditions").split(',') : ['New', 'Used-Excellent'];

  const [currencyKey, setCurrencyKey] = useState(initialCurrency);
  const currency = CURRENCIES[currencyKey];

  // Filters State
  const [activePlatforms, setActivePlatforms] = useState(initialPlatforms);
  const [maxPrice, setMaxPrice] = useState(initialMaxPrice);
  const [sortBy, setSortBy] = useState(initialSortBy); 
  const [activeConditions, setActiveConditions] = useState(initialConditions);

  const [copied, setCopied] = useState(false);
  
  useEffect(() => {
    if (typeof window !== "undefined") {
      if (!window.__PRICEHACK_NAVIGATED__) {
        router.replace("/");
      }
    }
  }, [router]);

  const handleShare = () => {
    const url = new URL(window.location.href);
    url.searchParams.set("q", query);
    url.searchParams.set("currency", currencyKey);
    url.searchParams.set("platforms", activePlatforms.join(','));
    url.searchParams.set("maxPrice", maxPrice);
    url.searchParams.set("sortBy", sortBy);
    url.searchParams.set("conditions", activeConditions.join(','));
    
    navigator.clipboard.writeText(url.toString());
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const executeSearch = async (searchQuery) => {
    if (!searchQuery) return;
    setIsLoading(true);
    setRawResults(null);

    try {
      const backendUrl = process.env.NEXT_PUBLIC_API_URL || (window.location.hostname === "localhost" ? "http://127.0.0.1:8000" : "https://pricehack-api.onrender.com");
      const res = await fetch(`${backendUrl}/api/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: searchQuery, limit: 40 }),
      });
      const data = await res.json();
      if (!res.ok) {
        alert("Search failed");
        setIsLoading(false);
        return;
      }
      setRawResults(data.results || data);
      setIsLoading(false);
    } catch (error) {
      console.error(error);
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (initialQuery && !hasInitialFetched) {
      executeSearch(initialQuery);
      setHasInitialFetched(true);
    }
  }, [initialQuery, hasInitialFetched]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    executeSearch(query);
  };

  const togglePlatform = (platform) => {
    setActivePlatforms(prev => 
      prev.length === 1 && prev[0] === platform ? ALL_PLATFORMS : [platform]
    );
  };

  const toggleCondition = (cond) => {
    setActiveConditions(prev => 
      prev.includes(cond) ? prev.filter(c => c !== cond) : [...prev, cond]
    );
  };

  const processedResults = useMemo(() => {
    if (!rawResults) return null;
    
    // 1. Relevance and Negative Keyword Filtering
    const queryWords = query.toLowerCase().trim().split(/\s+/).filter(w => w.length > 0);
    const negativeKeywords = ["case", "cover", "protector", "cable", "strap", "band", "charger", "refurbished", "renewed"];
    
    let filtered = rawResults.filter(item => {
      // Platform filter
      if (!activePlatforms.includes(item.platform)) return false;
      
      // Price and condition filter
      const convertedPrice = item.price * currency.rate;
      if (convertedPrice > maxPrice && convertedPrice !== 0) return false;
      const mockCondition = item.platform === 'Dubizzle' ? 'Used-Excellent' : 'New';
      if (!activeConditions.includes(mockCondition)) return false;

      const titleLower = item.title.toLowerCase();
      
      // Relevance Check: Title must contain at least 50% of query words
      const matchCount = queryWords.filter(word => titleLower.includes(word)).length;
      const hasMostQueryWords = queryWords.length === 0 || (matchCount / queryWords.length >= 0.5);
      if (!hasMostQueryWords) return false;
      
      // Negative Keyword Check (unless the user explicitly searched for it)
      const hasNegative = negativeKeywords.some(neg => {
        return titleLower.includes(neg) && !queryWords.includes(neg);
      });
      if (hasNegative) return false;

      return true;
    });

    // 2. Filter out zero-price items and keep all valid results
    filtered = filtered.filter(item => item.price > 0);

    // Deal Score Calculation
    if (filtered.length > 0) {
      const avgPrice = filtered.reduce((sum, item) => sum + item.price, 0) / filtered.length;
      filtered = filtered.map(item => {
        let dealScore = 'fair';
        if (item.price <= avgPrice * 0.8) dealScore = 'great';
        else if (item.price >= avgPrice * 1.2) dealScore = 'poor';
        return { ...item, dealScore };
      });
    }

    // 3. Sorting
    if (sortBy === 'price_asc') {
      filtered = filtered.sort((a, b) => a.price - b.price);
    } else if (sortBy === 'price_desc') {
      filtered = filtered.sort((a, b) => b.price - a.price);
    }

    return filtered;
  }, [rawResults, activePlatforms, maxPrice, sortBy, activeConditions, query, currency]);

  const TopPlatformToggle = ({ label, colorClass, isActive }) => (
    <div 
      onClick={() => togglePlatform(label)}
      className={`px-4 py-2 rounded-full text-xs font-medium transition-all cursor-pointer select-none flex items-center gap-2 border shadow-lg backdrop-blur-md
        ${isActive ? `bg-[#F7F7F7]/[0.1] text-white font-bold drop-shadow-lg border-[#F7F7F7]/20 ${colorClass}` : 'bg-[#F7F7F7]/[0.02] text-white drop-shadow-md border-[#F7F7F7]/5 hover:bg-[#F7F7F7]/[0.05] hover:text-white font-medium'}`}
    >
      <div className={`w-2 h-2 rounded-full shadow-[0_0_10px_currentColor] transition-opacity duration-300 ${isActive ? 'opacity-100' : 'opacity-0'} ${colorClass.split(' ')[0].replace('text', 'bg')}`}></div>
      {label}
    </div>
  );

  const FilterAccordion = ({ title, children, defaultOpen = false }) => {
    const [isOpen, setIsOpen] = useState(defaultOpen);
    return (
      <div className="w-full border-b border-white/5 mb-4 overflow-hidden transition-all">
        <div 
          onClick={() => setIsOpen(!isOpen)}
          className="py-3 flex items-center justify-between cursor-pointer hover:text-white font-bold drop-shadow-lg text-white font-medium transition-colors"
        >
          <span className="text-sm font-semibold tracking-wide">{title}</span>
          {isOpen ? <ChevronUp size={16} className="text-[#AAAE7F]" /> : <ChevronDown size={16} className="text-gray-200" />}
        </div>
        {isOpen && (
          <div className="pb-4 pt-2 flex flex-col gap-3">
            {children}
          </div>
        )}
      </div>
    );
  };

  return (
    <main className="min-h-screen text-white font-bold drop-shadow-lg font-sans bg-[#143109] relative flex flex-col lg:flex-row selection:bg-[#AAAE7F]/30 overflow-hidden">
      
      {/* VIBRANT GLASS: Animated Background Orbs */}
      <div className="fixed inset-0 z-0 pointer-events-none overflow-hidden">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-[#AAAE7F]/30 blur-[120px] mix-blend-screen animate-blob"></div>
        <div className="absolute top-[20%] right-[-10%] w-[30%] h-[30%] rounded-full bg-[#D0D6B3]/30 blur-[120px] mix-blend-screen animate-blob animation-delay-2000"></div>
        <div className="absolute bottom-[-20%] left-[20%] w-[50%] h-[50%] rounded-full bg-[#AAAE7F]/20 blur-[150px] mix-blend-screen animate-blob animation-delay-4000"></div>
      </div>

      {/* 1. LEFT SIDEBAR */}
      <aside className="relative z-20 w-full lg:w-[280px] xl:w-[320px] flex-shrink-0 flex flex-col border-b lg:border-b-0 lg:border-r border-white/10 bg-white/[0.02] backdrop-blur-[40px] shadow-[0_0_40px_rgba(0,0,0,0.5)] h-auto lg:h-screen overflow-y-visible lg:overflow-y-auto custom-scrollbar p-6 lg:p-8">
        
        {/* Branding */}
        <div className="flex items-center justify-between mb-12">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-gradient-to-br from-[#AAAE7F] to-[#D0D6B3] rounded-xl shadow-[0_0_20px_rgba(170,174,127,0.4)] text-[#143109]">
              <Zap size={18} className="fill-[#143109]" />
            </div>
            <h1 className="text-lg font-bold tracking-tight text-white font-bold drop-shadow-lg drop-shadow-md">
              PriceHack
            </h1>
          </div>

          <div className="relative flex items-center bg-white/[0.05] border border-white/10 hover:bg-white/[0.1] rounded-lg transition-colors cursor-pointer shadow-inner">
            <div className="pl-3 pr-1 py-1.5 flex items-center pointer-events-none">
              <Globe size={14} className="text-[#AAAE7F]" />
            </div>
            <select 
              value={currencyKey}
              onChange={(e) => setCurrencyKey(e.target.value)}
              className="bg-transparent text-gray-200 text-xs font-semibold focus:outline-none cursor-pointer appearance-none py-1.5 pr-8 pl-1 w-full"
            >
              {Object.keys(CURRENCIES).map(key => (
                <option key={key} value={key} className="bg-[#143109] text-white py-2">{key}</option>
              ))}
            </select>
            <div className="absolute right-2 top-1/2 transform -translate-y-1/2 pointer-events-none">
              <ChevronDown size={14} className="text-gray-400" />
            </div>
          </div>
        </div>

        <div className="mb-10">
          <h2 className="text-xs font-black uppercase tracking-widest text-[#D0D6B3] mb-3 drop-shadow-sm">Market Intelligence</h2>
          <p className="text-white font-medium text-sm leading-relaxed font-medium">
            Simultaneously scrape and index the absolute lowest prices across top retailers in real-time.
          </p>
        </div>

        {/* Price Chart */}
        {processedResults && !isLoading && (
          <div className="mt-2 flex-grow flex flex-col animate-in fade-in duration-700">
            <h2 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-4">Live Comparison</h2>
            <div className="bg-white/[0.03] rounded-2xl border border-white/10 p-5 shadow-[inset_0_0_20px_rgba(255,255,255,0.02)]">
              <PriceChart data={processedResults} currency={currency} />
            </div>
          </div>
        )}
      </aside>


      {/* 2. CENTER COLUMN */}
      <section className="relative z-10 flex-1 flex flex-col h-auto lg:h-screen overflow-y-visible lg:overflow-y-auto p-6 lg:px-12 lg:py-10 custom-scrollbar min-h-screen">
        
        {/* TOP HEADER */}
        <header className="flex flex-col gap-8 mb-10 w-full max-w-4xl mx-auto">
          
          {/* Vibrant Search Bar */}
          <form onSubmit={handleSearchSubmit} className="w-full">
            <div className="relative flex items-center w-full bg-white/[0.03] backdrop-blur-xl border border-white/10 hover:border-white/20 hover:shadow-[0_0_30px_rgba(170,174,127,0.15)] transition-all duration-300 rounded-2xl px-6 py-4 shadow-2xl">
              <Search className="h-6 w-6 text-[#AAAE7F] mr-4" />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search for any product (e.g. iPhone 15 Pro Max)..."
                disabled={isLoading}
                className="block w-full bg-transparent text-lg font-medium text-white font-bold drop-shadow-lg placeholder-[#EFEFEF]/50 focus:outline-none"
              />
              <button type="submit" disabled={isLoading} className="hidden"></button>
              {isLoading && <RefreshCw className="animate-spin h-5 w-5 text-[#D0D6B3] ml-2" />}
            </div>
          </form>

          {/* Sleek Platform Tabs */}
          <div className="flex items-center gap-3 border-b border-white/10 pb-5">
            <span className="text-xs font-bold text-gray-500 mr-2 uppercase tracking-widest">Active Sources</span>
            <div 
              onClick={() => setActivePlatforms(ALL_PLATFORMS)}
              className={`px-4 py-2 rounded-full text-xs font-medium transition-all cursor-pointer select-none flex items-center gap-2 border shadow-lg backdrop-blur-md
                ${activePlatforms.length === ALL_PLATFORMS.length ? 'bg-[#F7F7F7]/[0.1] text-white font-bold drop-shadow-lg border-[#F7F7F7]/20' : 'bg-[#F7F7F7]/[0.02] text-white drop-shadow-md border-[#F7F7F7]/5 hover:bg-[#F7F7F7]/[0.05] hover:text-white font-medium'}`}
            >
              <div className={`w-2 h-2 rounded-full shadow-[0_0_10px_currentColor] transition-opacity duration-300 bg-white ${activePlatforms.length === ALL_PLATFORMS.length ? 'opacity-100' : 'opacity-0'}`}></div>
              View All
            </div>
            <TopPlatformToggle label="Amazon" colorClass="text-amber-500" isActive={activePlatforms.includes('Amazon') && activePlatforms.length === 1} />
            <TopPlatformToggle label="Dubizzle" colorClass="text-red-500" isActive={activePlatforms.includes('Dubizzle') && activePlatforms.length === 1} />
            <TopPlatformToggle label="Noon" colorClass="text-yellow-400" isActive={activePlatforms.includes('Noon') && activePlatforms.length === 1} />
            <TopPlatformToggle label="eBay" colorClass="text-blue-400" isActive={activePlatforms.includes('eBay') && activePlatforms.length === 1} />
          </div>
        </header>

        {/* Product List */}
        <div className="w-full max-w-4xl mx-auto flex flex-col flex-1 pb-12">
          {!rawResults && !isLoading && (
             <div className="flex-1 flex flex-col items-center justify-center opacity-50">
                <div className="w-24 h-24 rounded-full bg-white/5 border border-white/10 flex items-center justify-center mb-6 shadow-[0_0_30px_rgba(255,255,255,0.05)]">
                  <Search size={40} className="text-gray-400 stroke-1" />
                </div>
                <p className="text-lg font-medium text-gray-300">Enter a product name to begin.</p>
             </div>
          )}
          {isLoading && <LoadingState />}
          
          {processedResults && !isLoading && (
            <div className="flex flex-col animate-in fade-in duration-500">
              <div className="mb-6 flex flex-col justify-start">
                <h2 className="text-xl font-bold text-white drop-shadow-md mb-2">Consolidated Results</h2>
                <span className="text-sm font-semibold text-white bg-white/5 px-3 py-1 rounded-full border border-white/10 self-start">Showing Top {processedResults.length} relevant items</span>
              </div>
              {processedResults.length === 0 ? (
                <div className="p-12 text-center text-base font-medium text-gray-400 border border-white/10 rounded-2xl bg-white/[0.02] backdrop-blur-md shadow-xl">No products match your current filters.</div>
              ) : (
                <div className="flex flex-col gap-4">
                  {processedResults.map((product, index) => (
                    <ProductCard key={`${product.platform}-${index}`} product={product} currency={currency} />
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </section>

      {/* 3. RIGHT SIDEBAR */}
      <aside className="relative z-20 w-full lg:w-[280px] xl:w-[320px] flex-shrink-0 flex flex-col h-auto lg:h-screen overflow-y-visible lg:overflow-y-auto p-6 lg:p-8 border-t lg:border-t-0 lg:border-l border-white/10 bg-white/[0.02] backdrop-blur-[40px] shadow-[-20px_0_40px_rgba(0,0,0,0.3)] custom-scrollbar">
        
        <div className="flex items-center justify-between mb-10 pb-6 border-b border-white/10">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-[#AAAE7F]/20 text-[#AAAE7F]">
              <SlidersHorizontal size={16} />
            </div>
            <h2 className="text-base font-bold text-white tracking-wide">Filters</h2>
          </div>
          <button 
            onClick={handleShare}
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-xs font-semibold text-white transition-colors"
          >
            <Share2 size={14} />
            {copied ? "Copied!" : "Share"}
          </button>
        </div>

        {/* Price Range Card */}
        <div className="w-full mb-8">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-white font-medium">Max Price</h3>
            <span className="text-sm font-bold font-mono text-white font-bold drop-shadow-lg bg-[#AAAE7F]/20 border border-[#AAAE7F]/30 px-3 py-1 rounded-lg shadow-[0_0_10px_rgba(170,174,127,0.2)]">{currency.symbol}{maxPrice.toLocaleString()}</span>
          </div>
          
          <div className="relative w-full mb-1 flex items-center justify-center py-3">
            <input 
              type="range" 
              min="0" 
              max="20000" 
              step="50"
              value={maxPrice}
              onChange={(e) => setMaxPrice(parseInt(e.target.value))}
              className="w-full h-1.5 bg-white/10 rounded-full appearance-none cursor-pointer accent-[#AAAE7F] hover:accent-[#D0D6B3] transition-all shadow-inner"
            />
          </div>
        </div>

        {/* Condition Accordion */}
        <FilterAccordion title="Condition" defaultOpen={true}>
          {['New', 'Used-Excellent'].map(cond => (
            <label key={cond} onClick={() => toggleCondition(cond)} className="flex items-center gap-4 cursor-pointer group p-2 rounded-lg hover:bg-[#F7F7F7]/5 transition-colors">
              <div className={`w-4 h-4 rounded-md flex items-center justify-center border-2 transition-all ${activeConditions.includes(cond) ? 'bg-[#AAAE7F] border-[#AAAE7F] shadow-[0_0_10px_rgba(170,174,127,0.5)]' : 'bg-transparent border-[#EFEFEF]/50 group-hover:border-[#EFEFEF]'}`}>
                {activeConditions.includes(cond) && <Check size={12} className="text-[#143109] font-bold" />}
              </div>
              <span className="text-sm font-medium text-white font-medium group-hover:text-white font-bold drop-shadow-lg transition-colors">{cond}</span>
            </label>
          ))}
        </FilterAccordion>

        {/* Sort by Accordion */}
        <FilterAccordion title="Sort by" defaultOpen={true}>
            <label className="flex items-center gap-4 cursor-pointer group p-2 rounded-lg hover:bg-[#F7F7F7]/5 transition-colors">
              <input type="radio" name="sort" checked={sortBy === ''} onChange={() => setSortBy('')} className="hidden" />
              <div className={`w-4 h-4 rounded-full flex items-center justify-center border-2 transition-all ${sortBy === '' ? 'border-[#AAAE7F] shadow-[0_0_10px_rgba(170,174,127,0.5)]' : 'border-[#EFEFEF]/50 group-hover:border-[#EFEFEF]'}`}>
                {sortBy === '' && <div className="w-2 h-2 rounded-full bg-[#AAAE7F]" />}
              </div>
              <span className="text-sm font-medium text-white font-medium group-hover:text-white font-bold drop-shadow-lg transition-colors">Recommended</span>
            </label>
            <label className="flex items-center gap-4 cursor-pointer group p-2 rounded-lg hover:bg-[#F7F7F7]/5 transition-colors">
              <input type="radio" name="sort" checked={sortBy === 'price_asc'} onChange={() => setSortBy('price_asc')} className="hidden" />
              <div className={`w-4 h-4 rounded-full flex items-center justify-center border-2 transition-all ${sortBy === 'price_asc' ? 'border-[#AAAE7F] shadow-[0_0_10px_rgba(170,174,127,0.5)]' : 'border-[#EFEFEF]/50 group-hover:border-[#EFEFEF]'}`}>
                {sortBy === 'price_asc' && <div className="w-2 h-2 rounded-full bg-[#AAAE7F]" />}
              </div>
              <span className="text-sm font-medium text-white font-medium group-hover:text-white font-bold drop-shadow-lg transition-colors">Price: Low to High</span>
            </label>
            <label className="flex items-center gap-4 cursor-pointer group p-2 rounded-lg hover:bg-[#F7F7F7]/5 transition-colors">
              <input type="radio" name="sort" checked={sortBy === 'price_desc'} onChange={() => setSortBy('price_desc')} className="hidden" />
              <div className={`w-4 h-4 rounded-full flex items-center justify-center border-2 transition-all ${sortBy === 'price_desc' ? 'border-[#AAAE7F] shadow-[0_0_10px_rgba(170,174,127,0.5)]' : 'border-[#EFEFEF]/50 group-hover:border-[#EFEFEF]'}`}>
                {sortBy === 'price_desc' && <div className="w-2 h-2 rounded-full bg-[#AAAE7F]" />}
              </div>
              <span className="text-sm font-medium text-white font-medium group-hover:text-white font-bold drop-shadow-lg transition-colors">Price: High to Low</span>
            </label>
        </FilterAccordion>

      </aside>
    </main>
  );
}

export default function SearchPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-[#143109] text-white font-bold drop-shadow-lg flex items-center justify-center">Loading dashboard...</div>}>
      <SearchDashboard />
    </Suspense>
  );
}
