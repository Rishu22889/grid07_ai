import os
from typing import List, Dict
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()


class RealSearchTool:
    """Real web search using Tavily API."""
    
    def __init__(self):
        self.api_key = os.getenv("TAVILY_API_KEY")
        if self.api_key:
            self.client = TavilyClient(api_key=self.api_key)
            self.available = True
        else:
            self.available = False
            print("⚠️  TAVILY_API_KEY not found, real search unavailable")
    
    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Search the web for real-time information.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            List of search results with title, content, url
        """
        if not self.available:
            return self._fallback_results(query)
        
        try:
            response = self.client.search(
                query=query,
                max_results=max_results,
                search_depth="basic",
                include_domains=[],
                exclude_domains=[]
            )
            
            results = []
            for result in response.get("results", []):
                results.append({
                    "title": result.get("title", ""),
                    "content": result.get("content", ""),
                    "url": result.get("url", ""),
                    "score": result.get("score", 0.0)
                })
            
            return results
            
        except Exception as e:
            print(f"❌ Tavily search error: {e}")
            return self._fallback_results(query)
    
    def _fallback_results(self, query: str) -> List[Dict]:
        """Fallback when API is unavailable."""
        return [{
            "title": f"Search: {query}",
            "content": "Real search unavailable. Please add TAVILY_API_KEY to .env file.",
            "url": "https://tavily.com",
            "score": 0.0
        }]


real_search = RealSearchTool()


def search_web(query: str, max_results: int = 5) -> List[Dict]:
    """
    Convenience function for web search.
    
    Usage:
        results = search_web("latest AI news")
    """
    return real_search.search(query, max_results)
