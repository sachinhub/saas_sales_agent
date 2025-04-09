from typing import List, Dict, Optional
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv
import json
from .elasticrun_kb import ElasticRunKnowledgeBase, Product, Industry

# Load environment variables
load_dotenv()

class EnhancedKnowledgeBase:
    def __init__(self, base_kb):
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Initialize LLM
        self.llm = HuggingFaceHub(
            repo_id="mistralai/Mistral-7B-Instruct-v0.2",
            model_kwargs={"temperature": 0.7, "max_length": 512},
            huggingfacehub_api_token=os.getenv("HUGGINGFACE_API_TOKEN")
        )
        
        # Create prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are an AI assistant for ElasticRun. Use the following context to answer the question.
            If the question asks for a summary, provide a concise summary.
            If the question asks for a comparison, compare the relevant items.
            If the question asks for specific details, provide those details.
            Always maintain a professional and helpful tone.

            Context:
            {context}

            Question: {question}

            Answer:"""
        )
        
        # Create LLM chain
        self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
        
        # Store base knowledge base
        self.base_kb = base_kb
        
        # Initialize vector store
        self.vector_store = self._create_vector_store()
    
    def _create_vector_store(self):
        """Create a vector store from the knowledge base content."""
        # Convert knowledge base to text
        kb_text = self._convert_kb_to_text()
        
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_text(kb_text)
        
        # Create vector store
        return FAISS.from_texts(texts, self.embeddings)
    
    def _convert_kb_to_text(self) -> str:
        """Convert the knowledge base content into a text format."""
        text = "ElasticRun Products and Solutions:\n\n"
        
        # Add products
        for product in self.base_kb.get_all_products():
            text += f"Product: {product.name}\n"
            text += f"Description: {product.description}\n"
            text += "Features:\n"
            for feature in product.features:
                text += f"- {feature.name}: {feature.description}\n"
            if product.benefits:
                text += "Benefits:\n"
                for benefit in product.benefits:
                    text += f"- {benefit}\n"
            if product.use_cases:
                text += "Use Cases:\n"
                for use_case in product.use_cases:
                    text += f"- {use_case}\n"
            text += "\n"
        
        # Add industries
        for industry in self.base_kb.get_all_industries():
            text += f"Industry: {industry.name}\n"
            text += f"Description: {industry.description}\n"
            if industry.use_cases:
                text += "Use Cases:\n"
                for use_case in industry.use_cases:
                    text += f"- {use_case}\n"
            if industry.challenges:
                text += "Challenges:\n"
                for challenge in industry.challenges:
                    text += f"- {challenge}\n"
            if industry.solutions:
                text += "Solutions:\n"
                for solution in industry.solutions:
                    text += f"- {solution}\n"
            text += "\n"
        
        return text
    
    def query(self, question: str) -> Dict:
        """Query the enhanced knowledge base with natural language."""
        try:
            # Get relevant documents
            docs = self.vector_store.similarity_search(question, k=3)
            
            # Extract relevant content
            context = "\n".join([doc.page_content for doc in docs])
            
            # Generate answer using LLM
            answer = self.llm_chain.run(context=context, question=question)
            
            return {
                "answer": answer,
                "sources": [doc.page_content for doc in docs],
                "classification": "general"
            }
        except Exception as e:
            return {
                "answer": f"I apologize, but I encountered an error: {str(e)}",
                "sources": [],
                "classification": "error"
            }
    
    def get_relevant_products(self, query: str) -> List[Product]:
        """Get products relevant to a query."""
        docs = self.vector_store.similarity_search(query, k=5)
        product_names = set()
        
        for doc in docs:
            if "Product:" in doc.page_content:
                product_name = doc.page_content.split("Product:")[1].split("\n")[0].strip()
                product_names.add(product_name)
        
        return [self.base_kb.get_product_by_name(name) for name in product_names if self.base_kb.get_product_by_name(name)]

    def get_relevant_industries(self, query: str) -> List[Industry]:
        """Get industries relevant to a query."""
        docs = self.vector_store.similarity_search(query, k=5)
        industry_names = set()
        
        for doc in docs:
            if "Industry:" in doc.page_content:
                industry_name = doc.page_content.split("Industry:")[1].split("\n")[0].strip()
                industry_names.add(industry_name)
        
        return [self.base_kb.get_industry_by_name(name) for name in industry_names if self.base_kb.get_industry_by_name(name)] 