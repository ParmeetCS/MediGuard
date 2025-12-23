"""
Health Search Agent - MediGuard Drift AI
Uses Google Search + OpenRouter AI for evidence-based health information
Provides reliable medical resources and information with real web search
"""

import requests
from typing import Dict, Any, Optional, List
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Get OpenRouter API credentials
VISION_API_KEY = os.getenv("VISION_API_KEY")
VISION_MODEL = os.getenv("VISION_MODEL", "google/gemini-2.0-flash-exp:free")


class HealthSearchAgent:
    """
    AI Health Assistant Agent with Google Search + OpenRouter
    
    Uses Google Search + OpenRouter AI to provide:
    - Evidence-based health information from reliable sources
    - Reliable medical resources with source URLs
    - Comprehensive health guidance for Indian users
    - Up-to-date health information in English
    """
    
    def __init__(self):
        """Initialize the Health Search Agent with OpenRouter"""
        self.model_name = VISION_MODEL
        self.api_key = VISION_API_KEY
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.is_ready = False
        self._configure()
    
    def _configure(self) -> None:
        """Configure the OpenRouter API"""
        if not self.api_key or self.api_key == "your_api_key_here":
            print("⚠️ Health Search Agent: OpenRouter API key not configured")
            self.is_ready = False
            return
        
        try:
            self.is_ready = True
            print(f"✅ Health Search Agent initialized with Brave Search + OpenRouter ({self.model_name})")
                
        except Exception as e:
            print(f"⚠️ Error configuring Health Search Agent: {e}")
            self.is_ready = True  # Continue anyway, will handle errors during actual use
    
    def _search_web(self, query: str, max_results: int = 8) -> List[Dict[str, str]]:
        """
        Perform web search using direct Google scraping (no API key needed)
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            List of search results with title, link, and snippet
        """
        try:
            # Detect if this is an India-specific query
            india_terms = ["india", "indian", "delhi", "mumbai", "bangalore", "chennai", "kolkata", 
                          "hyderabad", "pune", "ahmedabad", "jaipur", "lucknow", "kanpur", "nagpur",
                          "indore", "bhopal", "chandigarh", "ludhiana", "jalandhar", "punjab", "haryana",
                          "doctor", "doctors", "clinic", "hospital", "medical center"]
            
            is_india_query = any(term in query.lower() for term in india_terms)
            
            # Detect if looking for doctors/clinics
            is_provider_search = any(word in query.lower() for word in ["doctor", "doctors", "clinic", "hospital", "physician", "specialist", "dentist", "surgeon"])
            
            # Build search query
            if is_provider_search and is_india_query:
                city = None
                for term in india_terms:
                    if term in query.lower() and len(term) > 5:
                        city = term.title()
                        break
                
                if city:
                    search_query = f'best doctors {city} India contact'
                else:
                    search_query = f'{query} India contact'
            elif is_india_query:
                search_query = f"{query} India"
            else:
                search_query = f"{query} health medical"
            
            print(f"   Searching Google: {search_query}")
            
            # Use Google search with proper headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            # Google search URL
            google_url = "https://www.google.com/search"
            params = {
                'q': search_query,
                'num': max_results * 2,
                'hl': 'en'
            }
            
            response = requests.get(google_url, params=params, headers=headers, timeout=15)
            
            if response.status_code == 200:
                # Parse HTML to extract search results
                import re
                from urllib.parse import unquote
                html = response.text
                
                # Extract search result blocks
                results = []
                
                # Multiple patterns to catch different Google result formats
                # Pattern 1: Standard h3 titles
                title_patterns = [
                    r'<h3[^>]*class="[^"]*"[^>]*>([^<]+)</h3>',
                    r'<h3[^>]*>([^<]+)</h3>',
                    r'<div[^>]*role="heading"[^>]*>([^<]+)</div>'
                ]
                
                # Pattern 2: Link extraction with better URL handling
                link_patterns = [
                    r'<a[^>]+href="/url\?q=(https?://[^&"]+)',
                    r'<a[^>]+href="(https?://[^"]+)"[^>]*><h3',
                    r'<a[^>]+jsname="[^"]*"[^>]+href="(https?://[^"]+)"'
                ]
                
                # Pattern 3: Snippet extraction with multiple fallbacks
                snippet_patterns = [
                    r'<div[^>]*class="[^"]*VwiC3b[^"]*"[^>]*>([^<]+)</div>',
                    r'<div[^>]*data-sncf="[^"]*"[^>]*>([^<]+)</div>',
                    r'<span[^>]*class="[^"]*st[^"]*"[^>]*>([^<]+)</span>'
                ]
                
                # Try all patterns
                titles = []
                for pattern in title_patterns:
                    titles.extend(re.findall(pattern, html))
                    if len(titles) >= max_results:
                        break
                
                links = []
                for pattern in link_patterns:
                    found_links = re.findall(pattern, html)
                    for link in found_links:
                        # Clean and decode URL
                        clean_link = unquote(link.split('&')[0])
                        if clean_link not in links:
                            links.append(clean_link)
                    if len(links) >= max_results:
                        break
                
                snippets = []
                for pattern in snippet_patterns:
                    snippets.extend(re.findall(pattern, html))
                    if len(snippets) >= max_results:
                        break
                
                # Combine results - be flexible with mismatched counts
                min_count = min(len(titles), len(links))
                for i in range(min(min_count, max_results * 2)):
                    title = titles[i] if i < len(titles) else ''
                    link = links[i] if i < len(links) else ''
                    snippet = snippets[i] if i < len(snippets) else ''
                    
                    # Skip invalid or Google's own links
                    if not link or 'google.com' in link or 'youtube.com' in link:
                        continue
                    
                    # Ensure valid URL
                    if not link.startswith('http'):
                        continue
                    
                    if title and link:
                        results.append({
                            'title': title.strip(),
                            'link': link.strip(),
                            'snippet': snippet.strip() if snippet else title.strip()
                        })
                
                if results:
                    print(f"✅ Got {len(results)} results from Google")
                    
                    # Filter for relevance
                    query_keywords = set(query.lower().split())
                    filtered_results = []
                    
                    for result in results:
                        title = result.get('title', '').lower()
                        snippet = result.get('snippet', '').lower()
                        url = result.get('link', '').lower()
                        
                        # Check relevance
                        relevance_score = 0
                        for keyword in query_keywords:
                            if len(keyword) > 2:
                                if keyword in title:
                                    relevance_score += 3
                                if keyword in snippet:
                                    relevance_score += 1
                                if keyword in url:
                                    relevance_score += 1
                        
                        # Boost Indian sites
                        if is_india_query and ('.in/' in url or '.in' in url or 'india' in url or 'india' in title):
                            relevance_score += 5
                        
                        # Boost trusted health sites
                        if any(domain in url for domain in ['mayoclinic', 'webmd', 'healthline', 'nih.gov', 'cdc.gov', 'who.int', 'health.com']):
                            relevance_score += 3
                        
                        if relevance_score >= 1:
                            filtered_results.append({
                                'result': result,
                                'score': relevance_score
                            })
                    
                    # If no filtered results, use all
                    if not filtered_results and results:
                        print("   ⚠️ No filtered results, using all")
                        filtered_results = [{'result': r, 'score': 1} for r in results]
                    
                    # Sort by score
                    filtered_results.sort(key=lambda x: x['score'], reverse=True)
                    
                    # Format results
                    unique_results = []
                    seen_urls = set()
                    
                    for item in filtered_results:
                        result = item['result']
                        url = result.get('link', '')
                        if url and url not in seen_urls:
                            seen_urls.add(url)
                            unique_results.append({
                                'title': result.get('title', 'No title'),
                                'link': url,
                                'snippet': result.get('snippet', '')[:300]
                            })
                            
                        if len(unique_results) >= max_results:
                            break
                    
                    if unique_results:
                        print(f"✅ Returning {len(unique_results)} relevant results")
                        return unique_results
                else:
                    print("   ⚠️ No results extracted from Google HTML")
                    # Try to provide fallback results
                    return self._get_fallback_results(query, is_india_query)
            else:
                print(f"   ⚠️ Google returned status {response.status_code}")
                return self._get_fallback_results(query, is_india_query)
            
            return []
                
        except Exception as e:
            print(f"❌ Search error: {str(e)}")
            import traceback
            traceback.print_exc()
            # Provide fallback results even on error
            return self._get_fallback_results(query, False)
    
    def _get_fallback_results(self, query: str, is_india_query: bool = False) -> List[Dict[str, str]]:
        """
        Provide curated trusted health sources as fallback when search fails
        
        Args:
            query: Original search query
            is_india_query: Whether query is India-specific
            
        Returns:
            List of trusted health resource results
        """
        print("   📚 Providing curated trusted health resources")
        
        # Determine query type for better fallback sources
        is_symptom = any(word in query.lower() for word in ['symptom', 'pain', 'ache', 'fever', 'cough', 'headache'])
        is_condition = any(word in query.lower() for word in ['disease', 'diabetes', 'cancer', 'heart', 'hypertension'])
        is_treatment = any(word in query.lower() for word in ['treatment', 'cure', 'medicine', 'therapy', 'medication'])
        is_prevention = any(word in query.lower() for word in ['prevent', 'avoid', 'reduce risk', 'healthy'])
        
        fallback_results = []
        
        if is_india_query:
            # India-specific resources
            fallback_results.extend([
                {
                    'title': 'National Health Portal of India',
                    'link': 'https://www.nhp.gov.in/',
                    'snippet': 'Official health information portal by Ministry of Health & Family Welfare, Government of India. Comprehensive health information for Indian citizens.'
                },
                {
                    'title': 'AIIMS Delhi - Health Information',
                    'link': 'https://www.aiims.edu/en.html',
                    'snippet': 'All India Institute of Medical Sciences, premier medical institution providing health education and information for Indian patients.'
                },
                {
                    'title': 'Indian Medical Association',
                    'link': 'https://www.ima-india.org/',
                    'snippet': 'National organization of physicians in India. Find verified doctors and health information specific to India.'
                }
            ])
        
        # General trusted health resources
        if is_symptom:
            fallback_results.extend([
                {
                    'title': 'Mayo Clinic - Symptoms Guide',
                    'link': 'https://www.mayoclinic.org/symptoms/',
                    'snippet': 'Comprehensive symptom checker and information from Mayo Clinic, one of the world\'s leading medical centers.'
                },
                {
                    'title': 'WebMD Symptom Checker',
                    'link': 'https://symptoms.webmd.com/',
                    'snippet': 'Interactive symptom checker tool to understand your symptoms and when to see a doctor.'
                }
            ])
        
        if is_condition or is_treatment:
            fallback_results.extend([
                {
                    'title': 'National Institutes of Health (NIH)',
                    'link': 'https://www.nih.gov/health-information',
                    'snippet': 'Evidence-based health information from the U.S. National Institutes of Health, covering diseases, conditions, and treatments.'
                },
                {
                    'title': 'Healthline - Medical Information',
                    'link': 'https://www.healthline.com/',
                    'snippet': 'Medically reviewed health information covering conditions, treatments, and wellness advice.'
                }
            ])
        
        if is_prevention:
            fallback_results.extend([
                {
                    'title': 'CDC - Disease Prevention',
                    'link': 'https://www.cdc.gov/prevention/',
                    'snippet': 'Centers for Disease Control and Prevention - official guidelines for disease prevention and healthy living.'
                }
            ])
        
        # Always include WHO
        fallback_results.append({
            'title': 'World Health Organization (WHO)',
            'link': 'https://www.who.int/health-topics',
            'snippet': 'Global health topics and information from the World Health Organization, the leading international health authority.'
        })
        
        print(f"   ✅ Provided {len(fallback_results)} trusted sources")
        return fallback_results[:8]  # Return up to 8 sources
    
    def search_health_info(
        self,
        query: str,
        user_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Search for health information using OpenRouter AI + DuckDuckGo
        
        Args:
            query (str): User's health question or topic
            user_context (dict, optional): User's health context for personalization
        
        Returns:
            Dict containing:
                - success (bool): Whether the search succeeded
                - response (str): Formatted response with information and sources
                - sources (list): List of actual search result sources
                - error (str): Error message if failed
                - search_query (str): The actual query used
        """
        if not self.is_ready:
            return {
                "success": False,
                "response": "",
                "sources": [],
                "error": "Health Search Agent not configured. Please set VISION_API_KEY.",
                "search_query": query
            }
        
        if not query or len(query.strip()) < 3:
            return {
                "success": False,
                "response": "",
                "sources": [],
                "error": "Please provide a valid health question or topic.",
                "search_query": query
            }
        
        try:
            # First, perform web search
            print(f"🔍 Searching web for: {query}")
            search_results = self._search_web(query, max_results=8)
            
            # Even if web search fails, we have fallback trusted sources
            # So we continue to AI analysis
            if search_results:
                try:
                    # Build comprehensive system prompt
                    system_prompt = self._build_system_prompt(user_context)
                    
                    # Determine if we have specific search results or just trusted sources
                    has_specific_results = any('snippet' in r and len(r.get('snippet', '')) > 50 for r in search_results)
                    
                    # Add search results to the prompt in a clear format
                    if has_specific_results:
                        search_context = "\n\n**WEB SEARCH RESULTS (Latest Medical Information):**\n\n"
                    else:
                        search_context = "\n\n**TRUSTED HEALTH RESOURCES (Use as reference sources):**\n\n"
                        search_context += "Note: Specific search results were unavailable. Provide general evidence-based information using your medical knowledge, and refer users to these trusted sources for more details.\n\n"
                    
                    for idx, result in enumerate(search_results, 1):
                        search_context += f"SOURCE {idx}:\n"
                        search_context += f"Title: {result['title']}\n"
                        search_context += f"URL: {result['link']}\n"
                        if result.get('snippet'):
                            search_context += f"Content: {result['snippet']}\n\n"
                        else:
                            search_context += f"Description: Trusted medical resource\n\n"
                    
                    # Construct the full query with detailed instructions
                    full_query = f"""{system_prompt}

{search_context}

USER'S QUERY: {query}

CRITICAL: Respond ONLY in ENGLISH language. Do not use Chinese, Hindi, or any other language.

TASK:
Analyze the search results above and determine if this is:
A) A healthcare provider search (finding doctors/clinics in Indian locations), OR
B) A health information query (symptoms, conditions, treatments, advice)

