#!/bin/bash

echo "🧪 Grid07 AI - LLM-as-Judge Evaluation Harness"
echo "=============================================="
echo ""

if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found"
    echo "Please create .env with GROQ_API_KEY"
    exit 1
fi

echo "📋 Running evaluation tests..."
python -m eval.runner

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Evaluation failed"
    exit 1
fi

echo ""
echo "📊 Generating dashboard..."
python -m eval.dashboard

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Dashboard generation failed"
    exit 1
fi

echo ""
echo "✅ Evaluation complete!"
echo ""
echo "📂 Results saved to:"
echo "   - eval/results/latest.json"
echo "   - eval/results/latest.csv"
echo "   - eval/results/dashboard.html"
echo ""
echo "🌐 Open dashboard with:"
echo "   open eval/results/dashboard.html"
echo ""
