"""
Grid07 AI - LLM-as-Judge Evaluation Harness

Automated evaluation system for assessing RAG pipeline performance
across multiple dimensions: relevance, faithfulness, safety, and
prompt injection resistance.

Usage:
    python -m eval.runner      # Run all evaluations
    python -m eval.dashboard   # Generate HTML dashboard
"""

from .judge import LLMJudge
from .runner import EvalRunner

__all__ = ['LLMJudge', 'EvalRunner']
