"""
Test Health Search Agent with Google Search Grounding
Quick validation of the ADK-powered health information search
"""

from agents.health_search_agent import search_health_info, get_health_resources, explain_health_term

def test_basic_search():
    """Test basic health information search"""
    print("🔍 Testing Basic Health Search...")
    print("=" * 60)
    
    query = "What are the best balance exercises for seniors?"
    result = search_health_info(query)
    
    if result['success']:
        print(f"✅ Search successful!")
        print(f"\nQuery: {result['search_query']}")
        print(f"\nResponse:\n{result['response'][:500]}...")
        
        if result.get('sources'):
            print(f"\n📚 Found {len(result['sources'])} sources")
            for idx, source in enumerate(result['sources'][:3], 1):
                if source.get('type') == 'web_source':
                    print(f"{idx}. {source.get('title', 'Source')} - {source.get('url', 'N/A')[:60]}")
    else:
        print(f"❌ Search failed: {result['error']}")
    
    print("\n" + "=" * 60)


def test_with_context():
    """Test search with user context"""
    print("\n🧑 Testing Search with User Context...")
    print("=" * 60)
    
    query = "exercises to improve stability"
    user_context = {
        'age': 65,
        'health_conditions': 'monitoring balance',
        'recent_metrics': 'stability trending down'
    }
    
    result = search_health_info(query, user_context)
    
    if result['success']:
        print(f"✅ Personalized search successful!")
        print(f"\nQuery: {result['search_query']}")
        print(f"\nContext-aware response:\n{result['response'][:500]}...")
    else:
        print(f"❌ Search failed: {result['error']}")
    
    print("\n" + "=" * 60)


def test_get_resources():
    """Test getting health resources for a topic"""
    print("\n📚 Testing Get Health Resources...")
    print("=" * 60)
    
    topic = "fall prevention"
    result = get_health_resources(topic)
    
    if result['success']:
        print(f"✅ Resources retrieved!")
        print(f"\nTopic: {topic}")
        print(f"\nResources:\n{result['response'][:500]}...")
    else:
        print(f"❌ Failed: {result['error']}")
    
    print("\n" + "=" * 60)


def test_explain_term():
    """Test explaining a medical term"""
    print("\n📖 Testing Medical Term Explanation...")
    print("=" * 60)
    
    term = "proprioception"
    result = explain_health_term(term)
    
    if result['success']:
        print(f"✅ Term explained!")
        print(f"\nTerm: {term}")
        print(f"\nExplanation:\n{result['response'][:500]}...")
    else:
        print(f"❌ Failed: {result['error']}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    print("\n🧪 HEALTH SEARCH AGENT TEST SUITE")
    print("=" * 60)
    print("Testing ADK-powered Google Search for health information\n")
    
    # Run tests
    test_basic_search()
    test_with_context()
    test_get_resources()
    test_explain_term()
    
    print("\n✅ All tests complete!")
    print("\n💡 Note: Test results depend on:")
    print("   - Valid GOOGLE_API_KEY in .env")
    print("   - Internet connection")
    print("   - Google Search grounding availability")
