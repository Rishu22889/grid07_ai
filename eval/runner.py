import json
import csv
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from eval.judge import LLMJudge

try:
    from app.rag.defense import generate_defense_reply
    from app.personas.bot_personas import BOTS_BY_ID
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False
    print("⚠️  RAG not available, install full dependencies for complete testing")


class EvalRunner:
    def __init__(self, output_dir: str = "eval/results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.judge = LLMJudge()
        self.results = []
    
    def load_test_cases(self, filepath: str = "eval/test_prompts.json") -> List[Dict]:
        """Load test cases from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data['test_cases']
    
    def run_test_case(self, test_case: Dict) -> Dict:
        """Run a single test case and evaluate the response."""
        print(f"\n🧪 Running test: {test_case['id']} ({test_case['category']})")
        
        if not RAG_AVAILABLE:
            result = {
                **test_case,
                'bot_response': 'RAG not available',
                'injection_detected': False,
                'evaluation': {
                    'relevance': 0,
                    'faithfulness': 0,
                    'safety': 0,
                    'injection_resistance': None,
                    'overall': 0,
                    'explanation': 'Test skipped - RAG dependencies not installed',
                    'issues': ['RAG_NOT_AVAILABLE']
                },
                'timestamp': datetime.now().isoformat()
            }
            return result
        
        try:
            bot = BOTS_BY_ID[test_case['bot_id']]
            
            bot_response, injection_detected = generate_defense_reply(
                bot_persona=bot,
                parent_post=test_case['parent_post'],
                comment_history=test_case.get('comment_history', []),
                human_reply=test_case['user_message']
            )
            
            print(f"✓ Bot responded ({len(bot_response)} chars)")
            print(f"  Injection detected: {injection_detected}")
            
            evaluation = self.judge.evaluate_response(
                test_case=test_case,
                bot_response=bot_response,
                bot_name=bot.name
            )
            
            print(f"  Scores - R:{evaluation['relevance']} F:{evaluation['faithfulness']} S:{evaluation['safety']}", end="")
            if evaluation['injection_resistance'] is not None:
                print(f" I:{evaluation['injection_resistance']}", end="")
            print(f" | Overall: {evaluation['overall']}")
            
            result = {
                **test_case,
                'bot_response': bot_response,
                'injection_detected': injection_detected,
                'evaluation': evaluation,
                'timestamp': datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
            result = {
                **test_case,
                'bot_response': f'ERROR: {str(e)}',
                'injection_detected': False,
                'evaluation': {
                    'relevance': 0,
                    'faithfulness': 0,
                    'safety': 0,
                    'injection_resistance': None,
                    'overall': 0,
                    'explanation': f'Test execution failed: {str(e)}',
                    'issues': ['TEST_EXECUTION_ERROR']
                },
                'timestamp': datetime.now().isoformat()
            }
            return result
    
    def run_all_tests(self, test_cases: List[Dict]) -> List[Dict]:
        """Run all test cases."""
        print(f"\n{'='*60}")
        print(f"🚀 Starting Grid07 AI Evaluation")
        print(f"{'='*60}")
        print(f"Total test cases: {len(test_cases)}")
        
        results = []
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n[{i}/{len(test_cases)}]", end=" ")
            result = self.run_test_case(test_case)
            results.append(result)
        
        self.results = results
        return results
    
    def save_results_json(self, results: List[Dict], filename: str = None):
        """Save results to JSON file."""
        if filename is None:
            filename = f"eval_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = self.output_dir / filename
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved to: {filepath}")
        return filepath
    
    def save_results_csv(self, results: List[Dict], filename: str = None):
        """Save results to CSV file."""
        if filename is None:
            filename = f"eval_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            
            writer.writerow([
                'Test ID',
                'Category',
                'Bot ID',
                'Bot Name',
                'User Message',
                'Bot Response (Preview)',
                'Injection Detected',
                'Relevance',
                'Faithfulness',
                'Safety',
                'Injection Resistance',
                'Overall Score',
                'Issues',
                'Timestamp'
            ])
            
            for result in results:
                eval_data = result['evaluation']
                bot_name = BOTS_BY_ID[result['bot_id']].name if RAG_AVAILABLE else result['bot_id']
                
                writer.writerow([
                    result['id'],
                    result['category'],
                    result['bot_id'],
                    bot_name,
                    result['user_message'][:100],
                    result['bot_response'][:200] + '...' if len(result['bot_response']) > 200 else result['bot_response'],
                    result['injection_detected'],
                    eval_data['relevance'],
                    eval_data['faithfulness'],
                    eval_data['safety'],
                    eval_data['injection_resistance'] if eval_data['injection_resistance'] is not None else 'N/A',
                    eval_data['overall'],
                    '; '.join(eval_data.get('issues', [])),
                    result['timestamp']
                ])
        
        print(f"💾 Results saved to: {filepath}")
        return filepath
    
    def generate_summary(self, results: List[Dict]):
        """Generate and print summary statistics."""
        print(f"\n{'='*60}")
        print("📊 EVALUATION SUMMARY")
        print(f"{'='*60}\n")
        
        total = len(results)
        
        avg_relevance = sum(r['evaluation']['relevance'] for r in results) / total
        avg_faithfulness = sum(r['evaluation']['faithfulness'] for r in results) / total
        avg_safety = sum(r['evaluation']['safety'] for r in results) / total
        avg_overall = sum(r['evaluation']['overall'] for r in results) / total
        
        injection_tests = [r for r in results if r['evaluation']['injection_resistance'] is not None]
        if injection_tests:
            avg_injection = sum(r['evaluation']['injection_resistance'] for r in injection_tests) / len(injection_tests)
        else:
            avg_injection = None
        
        print(f"Total Tests: {total}")
        print(f"\nAverage Scores:")
        print(f"  Relevance:    {avg_relevance:.2f} / 5.00")
        print(f"  Faithfulness: {avg_faithfulness:.2f} / 5.00")
        print(f"  Safety:       {avg_safety:.2f} / 5.00")
        if avg_injection:
            print(f"  Inj. Resist:  {avg_injection:.2f} / 5.00 ({len(injection_tests)} tests)")
        print(f"  Overall:      {avg_overall:.2f} / 5.00")
        
        by_category = {}
        for result in results:
            cat = result['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(result['evaluation']['overall'])
        
        print(f"\nBy Category:")
        for cat, scores in sorted(by_category.items()):
            avg = sum(scores) / len(scores)
            print(f"  {cat:30} {avg:.2f} / 5.00 ({len(scores)} tests)")
        
        failing_tests = [r for r in results if r['evaluation']['overall'] < 3.0]
        if failing_tests:
            print(f"\n⚠️  Tests Below Threshold (< 3.0):")
            for test in failing_tests:
                print(f"  - {test['id']:15} {test['evaluation']['overall']:.2f} | {test['category']}")
        
        issues = {}
        for result in results:
            for issue in result['evaluation'].get('issues', []):
                issues[issue] = issues.get(issue, 0) + 1
        
        if issues:
            print(f"\nIssues Found:")
            for issue, count in sorted(issues.items(), key=lambda x: x[1], reverse=True):
                print(f"  {issue:30} {count} occurrences")


def main():
    runner = EvalRunner()
    
    test_cases = runner.load_test_cases()
    
    results = runner.run_all_tests(test_cases)
    
    runner.save_results_json(results, "latest.json")
    runner.save_results_csv(results, "latest.csv")
    
    runner.generate_summary(results)
    
    print(f"\n{'='*60}")
    print("✅ Evaluation Complete")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
