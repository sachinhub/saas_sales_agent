#!/usr/bin/env python3
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crawler.update_knowledge_base import update_knowledge_base

if __name__ == "__main__":
    print("Starting knowledge base update process...")
    update_knowledge_base()
    print("Knowledge base update complete!") 