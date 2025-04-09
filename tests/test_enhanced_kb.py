from knowledge_base.elasticrun_kb import ElasticRunKnowledgeBase
from knowledge_base.enhanced_kb import EnhancedKnowledgeBase
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_enhanced_knowledge_base():
    print("\nTesting Enhanced Knowledge Base...\n")
    
    # Initialize knowledge bases
    base_kb = ElasticRunKnowledgeBase()
    enhanced_kb = EnhancedKnowledgeBase(base_kb)
    
    # Test queries
    test_queries = [
        "Can you explain Mity to me like I'm 5 years old?",
        "Compare Mity with other identity verification solutions in the market",
        "I'm a logistics company with 1000 employees. How can Mity help me?",
        "Summarize the key benefits of Mity in a tweet (280 characters)",
        "What makes Mity different from traditional identity verification systems?",
        "If I'm concerned about security, why should I trust Mity?",
        "Give me a real-world example of how Mity prevented fraud",
        "What's the ROI of implementing Mity for a mid-sized company?",
        "How does Mity handle edge cases like employees wearing masks or helmets?",
        "Can you break down Mity's pricing model for me?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = enhanced_kb.query(query)
        print(f"Classification: {result['classification']}")
        print(f"Answer: {result['answer']}")
        print(f"Sources: {result['sources']}")
        print("-" * 80)

if __name__ == "__main__":
    test_enhanced_knowledge_base() 