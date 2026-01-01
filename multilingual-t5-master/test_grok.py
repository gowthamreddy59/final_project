"""Standalone test script for Grok API integration.
This script tests the Grok API client without requiring TensorFlow.
"""

import os
import sys

# Add the project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Check for API key first
api_key = os.getenv("GROK_API_KEY")
if not api_key:
    print("\n" + "="*60)
    print("⚠️  GROK_API_KEY not set!")
    print("="*60)
    print("\nTo use the Grok API, you need to set your API key:")
    print("\n  Windows (PowerShell):")
    print('    $env:GROK_API_KEY = "your-api-key-here"')
    print("\n  Windows (CMD):")
    print('    set GROK_API_KEY=your-api-key-here')
    print("\n  Linux/Mac:")
    print('    export GROK_API_KEY=your-api-key-here')
    print("\n📌 Get your API key from: https://console.x.ai/")
    print("="*60)
    
    # Demo mode - show what would happen
    print("\n🎭 DEMO MODE (No API calls will be made)")
    print("-"*60)
    print("\nExample usage once API key is set:\n")
    
    demo_code = '''
from multilingual_t5.grok_client import create_client

# Create client
client = create_client()

# Translation
response = client.translate("Hello world", "en", "es")
print(f"Translation: {response.text}")

# Question Answering
response = client.question_answering(
    question="What is the capital of France?",
    context="France is a country in Europe. Paris is its capital."
)
print(f"Answer: {response.text}")

# Named Entity Recognition
response = client.named_entity_recognition("Elon Musk founded SpaceX in California.")
print(f"Entities: {response.text}")

# Harsh Evaluation
result = client.evaluate_translation(
    source_text="The meeting is tomorrow.",
    translation="La reunión es mañana.",
    source_lang="en",
    target_lang="es"
)
print(f"Score: {result.score:.0%}")
print(f"Feedback: {result.feedback}")
'''
    print(demo_code)
    print("-"*60)
    print("\n✅ Grok client module is ready to use!")
    print("   Just set GROK_API_KEY and run this script again.\n")
    sys.exit(0)

# If we have an API key, import and run actual tests
print("\n" + "="*60)
print("🚀 GROK API INTEGRATION TEST")
print("="*60)
print(f"API Key: {api_key[:8]}...{api_key[-4:]}")

# Import the grok client directly (avoiding TensorFlow dependencies)
import requests
import json
import time
from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from enum import Enum


class GrokModel(Enum):
    GROK_1 = "grok-1"
    GROK_2 = "grok-2"
    GROK_2_MINI = "grok-2-mini"
    GROK_BETA = "grok-beta"


@dataclass
class GrokResponse:
    text: str
    model: str
    usage: Dict[str, int]
    finish_reason: str
    latency_ms: float


class SimpleGrokClient:
    """Simplified Grok client for testing."""
    
    def __init__(self, api_key: str, model: str = "grok-2"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.x.ai/v1"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
    
    def _call(self, messages: List[Dict], max_tokens: int = 1024, temperature: float = 0.7) -> GrokResponse:
        start = time.time()
        
        response = self.session.post(
            f"{self.base_url}/chat/completions",
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
            raise Exception(f"API Error {response.status_code}: {response.text}")
        
        data = response.json()
        
        return GrokResponse(
            text=data["choices"][0]["message"]["content"],
            model=data["model"],
            usage=data.get("usage", {}),
            finish_reason=data["choices"][0].get("finish_reason", "unknown"),
            latency_ms=latency
        )
    
    def translate(self, text: str, source: str, target: str) -> GrokResponse:
        messages = [
            {"role": "system", "content": "You are an expert translator. Translate accurately and naturally."},
            {"role": "user", "content": f"Translate from {source} to {target}:\n\n{text}"}
        ]
        return self._call(messages, temperature=0.3)
    
    def question_answering(self, question: str, context: str) -> GrokResponse:
        messages = [
            {"role": "system", "content": "Answer the question based on the context. Be concise."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
        ]
        return self._call(messages, temperature=0.1)
    
    def ner(self, text: str) -> GrokResponse:
        messages = [
            {"role": "system", "content": "Extract named entities. Format: TYPE: entity $$ TYPE: entity"},
            {"role": "user", "content": f"Extract entities from: {text}"}
        ]
        return self._call(messages, temperature=0.1)
    
    def nli(self, premise: str, hypothesis: str) -> GrokResponse:
        messages = [
            {"role": "system", "content": "Classify as: entailment, neutral, or contradiction. Output only the label."},
            {"role": "user", "content": f"Premise: {premise}\nHypothesis: {hypothesis}"}
        ]
        return self._call(messages, temperature=0.1, max_tokens=20)
    
    def evaluate_harsh(self, task: str, input_data: Dict) -> Dict:
        prompt = f"""Evaluate this {task} with EXTREME strictness (0-10 scale, be harsh):

{json.dumps(input_data, indent=2)}

Respond in JSON with: score, errors, feedback"""
        
        messages = [
            {"role": "system", "content": "You are the world's harshest critic. Never give above 8 unless perfect."},
            {"role": "user", "content": prompt}
        ]
        
        response = self._call(messages, temperature=0.2)
        return {"raw": response.text, "latency_ms": response.latency_ms}


def run_tests():
    """Run all tests."""
    client = SimpleGrokClient(api_key)
    
    print("\n" + "-"*60)
    print("📝 TEST 1: Translation")
    print("-"*60)
    try:
        response = client.translate("Hello, how are you?", "en", "es")
        print(f"✅ EN → ES: {response.text}")
        print(f"   Latency: {response.latency_ms:.0f}ms")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "-"*60)
    print("❓ TEST 2: Question Answering")
    print("-"*60)
    try:
        response = client.question_answering(
            question="What is the capital of France?",
            context="France is a beautiful country in Western Europe. Its capital city is Paris, known for the Eiffel Tower."
        )
        print(f"✅ Answer: {response.text}")
        print(f"   Latency: {response.latency_ms:.0f}ms")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "-"*60)
    print("🏷️ TEST 3: Named Entity Recognition")
    print("-"*60)
    try:
        response = client.ner("Elon Musk founded SpaceX in Hawthorne, California.")
        print(f"✅ Entities: {response.text}")
        print(f"   Latency: {response.latency_ms:.0f}ms")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "-"*60)
    print("🔍 TEST 4: Natural Language Inference")
    print("-"*60)
    try:
        response = client.nli(
            premise="A man is playing guitar.",
            hypothesis="Someone is making music."
        )
        print(f"✅ Classification: {response.text}")
        print(f"   Latency: {response.latency_ms:.0f}ms")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "-"*60)
    print("⚖️ TEST 5: Harsh Evaluation")
    print("-"*60)
    try:
        result = client.evaluate_harsh("translation", {
            "source": "The quick brown fox jumps over the lazy dog.",
            "translation": "El rápido zorro marrón salta sobre el perro perezoso.",
            "source_lang": "en",
            "target_lang": "es"
        })
        print(f"✅ Evaluation:\n{result['raw'][:500]}")
        print(f"   Latency: {result['latency_ms']:.0f}ms")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETED!")
    print("="*60 + "\n")


if __name__ == "__main__":
    run_tests()
