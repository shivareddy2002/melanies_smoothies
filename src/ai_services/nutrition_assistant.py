"""
Generative AI Services: RAG-based Nutrition Assistant & Recommendation Engine
Integrates OpenAI/Gemini with vector embeddings for semantic search
"""

import streamlit as st
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pandas as pd
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class NutritionAssistant:
    """RAG-based Nutrition Assistant using LLM"""
    
    def __init__(self, session, openai_key: str):
        self.session = session
        self.llm = ChatOpenAI(
            openai_api_key=openai_key,
            model="gpt-4",
            temperature=0.7
        )
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_key)
        self.vectorstore = None
    
    def build_knowledge_base(self) -> bool:
        """Build nutrition knowledge base from Snowflake Gold layer"""
        try:
            query = """
            SELECT
                FRUIT_NAME,
                CONCAT(
                    'Fruit: ', FRUIT_NAME, '. ',
                    'Category: ', CATEGORY, '. ',
                    'Calories: ', CALORIES, ' kcal per 100g. ',
                    'Protein: ', PROTEIN, 'g. ',
                    'Fiber: ', FIBER, 'g. ',
                    'Sugar: ', SUGAR, 'g. ',
                    'Health Benefits: ', 
                    CASE 
                        WHEN PROTEIN > 2 THEN 'High protein. '
                        WHEN FIBER > 3 THEN 'High fiber. '
                        WHEN SUGAR < 10 THEN 'Low sugar. '
                        ELSE ''
                    END,
                    'Recommendation Tags: ', RECOMMENDATION_TAGS
                ) as nutrition_info
            FROM GOLD.DIM_FRUITS
            """
            
            docs_df = self.session.sql(query).to_pandas()
            
            if docs_df.empty:
                logger.warning("⚠ No fruits in knowledge base")
                return False
            
            # Create document list
            documents = []
            for _, row in docs_df.iterrows():
                doc = {
                    'page_content': row['NUTRITION_INFO'],
                    'metadata': {'source': 'snowflake', 'fruit': row['FRUIT_NAME']}
                }
                documents.append(doc)
            
            # Build vector store
            self.vectorstore = Chroma.from_documents(
                documents=[{'page_content': d['page_content'], 
                           'metadata': d['metadata']} for d in documents],
                embedding=self.embeddings,
                collection_name="nutrition_kb"
            )
            
            logger.info(f"✓ Knowledge base built with {len(documents)} documents")
            return True
            
        except Exception as e:
            logger.error(f"✗ Knowledge base build failed: {e}")
            return False
    
    def query(self, user_query: str) -> str:
        """Query the nutrition assistant"""
        try:
            if not self.vectorstore:
                return "Knowledge base not initialized. Please build it first."
            
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vectorstore.as_retriever(),
                return_source_documents=False
            )
            
            response = qa_chain({"query": user_query})
            return response['result']
            
        except Exception as e:
            logger.error(f"✗ Query failed: {e}")
            return f"Error processing query: {str(e)}"
    
    def generate_smoothie_suggestions(self, health_goal: str, dietary_restrictions: List[str] = None) -> str:
        """Generate AI-powered smoothie suggestions"""
        
        restrictions_text = ", ".join(dietary_restrictions) if dietary_restrictions else "None"
        
        prompt = f"""
        Based on your expertise in nutrition, suggest a personalized smoothie recipe with:
        
        Health Goal: {health_goal}
        Dietary Restrictions: {restrictions_text}
        
        Please provide:
        1. Optimal fruit combination (max 3 fruits)
        2. Nutritional benefits
        3. Preparation instructions
        4. Health tips
        5. Estimated nutrition facts
        
        Format as a friendly recommendation.
        """
        
        response = self.llm.predict(prompt)
        return response

class RAGEngine:
    """General-purpose RAG (Retrieval-Augmented Generation) engine"""
    
    def __init__(self, openai_key: str):
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_key)
        self.vectorstore = None
        self.llm = ChatOpenAI(
            openai_api_key=openai_key,
            model="gpt-4",
            temperature=0.5
        )
    
    def create_collection(self, documents: List[str], collection_name: str = "default") -> bool:
        """Create vector store collection"""
        try:
            if not documents:
                return False
            
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            
            split_docs = []
            for doc in documents:
                chunks = splitter.split_text(doc)
                split_docs.extend(chunks)
            
            self.vectorstore = Chroma.from_texts(
                texts=split_docs,
                embedding=self.embeddings,
                collection_name=collection_name
            )
            
            logger.info(f"✓ Collection '{collection_name}' created with {len(split_docs)} chunks")
            return True
            
        except Exception as e:
            logger.error(f"✗ Collection creation failed: {e}")
            return False
    
    def retrieve_documents(self, query: str, k: int = 3) -> List[str]:
        """Retrieve relevant documents"""
        try:
            if not self.vectorstore:
                return []
            
            results = self.vectorstore.similarity_search(query, k=k)
            return [doc.page_content for doc in results]
            
        except Exception as e:
            logger.error(f"✗ Retrieval failed: {e}")
            return []
    
    def generate_answer(self, query: str, context_docs: List[str] = None) -> str:
        """Generate answer using RAG"""
        try:
            if not context_docs:
                context_docs = self.retrieve_documents(query)
            
            context = "\n\n".join(context_docs) if context_docs else "No context available"
            
            prompt_template = PromptTemplate(
                input_variables=["context", "question"],
                template="""Based on the following context, answer the question comprehensively:

Context:
{context}

Question: {question}

Answer:"""
            )
            
            prompt = prompt_template.format(context=context, question=query)
            response = self.llm.predict(prompt)
            
            return response
            
        except Exception as e:
            logger.error(f"✗ Answer generation failed: {e}")
            return f"Error generating answer: {str(e)}"

# Streamlit Component
def render_ai_assistant():
    """Render AI Assistant in Streamlit"""
    
    st.subheader("🤖 AI Nutrition Assistant")
    
    try:
        openai_key = st.secrets.get("openai", {}).get("api_key")
        if not openai_key:
            st.warning("OpenAI API key not configured")
            return
        
        session = st.connection("snowflake").session()
        
        # Initialize assistant
        assistant = NutritionAssistant(session, openai_key)
        
        # Sidebar controls
        with st.sidebar:
            if st.button("🔄 Build Knowledge Base"):
                with st.spinner("Building knowledge base..."):
                    success = assistant.build_knowledge_base()
                    if success:
                        st.success("Knowledge base built!")
                    else:
                        st.error("Failed to build knowledge base")
        
        # Chat interface
        st.write("Ask me about nutrition, smoothies, and health recommendations!")
        
        # Query input
        query = st.text_input("Your question:")
        
        if query:
            with st.spinner("Thinking..."):
                response = assistant.query(query)
                st.write(response)
        
        # Recommendations section
        st.markdown("### 💡 Get Personalized Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            health_goal = st.selectbox(
                "Health Goal",
                ["weight_loss", "muscle_gain", "high_protein", "diabetes_friendly", "low_sugar", "energy_boost"]
            )
        
        with col2:
            dietary_restrictions = st.multiselect(
                "Dietary Restrictions",
                ["Vegan", "Gluten-Free", "Nut-Free", "Dairy-Free"]
            )
        
        if st.button("Get Smoothie Recommendation"):
            with st.spinner("Generating recommendation..."):
                suggestion = assistant.generate_smoothie_suggestions(health_goal, dietary_restrictions)
                st.write(suggestion)
    
    except Exception as e:
        st.error(f"Error initializing AI Assistant: {e}")
