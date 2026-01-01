# Grok API Integration Examples for mT5
# ======================================
# This script demonstrates how to use the Grok API client with mT5 tasks.
#
# SETUP:
# 1. Set your Grok API key:
#    - Windows: set GROK_API_KEY=your-api-key-here
#    - Linux/Mac: export GROK_API_KEY=your-api-key-here
#
# 2. Install requirements:
#    pip install requests
#
# 3. Run this script:
#    python examples/grok_examples.py

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multilingual_t5.grok_client import (
    GrokClient, GrokConfig, GrokModel, 
    create_client, quick_translate, quick_qa
)
from multilingual_t5.grok_evaluator import (
    EvaluationRunner, EvaluationConfig, TaskType
)


def example_translation():
    """Example: Translate text between languages."""
    print("\n" + "="*60)
    print("📝 TRANSLATION EXAMPLE")
    print("="*60)
    
    client = create_client()
    
    # English to Spanish
    response = client.translate(
        text="The quick brown fox jumps over the lazy dog.",
        source_lang="en",
        target_lang="es"
    )
    print(f"EN → ES: {response.text}")
    
    # English to Chinese
    response = client.translate(
        text="Machine learning is transforming the world.",
        source_lang="en",
        target_lang="zh"
    )
    print(f"EN → ZH: {response.text}")
    
    # Spanish to German
    response = client.translate(
        text="Buenos días, ¿cómo estás?",
        source_lang="es",
        target_lang="de"
    )
    print(f"ES → DE: {response.text}")


def example_question_answering():
    """Example: XQuAD/MLQA style question answering."""
    print("\n" + "="*60)
    print("❓ QUESTION ANSWERING EXAMPLE")
    print("="*60)
    
    client = create_client()
    
    context = """
    The Amazon rainforest, also known as Amazonia, is a moist broadleaf 
    tropical rainforest in the Amazon biome that covers most of the Amazon 
    basin of South America. This basin encompasses 7,000,000 km² (2,700,000 sq mi), 
    of which 5,500,000 km² (2,100,000 sq mi) are covered by the rainforest. 
    This region includes territory belonging to nine nations and 3,344 formally 
    acknowledged indigenous territories.
    """
    
    questions = [
        "What is the Amazon rainforest also known as?",
        "How large is the Amazon basin?",
        "How many nations have territory in this region?"
    ]
    
    for q in questions:
        response = client.question_answering(question=q, context=context)
        print(f"Q: {q}")
        print(f"A: {response.text}\n")


def example_nli():
    """Example: XNLI style natural language inference."""
    print("\n" + "="*60)
    print("🔍 NATURAL LANGUAGE INFERENCE EXAMPLE")
    print("="*60)
    
    client = create_client()
    
    examples = [
        ("A man is playing a guitar.", "Someone is making music.", "entailment"),
        ("The cat sat on the mat.", "The dog ran in the park.", "neutral"),
        ("It is raining outside.", "The weather is sunny and clear.", "contradiction"),
    ]
    
    for premise, hypothesis, expected in examples:
        response = client.natural_language_inference(premise, hypothesis)
        print(f"Premise: {premise}")
        print(f"Hypothesis: {hypothesis}")
        print(f"Predicted: {response.text} (Expected: {expected})\n")


def example_ner():
    """Example: WikiANN style named entity recognition."""
    print("\n" + "="*60)
    print("🏷️ NAMED ENTITY RECOGNITION EXAMPLE")
    print("="*60)
    
    client = create_client()
    
    texts = [
        "Elon Musk founded SpaceX in Hawthorne, California.",
        "Marie Curie won the Nobel Prize in Paris.",
        "Barack Obama visited the United Nations headquarters in New York."
    ]
    
    for text in texts:
        response = client.named_entity_recognition(text)
        print(f"Text: {text}")
        print(f"Entities: {response.text}\n")


def example_paraphrase_detection():
    """Example: PAWS-X style paraphrase detection."""
    print("\n" + "="*60)
    print("🔄 PARAPHRASE DETECTION EXAMPLE")
    print("="*60)
    
    client = create_client()
    
    pairs = [
        ("The cat is on the mat.", "The mat has a cat on it.", True),
        ("He went to the store.", "She stayed at home.", False),
        ("The movie was excellent.", "The film was outstanding.", True),
    ]
    
    for sent1, sent2, expected in pairs:
        response = client.paraphrase_detection(sent1, sent2)
        print(f"S1: {sent1}")
        print(f"S2: {sent2}")
        print(f"Result: {response.text} (Expected: {'paraphrase' if expected else 'not paraphrase'})\n")


