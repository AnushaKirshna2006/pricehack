import { NextResponse } from 'next/server';

export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const q = searchParams.get('q');
  
  if (!q) return NextResponse.json([]);
  
  try {
    const res = await fetch(`https://completion.amazon.com/search/complete?search-alias=aps&client=amazon-search-ui&mkt=1&q=${encodeURIComponent(q)}`);
    const data = await res.json();
    return NextResponse.json(data[1] || []);
  } catch (error) {
    return NextResponse.json([]);
  }
}
