"""
Streamlit UI for Grok API + mT5 Tasks
=====================================
A beautiful web interface for multilingual NLP tasks using Grok API.

Run with: streamlit run app.py
"""

import streamlit as st
import requests
import json
import time
import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum


# =============================================================================
# Configuration & Styling
# =============================================================================

st.set_page_config(
    page_title="mT5 + Grok API",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .task-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .score-high { color: #28a745; font-weight: bold; }
    .score-medium { color: #ffc107; font-weight: bold; }
    .score-low { color: #dc3545; font-weight: bold; }
    .stTextArea textarea { font-size: 16px; }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# Grok Client
# =============================================================================

class GroqModel(Enum):
    LLAMA_3_3_70B = "llama-3.3-70b-versatile"
    LLAMA_3_1_8B = "llama-3.1-8b-instant"
    MIXTRAL_8X7B = "mixtral-8x7b-32768"
    GEMMA2_9B = "gemma2-9b-it"


@dataclass
class GroqResponse:
    text: str
    model: str
    usage: Dict[str, int]
    latency_ms: float
    success: bool
    error: Optional[str] = None


class GroqClient:
    """Groq API Client for Streamlit (console.groq.com)."""
    
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.groq.com/openai/v1"
    
    def _call(self, messages: List[Dict], max_tokens: int = 1024, temperature: float = 0.7) -> GroqResponse:
        start = time.time()
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature
                },
                timeout=60
            )
            
            latency = (time.time() - start) * 1000
            
            if response.status_code != 200:
                return GroqResponse(
                    text="",
                    model=self.model,
                    usage={},
                    latency_ms=latency,
                    success=False,
                    error=f"API Error {response.status_code}: {response.text}"
                )
            
            data = response.json()
            
            return GroqResponse(
                text=data["choices"][0]["message"]["content"],
                model=data["model"],
                usage=data.get("usage", {}),
                latency_ms=latency,
                success=True
            )
            
        except Exception as e:
            return GroqResponse(
                text="",
                model=self.model,
                usage={},
                latency_ms=(time.time() - start) * 1000,
                success=False,
                error=str(e)
            )
    
    def translate(self, text: str, source: str, target: str) -> GroqResponse:
        messages = [
            {"role": "system", "content": "You are an expert multilingual translator. Translate accurately while preserving meaning, tone, and style. Output only the translation."},
            {"role": "user", "content": f"Translate from {source} to {target}:\n\n{text}"}
        ]
        return self._call(messages, temperature=0.3)
    
    def question_answering(self, question: str, context: str, language: str = "en") -> GroqResponse:
        messages = [
            {"role": "system", "content": f"You are a precise QA system. Extract the answer from the context. If not found, say 'unanswerable'. Answer in {language}."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"}
        ]
        return self._call(messages, temperature=0.1)
    
    def named_entity_recognition(self, text: str, entity_types: List[str] = None) -> GroqResponse:
        types = entity_types or ["PER (Person)", "LOC (Location)", "ORG (Organization)"]
        types_str = ", ".join(types)
        messages = [
            {"role": "system", "content": f"Extract named entities of types: {types_str}. Format as 'TYPE: entity' on separate lines. If none found, say 'No entities found'."},
            {"role": "user", "content": f"Extract entities from:\n\n{text}"}
        ]
        return self._call(messages, temperature=0.1)
    
    def natural_language_inference(self, premise: str, hypothesis: str) -> GroqResponse:
        messages = [
            {"role": "system", "content": "Classify the relationship between premise and hypothesis as exactly one of: ENTAILMENT, NEUTRAL, or CONTRADICTION. Explain your reasoning briefly."},
            {"role": "user", "content": f"Premise: {premise}\n\nHypothesis: {hypothesis}\n\nClassification:"}
        ]
        return self._call(messages, temperature=0.1)
    
    def paraphrase_detection(self, sentence1: str, sentence2: str) -> GroqResponse:
        messages = [
            {"role": "system", "content": "Determine if two sentences are paraphrases (same meaning). Answer with 'PARAPHRASE' or 'NOT PARAPHRASE' and explain why."},
            {"role": "user", "content": f"Sentence 1: {sentence1}\n\nSentence 2: {sentence2}\n\nAre these paraphrases?"}
        ]
        return self._call(messages, temperature=0.1)
    
    def summarize(self, text: str, max_length: int = 100) -> GroqResponse:
        messages = [
            {"role": "system", "content": f"Create a concise summary in {max_length} words or less. Be accurate and capture key points."},
            {"role": "user", "content": f"Summarize:\n\n{text}"}
        ]
        return self._call(messages, temperature=0.5)
    
    def evaluate_harsh(self, task_type: str, data: Dict) -> GroqResponse:
        prompt = f"""Evaluate this {task_type} with EXTREME strictness. Be harsh and critical.

{json.dumps(data, indent=2, ensure_ascii=False)}

Score each criterion 0-10 (10=perfect, be strict - rarely give above 8).
Provide:
1. Overall score
2. Detailed scores per criterion
3. Specific errors found
4. Harsh but constructive feedback
5. Suggestions for improvement"""

        messages = [
            {"role": "system", "content": "You are the world's harshest but fair critic. Find every flaw. Never give perfect scores unless truly flawless."},
            {"role": "user", "content": prompt}
        ]
        return self._call(messages, temperature=0.2, max_tokens=2048)
    
    def custom_prompt(self, prompt: str, system_prompt: str = None, temperature: float = 0.7) -> GroqResponse:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        return self._call(messages, temperature=temperature)


# =============================================================================
# Language Data
# =============================================================================

LANGUAGES = {
    "en": "🇬🇧 English",
    "es": "🇪🇸 Spanish",
    "fr": "🇫🇷 French",
    "de": "🇩🇪 German",
    "it": "🇮🇹 Italian",
    "pt": "🇵🇹 Portuguese",
    "ru": "🇷🇺 Russian",
    "zh": "🇨🇳 Chinese",
    "ja": "🇯🇵 Japanese",
    "ko": "🇰🇷 Korean",
    "ar": "🇸🇦 Arabic",
    "hi": "🇮🇳 Hindi",
    "tr": "🇹🇷 Turkish",
    "vi": "🇻🇳 Vietnamese",
    "th": "🇹🇭 Thai",
    "nl": "🇳🇱 Dutch",
    "pl": "🇵🇱 Polish",
    "uk": "🇺🇦 Ukrainian",
    "el": "🇬🇷 Greek",
    "he": "🇮🇱 Hebrew",
    "sw": "🇰🇪 Swahili",
    "bn": "🇧🇩 Bengali",
}


# =============================================================================
# Streamlit App
# =============================================================================

def main():
    # Header
    st.markdown('<h1 class="main-header">🌍 mT5 + Groq API</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">Multilingual NLP Tasks powered by Groq (Ultra-Fast LLMs)</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "🔑 Groq API Key",
            type="password",
            value=os.getenv("GROQ_API_KEY", ""),
            help="Get your API key from https://console.groq.com/"
        )
        
        if not api_key:
            st.warning("⚠️ Please enter your Groq API key")
            st.markdown("""
            **Get your API key:**
            1. Go to [console.groq.com](https://console.groq.com/)
            2. Sign in / Create account
            3. Go to API Keys and create one
            """)
        
        # Model selection
        model = st.selectbox(
            "🤖 Model",
            options=["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768", "gemma2-9b-it"],
            index=0
        )
        
        st.markdown("---")
        st.markdown("## 📊 Task Selection")
        
        task = st.radio(
            "Choose a task:",
            [
                "🌐 Translation",
                "❓ Question Answering",
                "🏷️ Named Entity Recognition",
                "🔍 Natural Language Inference",
                "🔄 Paraphrase Detection",
                "📝 Summarization",
                "⚖️ Harsh Evaluator",
                "💬 Custom Prompt"
            ]
        )
        
        st.markdown("---")
        st.markdown("### 📈 About")
        st.markdown("""
        This app uses **Groq API** for
        ultra-fast multilingual NLP tasks
        similar to **mT5 benchmarks**:
        - XQuAD, MLQA (QA)
        - XNLI (Inference)
        - WikiANN (NER)
        - PAWS-X (Paraphrase)
        """)
    
    # Main content area
    if not api_key:
        st.info("👈 Enter your Groq API key in the sidebar to get started")
        
        # Show demo
        st.markdown("### 🎭 Demo Preview")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("#### 🌐 Translation")
            st.code("Hello → Hola (ES)\nHello → 你好 (ZH)")
        with col2:
            st.markdown("#### ❓ QA")
            st.code("Q: Capital of France?\nA: Paris")
        with col3:
            st.markdown("#### 🏷️ NER")
            st.code("Elon Musk → PER\nSpaceX → ORG")
        return
    
    # Create client
    client = GroqClient(api_key, model)
    
    # Task UIs
    if "Translation" in task:
        render_translation_ui(client)
    elif "Question Answering" in task:
        render_qa_ui(client)
    elif "Named Entity" in task:
        render_ner_ui(client)
    elif "Natural Language Inference" in task:
        render_nli_ui(client)
    elif "Paraphrase" in task:
        render_paraphrase_ui(client)
    elif "Summarization" in task:
        render_summarization_ui(client)
    elif "Harsh Evaluator" in task:
        render_evaluator_ui(client)
    elif "Custom Prompt" in task:
        render_custom_ui(client)


def render_translation_ui(client: GroqClient):
    st.markdown("## 🌐 Translation")
    st.markdown("Translate text between 100+ languages")
    
    col1, col2 = st.columns(2)
    
    with col1:
        source_lang = st.selectbox("Source Language", list(LANGUAGES.keys()), 
                                   format_func=lambda x: LANGUAGES[x], index=0)
        source_text = st.text_area("Enter text to translate:", height=200,
                                   placeholder="Type or paste your text here...")
    
    with col2:
        target_lang = st.selectbox("Target Language", list(LANGUAGES.keys()),
                                   format_func=lambda x: LANGUAGES[x], index=1)
        
        if st.button("🚀 Translate", type="primary", use_container_width=True):
            if source_text:
                with st.spinner("Translating..."):
                    response = client.translate(source_text, source_lang, target_lang)
                
                if response.success:
                    st.text_area("Translation:", value=response.text, height=200)
                    st.caption(f"⏱️ {response.latency_ms:.0f}ms | 📊 {response.usage}")
                else:
                    st.error(f"Error: {response.error}")
            else:
                st.warning("Please enter text to translate")


def render_qa_ui(client: GroqClient):
    st.markdown("## ❓ Question Answering")
    st.markdown("XQuAD/MLQA style extractive QA")
    
    context = st.text_area(
        "📄 Context/Passage:",
        height=200,
        placeholder="Paste the context passage here...",
        value="The Amazon rainforest, also known as Amazonia, is a moist broadleaf tropical rainforest in the Amazon biome that covers most of the Amazon basin of South America. This basin encompasses 7,000,000 km², of which 5,500,000 km² are covered by the rainforest. The majority of the forest is contained within Brazil, with 60% of the rainforest."
    )
    
    question = st.text_input("❓ Question:", placeholder="What would you like to know?")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        language = st.selectbox("Answer in:", list(LANGUAGES.keys()),
                               format_func=lambda x: LANGUAGES[x], index=0)
    with col2:
        st.write("")  # Spacer
        st.write("")
        run = st.button("🔍 Find Answer", type="primary", use_container_width=True)
    
    if run:
        if context and question:
            with st.spinner("Finding answer..."):
                response = client.question_answering(question, context, LANGUAGES[language].split()[-1])
            
            if response.success:
                st.success(f"**Answer:** {response.text}")
                st.caption(f"⏱️ {response.latency_ms:.0f}ms")
            else:
                st.error(f"Error: {response.error}")
        else:
            st.warning("Please provide both context and question")


def render_ner_ui(client: GroqClient):
    st.markdown("## 🏷️ Named Entity Recognition")
    st.markdown("WikiANN style entity extraction")
    
    text = st.text_area(
        "Enter text:",
        height=150,
        placeholder="Enter text with named entities...",
        value="Elon Musk founded SpaceX in Hawthorne, California. The company launched Falcon 9 from Cape Canaveral."
    )
    
    entity_types = st.multiselect(
        "Entity types to extract:",
        ["PER (Person)", "LOC (Location)", "ORG (Organization)", "DATE", "EVENT", "PRODUCT"],
        default=["PER (Person)", "LOC (Location)", "ORG (Organization)"]
    )
    
    if st.button("🏷️ Extract Entities", type="primary"):
        if text:
            with st.spinner("Extracting entities..."):
                response = client.named_entity_recognition(text, entity_types)
            
            if response.success:
                st.markdown("### Extracted Entities:")
                st.code(response.text)
                st.caption(f"⏱️ {response.latency_ms:.0f}ms")
            else:
                st.error(f"Error: {response.error}")
        else:
            st.warning("Please enter text")


def render_nli_ui(client: GroqClient):
    st.markdown("## 🔍 Natural Language Inference")
    st.markdown("XNLI style textual entailment")
    
    premise = st.text_area(
        "📝 Premise:",
        height=100,
        placeholder="Enter the premise statement...",
        value="A man is playing a guitar on stage."
    )
    
    hypothesis = st.text_area(
        "💭 Hypothesis:",
        height=100,
        placeholder="Enter the hypothesis to evaluate...",
        value="Someone is making music."
    )
    
    if st.button("🔍 Classify Relationship", type="primary"):
        if premise and hypothesis:
            with st.spinner("Analyzing..."):
                response = client.natural_language_inference(premise, hypothesis)
            
            if response.success:
                # Parse result
                result_text = response.text.upper()
                if "ENTAILMENT" in result_text:
                    st.success("✅ **ENTAILMENT** - Hypothesis follows from premise")
                elif "CONTRADICTION" in result_text:
                    st.error("❌ **CONTRADICTION** - Hypothesis contradicts premise")
                else:
                    st.info("➖ **NEUTRAL** - Neither entailment nor contradiction")
                
                st.markdown("**Explanation:**")
                st.write(response.text)
                st.caption(f"⏱️ {response.latency_ms:.0f}ms")
            else:
                st.error(f"Error: {response.error}")
        else:
            st.warning("Please provide both premise and hypothesis")


def render_paraphrase_ui(client: GroqClient):
    st.markdown("## 🔄 Paraphrase Detection")
    st.markdown("PAWS-X style paraphrase identification")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sentence1 = st.text_area(
            "Sentence 1:",
            height=120,
            value="The cat is sitting on the mat."
        )
    
    with col2:
        sentence2 = st.text_area(
            "Sentence 2:",
            height=120,
            value="A cat can be seen on the mat."
        )
    
    if st.button("🔄 Check Paraphrase", type="primary", use_container_width=True):
        if sentence1 and sentence2:
            with st.spinner("Analyzing..."):
                response = client.paraphrase_detection(sentence1, sentence2)
            
            if response.success:
                if "NOT PARAPHRASE" in response.text.upper():
                    st.warning("❌ **NOT PARAPHRASE** - Different meanings")
                else:
                    st.success("✅ **PARAPHRASE** - Same meaning")
                
                st.markdown("**Analysis:**")
                st.write(response.text)
                st.caption(f"⏱️ {response.latency_ms:.0f}ms")
            else:
                st.error(f"Error: {response.error}")
        else:
            st.warning("Please enter both sentences")


def render_summarization_ui(client: GroqClient):
    st.markdown("## 📝 Summarization")
    st.markdown("XSum/GEM style text summarization")
    
    text = st.text_area(
        "Text to summarize:",
        height=250,
        placeholder="Paste a long article or document...",
        value="""The Amazon rainforest, also known as Amazonia, is a moist broadleaf tropical rainforest in the Amazon biome that covers most of the Amazon basin of South America. This basin encompasses 7,000,000 km² (2,700,000 sq mi), of which 5,500,000 km² (2,100,000 sq mi) are covered by the rainforest. This region includes territory belonging to nine nations and 3,344 formally acknowledged indigenous territories. The majority of the forest is contained within Brazil, with 60% of the rainforest, followed by Peru with 13%, Colombia with 10%, and with minor amounts in Bolivia, Ecuador, French Guiana, Guyana, Suriname, and Venezuela."""
    )
    
    max_length = st.slider("Maximum summary length (words):", 20, 200, 50)
    
    if st.button("📝 Summarize", type="primary"):
        if text:
            with st.spinner("Summarizing..."):
                response = client.summarize(text, max_length)
            
            if response.success:
                st.success("**Summary:**")
                st.write(response.text)
                
                # Stats
                original_words = len(text.split())
                summary_words = len(response.text.split())
                compression = (1 - summary_words / original_words) * 100
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Original", f"{original_words} words")
                col2.metric("Summary", f"{summary_words} words")
                col3.metric("Compression", f"{compression:.0f}%")
                
                st.caption(f"⏱️ {response.latency_ms:.0f}ms")
            else:
                st.error(f"Error: {response.error}")
        else:
            st.warning("Please enter text to summarize")


def render_evaluator_ui(client: GroqClient):
    st.markdown("## ⚖️ Harsh Evaluator")
    st.markdown("**Extremely strict** evaluation of NLP outputs")
    
    st.warning("🔥 This evaluator is intentionally harsh and critical!")
    
    eval_type = st.selectbox(
        "What to evaluate:",
        ["Translation", "Question Answer", "Summary", "Named Entities"]
    )
    
    if eval_type == "Translation":
        col1, col2 = st.columns(2)
        with col1:
            source = st.text_area("Source text:", height=120)
            source_lang = st.selectbox("Source lang:", list(LANGUAGES.keys()),
                                       format_func=lambda x: LANGUAGES[x])
        with col2:
            translation = st.text_area("Translation to evaluate:", height=120)
            target_lang = st.selectbox("Target lang:", list(LANGUAGES.keys()),
                                       format_func=lambda x: LANGUAGES[x], index=1)
        
        reference = st.text_input("Reference translation (optional):")
        
        if st.button("⚖️ Evaluate Harshly", type="primary"):
            if source and translation:
                data = {
                    "source_text": source,
                    "translation": translation,
                    "source_language": LANGUAGES[source_lang],
                    "target_language": LANGUAGES[target_lang],
                    "reference": reference if reference else "Not provided"
                }
                
                with st.spinner("Evaluating harshly..."):
                    response = client.evaluate_harsh("translation", data)
                
                if response.success:
                    st.markdown("### 📊 Harsh Evaluation Results")
                    st.markdown(response.text)
                    st.caption(f"⏱️ {response.latency_ms:.0f}ms")
                else:
                    st.error(f"Error: {response.error}")
    
    elif eval_type == "Question Answer":
        context = st.text_area("Context:", height=100)
        question = st.text_input("Question:")
        answer = st.text_input("Answer to evaluate:")
        gold = st.text_input("Gold answer (optional):")
        
        if st.button("⚖️ Evaluate Harshly", type="primary"):
            if context and question and answer:
                data = {
                    "context": context,
                    "question": question,
                    "predicted_answer": answer,
                    "gold_answer": gold if gold else "Not provided"
                }
                
                with st.spinner("Evaluating harshly..."):
                    response = client.evaluate_harsh("question answering", data)
                
                if response.success:
                    st.markdown("### 📊 Harsh Evaluation Results")
                    st.markdown(response.text)
                else:
                    st.error(f"Error: {response.error}")
    
    elif eval_type == "Summary":
        original = st.text_area("Original text:", height=150)
        summary = st.text_area("Summary to evaluate:", height=100)
        
        if st.button("⚖️ Evaluate Harshly", type="primary"):
            if original and summary:
                data = {"original_text": original, "summary": summary}
                
                with st.spinner("Evaluating harshly..."):
                    response = client.evaluate_harsh("summarization", data)
                
                if response.success:
                    st.markdown("### 📊 Harsh Evaluation Results")
                    st.markdown(response.text)
                else:
                    st.error(f"Error: {response.error}")
    
    elif eval_type == "Named Entities":
        text = st.text_area("Original text:", height=100)
        entities = st.text_input("Extracted entities (TYPE: entity format):")
        gold_entities = st.text_input("Gold entities (optional):")
        
        if st.button("⚖️ Evaluate Harshly", type="primary"):
            if text and entities:
                data = {
                    "text": text,
                    "predicted_entities": entities,
                    "gold_entities": gold_entities if gold_entities else "Not provided"
                }
                
                with st.spinner("Evaluating harshly..."):
                    response = client.evaluate_harsh("NER", data)
                
                if response.success:
                    st.markdown("### 📊 Harsh Evaluation Results")
                    st.markdown(response.text)
                else:
                    st.error(f"Error: {response.error}")


def render_custom_ui(client: GroqClient):
    st.markdown("## 💬 Custom Prompt")
    st.markdown("Send any prompt to Grok")
    
    system_prompt = st.text_area(
        "System prompt (optional):",
        height=80,
        placeholder="e.g., 'You are a helpful assistant specialized in...'",
        value=""
    )
    
    user_prompt = st.text_area(
        "Your prompt:",
        height=200,
        placeholder="Enter your prompt here..."
    )
    
    col1, col2 = st.columns(2)
    with col1:
        temperature = st.slider("Temperature:", 0.0, 1.0, 0.7, 0.1)
    with col2:
        st.write("")
        st.write("")
        run = st.button("🚀 Send", type="primary", use_container_width=True)
    
    if run:
        if user_prompt:
            with st.spinner("Generating..."):
                response = client.custom_prompt(
                    user_prompt,
                    system_prompt if system_prompt else None,
                    temperature
                )
            
            if response.success:
                st.markdown("### Response:")
                st.write(response.text)
                st.caption(f"⏱️ {response.latency_ms:.0f}ms | 📊 {response.usage}")
            else:
                st.error(f"Error: {response.error}")
        else:
            st.warning("Please enter a prompt")


if __name__ == "__main__":
    main()