RESPONSE FORMAT (Write in ENGLISH only):

**If Provider Search in India (Type A):**
## 🏥 Top Doctors/Clinics in [Indian City]

Based on web search results:

1. **[Doctor/Clinic Name]** - [Specialty]
   - Location: [Address in India]
   - Details: [qualifications, ratings from search]
   - Source: SOURCE [number]

2. **[Next option]**
   - Location: [Address]
   - Details: [key info]
   - Source: SOURCE [number]

*(List top 5-6 options found in search results)*

## 📞 How to Choose
- Verify with Indian Medical Association
- Check Google reviews and ratings
- Confirm location and visiting hours
- Contact directly for appointments

---

**If Health Information (Type B):**
## Answer
[Direct, clear answer in English]

## Detailed Information
[Comprehensive explanation in English using search results]

## What You Can Do
[Practical advice in English]

## Important Safety Notes
[When to seek medical help - in English]

## Sources Referenced
[List SOURCE numbers used]

---

REMEMBER: Write entire response in ENGLISH language only. Extract and present ACTUAL information from search results.

Format the response in a patient-friendly way with clear sections."""

                    # Try to generate response using OpenRouter
                    if self.is_ready:
                        print("🤖 Generating AI response with search context...")
                        
                        headers = {
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json",
                            "HTTP-Referer": "https://mediaguard-ai.com",
                            "X-Title": "MediGuard AI Health Assistant"
                        }
                        
                        payload = {
                            "model": self.model_name,
                            "messages": [
                                {"role": "system", "content": "You are a helpful AI Health Assistant for users in INDIA. You MUST respond ONLY in ENGLISH language. NEVER use Chinese, Hindi, Punjabi, or any language other than ENGLISH. Focus on Indian healthcare context - Indian cities, Indian doctors, Indian medical facilities. If you receive sources in other languages, translate the key information to ENGLISH."},
                                {"role": "user", "content": f"IMPORTANT: Write your ENTIRE response in ENGLISH language only. No Chinese characters allowed.\n\n{full_query}"}
                            ],
                            "temperature": 0.3,
                            "max_tokens": 2048
                        }
                        
                        # Try with retries and exponential backoff
                        import time
                        max_retries = 3
                        response_text = None
                        
                        for attempt in range(max_retries):
                            try:
                                response = requests.post(self.api_url, headers=headers, json=payload, timeout=45)
                                
                                if response.status_code == 200:
                                    response_data = response.json()
                                    response_text = response_data.get('choices', [{}])[0].get('message', {}).get('content', '')
                                    
                                    if response_text:
                                        # Check for Chinese characters
                                        has_chinese = any('\u4e00' <= char <= '\u9fff' for char in response_text)
                                        
                                        if has_chinese:
                                            print(f"⚠️ Detected non-English response, retrying... (Attempt {attempt+1}/{max_retries})")
                                            response_text = None
                                            if attempt < max_retries - 1:
                                                time.sleep(2 ** (attempt + 1))  # Exponential backoff: 2s, 4s, 8s
                                                continue
                                            else:
                                                # Last attempt failed, use fallback
                                                print("⚠️ All attempts returned non-English, using direct search results")
                                                response_text = self._format_search_results_fallback(query, search_results)
                                        else:
                                            print(f"✅ AI response generated successfully in English")
                                            break
                                elif response.status_code == 429:
                                    # Rate limit error - need longer wait
                                    retry_after = int(response.headers.get('Retry-After', 10))
                                    wait_time = max(retry_after, 2 ** (attempt + 2))  # At least 4s, 8s, 16s
                                    print(f"⚠️ Rate limit (429) - waiting {wait_time}s before retry (Attempt {attempt+1}/{max_retries})")
                                    if attempt < max_retries - 1:
                                        time.sleep(wait_time)
                                    else:
                                        print("⚠️ Rate limit exceeded, using direct search results")
                                else:
                                    print(f"⚠️ OpenRouter API error: {response.status_code} (Attempt {attempt+1}/{max_retries})")
                                    if attempt < max_retries - 1:
                                        time.sleep(2 ** (attempt + 1))  # Exponential backoff
                            except requests.exceptions.Timeout:
                                print(f"⚠️ Request timeout (Attempt {attempt+1}/{max_retries})")
                                if attempt < max_retries - 1:
                                    time.sleep(2 ** (attempt + 1))
                            except Exception as e:
                                print(f"⚠️ Request error: {e} (Attempt {attempt+1}/{max_retries})")
                                if attempt < max_retries - 1:
                                    time.sleep(2 ** (attempt + 1))
                        
                        # If all retries failed, use fallback
                        if not response_text:
                            print("⚠️ All API attempts failed, using direct search results")
                            response_text = self._format_search_results_fallback(query, search_results)
                    else:
                        # Fallback: Return formatted search results without AI analysis
                        response_text = self._format_search_results_fallback(query, search_results)
                        
                except Exception as api_error:
                    # If API fails, use fallback
                    error_msg = str(api_error).lower()
                    print(f"⚠️ API error: {api_error}, using search results directly")
                    response_text = self._format_search_results_fallback(query, search_results)
                
                # Combine search result URLs - ONLY show actual search results
                sources = []
                
                # Add ALL actual search result sources (not just top 5)
                for result in search_results[:8]:  # Up to 8 search results
                    if result.get('link'):
                        sources.append({
                            'type': 'web_source',  # Add type for UI filtering
                            'title': result['title'],
                            'url': result['link'],
                            'description': result['snippet'][:200] + '...' if len(result['snippet']) > 200 else result['snippet']
                        })
                
                # Don't add generic trusted sources - only show actual search results
                # This ensures sources are relevant to the specific query
                
                print(f"✅ Generated response with {len(sources)} actual search result sources")
                
                return {
                    "success": True,
                    "response": response_text,
                    "sources": sources,
                    "error": None,
                    "search_query": query,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            error_msg = str(e)
            
            # Handle specific errors
            if "API key" in error_msg:
                error_msg = "Invalid Google API key. Please check configuration."
            elif "quota" in error_msg.lower():
                error_msg = "API quota exceeded. Please try again later."
            elif "safety" in error_msg.lower():
                error_msg = "Response blocked by safety filters. Please rephrase your question."
            
            return {
                "success": False,
                "response": "",
                "sources": [],
                "error": error_msg,
                "search_query": query
            }
    
    def _build_system_prompt(self, user_context: Optional[Dict[str, Any]] = None) -> str:
        """Build system prompt with user context"""
        base_prompt = """You are an AI Health Assistant helping users in INDIA. Always respond in ENGLISH language only.

