from flask import Blueprint, render_template, request, jsonify
from knowledge_base.elasticrun_kb import ElasticRunKnowledgeBase
from knowledge_base.enhanced_kb import EnhancedKnowledgeBase
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize knowledge bases
base_kb = ElasticRunKnowledgeBase()
enhanced_kb = EnhancedKnowledgeBase(base_kb)

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get('question', '')
    
    if not question:
        return jsonify({
            'answer': 'Please provide a question.',
            'sources': [],
            'classification': 'error'
        })
    
    # Query the enhanced knowledge base
    result = enhanced_kb.query(question)
    
    # Format the response
    response = {
        'answer': result['answer'],
        'sources': result['sources'],
        'classification': result['classification']
    }
    
    return jsonify(response) 