def example_harsh_evaluation():
    """Example: Harsh evaluation of model outputs."""
    print("\n" + "="*60)
    print("⚖️ HARSH EVALUATION EXAMPLE")
    print("="*60)
    
    client = create_client()
    
    # Evaluate a translation (intentionally imperfect)
    result = client.evaluate_translation(
        source_text="The meeting will be held tomorrow at 3 PM.",
        translation="La reunión se llevará a cabo mañana a las 3 de la tarde.",
        source_lang="en",
        target_lang="es"
    )
    
    print("Translation Evaluation:")
    print(f"  Overall Score: {result.score:.2%}")
    print(f"  Metrics: {result.metrics}")
    print(f"  Feedback: {result.feedback[:200]}..." if len(result.feedback) > 200 else f"  Feedback: {result.feedback}")
    print(f"  Is Correct: {result.is_correct}")
    
    # Evaluate a QA answer
    result = client.evaluate_qa_answer(
        question="What is the capital of France?",
        context="France is a country in Western Europe. Its capital city is Paris, which is also the largest city in France.",
        predicted_answer="Paris",
        gold_answer="Paris"
    )
    
    print("\nQA Evaluation:")
    print(f"  Overall Score: {result.score:.2%}")
    print(f"  Is Correct: {result.is_correct}")


def example_batch_evaluation():
    """Example: Batch evaluation with report generation."""
    print("\n" + "="*60)
    print("📊 BATCH EVALUATION EXAMPLE")
    print("="*60)
    
    runner = EvaluationRunner()
    
    # Sample QA predictions
    predictions = [
        {
            "question": "What is the capital of France?",
            "context": "France is a country in Europe. Paris is its capital.",
            "predicted_answer": "Paris",
            "language": "en"
        },
        {
            "question": "What color is the sky?",
            "context": "On a clear day, the sky appears blue due to Rayleigh scattering.",
            "predicted_answer": "blue",
            "language": "en"
        },
        {
            "question": "Who wrote Romeo and Juliet?",
            "context": "Romeo and Juliet is a tragedy written by William Shakespeare around 1594-1596.",
            "predicted_answer": "Shakespeare",
            "language": "en"
        }
    ]
    
    gold_answers = ["Paris", "blue", "William Shakespeare"]
    
    report = runner.evaluate_qa(
        predictions=predictions,
        gold_answers=gold_answers
    )
    
    report.print_summary()


def example_custom_config():
    """Example: Using custom configuration."""
    print("\n" + "="*60)
    print("⚙️ CUSTOM CONFIGURATION EXAMPLE")
    print("="*60)
    
    # Create client with custom config
    config = GrokConfig(
        model=GrokModel.GROK_2,
        max_tokens=512,
        temperature=0.5,
        max_retries=5,
        timeout=120
    )
    
    client = GrokClient(config)
    
    response = client.generate(
        prompt="Write a haiku about programming",
        system_prompt="You are a creative poet who loves technology."
    )
    
    print(f"Generated:\n{response.text}")
    print(f"\nMetadata:")
    print(f"  Model: {response.model}")
    print(f"  Latency: {response.latency_ms:.0f}ms")
    print(f"  Tokens: {response.usage}")


def main():
    """Run all examples."""
    print("\n" + "🚀 GROK API + mT5 INTEGRATION EXAMPLES 🚀")
    print("=" * 60)
    
    # Check for API key
    if not os.getenv("GROK_API_KEY"):
        print("\n⚠️  WARNING: GROK_API_KEY environment variable not set!")
        print("Set it using:")
        print("  Windows: set GROK_API_KEY=your-api-key")
        print("  Linux/Mac: export GROK_API_KEY=your-api-key")
        print("\nGet your API key from: https://x.ai/")
        return
    
    try:
        example_translation()
        example_question_answering()
        example_nli()
        example_ner()
        example_paraphrase_detection()
        example_harsh_evaluation()
        example_batch_evaluation()
        example_custom_config()
        
        print("\n" + "="*60)
        print("✅ All examples completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise


if __name__ == "__main__":
    main()