**CRITICAL INSTRUCTIONS:**
- ALWAYS write your response in ENGLISH language
- Focus on Indian healthcare context (Indian doctors, Indian cities, Indian medical system)
- Extract information from English sources when available
- If sources are in other languages, translate key information to English

**TYPE 1: Health Information Queries** (symptoms, conditions, treatments, exercises, prevention)
When users ask about health topics, provide:
- Clear, evidence-based health information
- Practical advice and recommendations relevant to Indian context
- Safety warnings and when to see a doctor
- Citations from search results

**TYPE 2: Healthcare Provider Searches** (finding doctors, clinics, hospitals in India)
When users ask to find doctors or medical facilities in Indian locations, provide:
- Summary of top doctors/facilities from search results
- Specialties, qualifications, and ratings if mentioned
- Contact information and exact locations from search results
- Recommendation to verify credentials with Indian Medical Association

**Important Guidelines:**
- **RESPOND ONLY IN ENGLISH** - Never use Chinese, Hindi, Punjabi or other languages
- Analyze the search results and extract relevant information
- For Indian provider searches, focus on doctors/clinics in specified Indian cities
- For health information, synthesize and explain in clear English
- Always cite your sources by referencing SOURCE numbers
- If search results don't match the query, say so clearly
- Focus on general health information, not personal medical advice
- Include safety warnings for any health topics with risks
- Be clear about uncertainty and limitations of information
- Format responses with clear sections and bullet points"""
        
        # Add user context if provided
        if user_context:
            context_section = "\n\n**User Context:**"
            if user_context.get('age'):
                context_section += f"\n- Age: {user_context['age']}"
            if user_context.get('health_conditions'):
                context_section += f"\n- Health conditions: {user_context['health_conditions']}"
            if user_context.get('recent_metrics'):
                context_section += f"\n- Recent health metrics tracked: {user_context['recent_metrics']}"
            
            base_prompt += context_section
        
        return base_prompt
    
    def _get_trusted_sources(self) -> List[Dict[str, str]]:
        """Get list of trusted health resource URLs"""
        return [
            {"type": "web_source", "url": "https://www.mayoclinic.org/", "title": "Mayo Clinic"},
            {"type": "web_source", "url": "https://www.nih.gov/health-information", "title": "National Institutes of Health (NIH)"},
            {"type": "web_source", "url": "https://www.cdc.gov/", "title": "Centers for Disease Control (CDC)"},
            {"type": "web_source", "url": "https://www.webmd.com/", "title": "WebMD"},
            {"type": "web_source", "url": "https://my.clevelandclinic.org/health", "title": "Cleveland Clinic"}
        ]
    
    def get_health_resources(self, topic: str) -> Dict[str, Any]:
        """
        Get curated health resources for a specific topic
        
        Args:
            topic (str): Health topic (e.g., "balance exercises", "fall prevention")
        
        Returns:
            Dict containing resources, exercises, and tips
        """
        query = f"What are the best {topic} resources, exercises, and evidence-based practices? Include links to trusted health websites and practical tips."
        
        return self.search_health_info(query)
    
    def _format_search_results_fallback(self, query: str, search_results: List[Dict]) -> str:
        """
        Format search results without AI analysis (fallback when API fails)
        
        Args:
            query: Original user query
            search_results: List of search results from DuckDuckGo
            
        Returns:
            Formatted string with search results
        """
        response = f"## 🔍 Search Results: {query}\n\n"
        response += "**Direct web search results** (AI analysis temporarily unavailable):\n\n"
        
        response += "---\n\n"
        
        for idx, result in enumerate(search_results[:8], 1):
            response += f"### 📌 Result {idx}: {result['title']}\n\n"
            response += f"{result['snippet']}\n\n"
            response += f"🔗 **Visit:** [{result['link']}]({result['link']})\n\n"
            response += "---\n\n"
        
        response += "\n## ⚠️ Important Note\n\n"
        response += "These are direct search results. Please verify information with official sources and healthcare professionals.\n"
        
        return response
    
    def explain_health_term(self, term: str) -> Dict[str, Any]:
        """
        Explain a medical or health term in simple language
        
        Args:
            term (str): Medical term to explain
        
        Returns:
            Dict containing explanation and resources
        """
        query = f"Explain '{term}' in simple, patient-friendly language. Include what it means, why it matters, and links to trusted medical sources for more information."
        
        return self.search_health_info(query)


# ========================================
# GLOBAL INSTANCE
# ========================================

# Create singleton instance
_health_search_agent = None


def get_health_search_agent() -> HealthSearchAgent:
    """
    Get the global Health Search Agent instance
    
    Returns:
        HealthSearchAgent: The agent instance
    """
    global _health_search_agent
    if _health_search_agent is None:
        _health_search_agent = HealthSearchAgent()
    return _health_search_agent


# ========================================
# CONVENIENCE FUNCTIONS
# ========================================

def search_health_info(query: str, user_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Convenience function to search health information
    
    Args:
        query (str): Health question or topic
        user_context (dict, optional): User context for personalization
    
    Returns:
        Dict: Search results with sources
    """
    agent = get_health_search_agent()
    return agent.search_health_info(query, user_context)


def get_health_resources(topic: str) -> Dict[str, Any]:
    """
    Get health resources for a topic
    
    Args:
        topic (str): Health topic
    
    Returns:
        Dict: Resources and information
    """
    agent = get_health_search_agent()
    return agent.get_health_resources(topic)


def explain_health_term(term: str) -> Dict[str, Any]:
    """
    Explain a health term
    
    Args:
        term (str): Medical term
    
    Returns:
        Dict: Explanation and resources
    """
    agent = get_health_search_agent()
    return agent.explain_health_term(term)
