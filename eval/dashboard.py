import json
from pathlib import Path
from datetime import datetime


def generate_dashboard(results_file: str = "eval/results/latest.json", output_file: str = "eval/results/dashboard.html"):
    """Generate an HTML dashboard from evaluation results."""
    
    with open(results_file, 'r') as f:
        results = json.load(f)
    
    total = len(results)
    avg_relevance = sum(r['evaluation']['relevance'] for r in results) / total
    avg_faithfulness = sum(r['evaluation']['faithfulness'] for r in results) / total
    avg_safety = sum(r['evaluation']['safety'] for r in results) / total
    avg_overall = sum(r['evaluation']['overall'] for r in results) / total
    
    injection_tests = [r for r in results if r['evaluation']['injection_resistance'] is not None]
    avg_injection = sum(r['evaluation']['injection_resistance'] for r in injection_tests) / len(injection_tests) if injection_tests else 0
    
    by_category = {}
    for result in results:
        cat = result['category']
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(result)
    
    failing_tests = [r for r in results if r['evaluation']['overall'] < 3.0]
    passing_tests = [r for r in results if r['evaluation']['overall'] >= 4.0]
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grid07 AI - Evaluation Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #e0e0e0;
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        header {{
            text-align: center;
            padding: 40px 0;
            border-bottom: 2px solid #0f3460;
            margin-bottom: 40px;
        }}
        
        h1 {{
            font-size: 2.5em;
            background: linear-gradient(90deg, #00d9ff, #7b2ff7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            color: #a0a0a0;
            font-size: 1.1em;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .metric-card {{
            background: rgba(15, 52, 96, 0.3);
            border: 1px solid #0f3460;
            border-radius: 12px;
            padding: 25px;
            text-align: center;
            transition: transform 0.2s;
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
            border-color: #00d9ff;
        }}
        
        .metric-label {{
            font-size: 0.9em;
            color: #a0a0a0;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }}
        
        .metric-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #00d9ff;
        }}
        
        .metric-max {{
            font-size: 1.2em;
            color: #666;
        }}
        
        .score-bar {{
            width: 100%;
            height: 8px;
            background: #222;
            border-radius: 4px;
            margin-top: 10px;
            overflow: hidden;
        }}
        
        .score-fill {{
            height: 100%;
            background: linear-gradient(90deg, #7b2ff7, #00d9ff);
            transition: width 0.5s ease;
        }}
        
        .section {{
            background: rgba(15, 52, 96, 0.2);
            border: 1px solid #0f3460;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
        }}
        
        .section-title {{
            font-size: 1.8em;
            margin-bottom: 20px;
            color: #00d9ff;
        }}
        
        .category-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
        }}
        
        .category-item {{
            background: rgba(0, 0, 0, 0.3);
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #7b2ff7;
        }}
        
        .category-name {{
            font-weight: bold;
            color: #fff;
            margin-bottom: 8px;
        }}
        
        .category-stats {{
            display: flex;
            justify-content: space-between;
            color: #a0a0a0;
            font-size: 0.9em;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        
        th {{
            background: rgba(0, 0, 0, 0.4);
            padding: 12px;
            text-align: left;
            color: #00d9ff;
            font-weight: 600;
            border-bottom: 2px solid #0f3460;
        }}
        
        td {{
            padding: 12px;
            border-bottom: 1px solid #0f3460;
        }}
        
        tr:hover {{
            background: rgba(0, 217, 255, 0.05);
        }}
        
        .score {{
            font-weight: bold;
            padding: 4px 8px;
            border-radius: 4px;
        }}
        
        .score-high {{
            background: rgba(0, 255, 100, 0.2);
            color: #00ff64;
        }}
        
        .score-medium {{
            background: rgba(255, 200, 0, 0.2);
            color: #ffc800;
        }}
        
        .score-low {{
            background: rgba(255, 50, 50, 0.2);
            color: #ff3232;
        }}
        
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        
        .badge-pass {{
            background: rgba(0, 255, 100, 0.2);
            color: #00ff64;
        }}
        
        .badge-fail {{
            background: rgba(255, 50, 50, 0.2);
            color: #ff3232;
        }}
        
        .badge-warning {{
            background: rgba(255, 200, 0, 0.2);
            color: #ffc800;
        }}
        
        .timestamp {{
            text-align: center;
            color: #666;
            font-size: 0.9em;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #0f3460;
        }}
        
        .test-detail {{
            font-size: 0.9em;
            color: #a0a0a0;
            margin-top: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Grid07 AI Evaluation Dashboard</h1>
            <p class="subtitle">LLM-as-Judge Automated Testing Results</p>
        </header>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">Overall Score</div>
                <div class="metric-value">{avg_overall:.2f}<span class="metric-max"> / 5</span></div>
                <div class="score-bar"><div class="score-fill" style="width: {(avg_overall/5)*100}%"></div></div>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">Relevance</div>
                <div class="metric-value">{avg_relevance:.2f}<span class="metric-max"> / 5</span></div>
                <div class="score-bar"><div class="score-fill" style="width: {(avg_relevance/5)*100}%"></div></div>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">Faithfulness</div>
                <div class="metric-value">{avg_faithfulness:.2f}<span class="metric-max"> / 5</span></div>
                <div class="score-bar"><div class="score-fill" style="width: {(avg_faithfulness/5)*100}%"></div></div>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">Safety</div>
                <div class="metric-value">{avg_safety:.2f}<span class="metric-max"> / 5</span></div>
                <div class="score-bar"><div class="score-fill" style="width: {(avg_safety/5)*100}%"></div></div>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">Injection Resistance</div>
                <div class="metric-value">{avg_injection:.2f}<span class="metric-max"> / 5</span></div>
                <div class="score-bar"><div class="score-fill" style="width: {(avg_injection/5)*100 if avg_injection else 0}%"></div></div>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">Total Tests</div>
                <div class="metric-value">{total}</div>
                <div class="test-detail">{len(passing_tests)} passing • {len(failing_tests)} needs improvement</div>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">Performance by Category</h2>
            <div class="category-grid">
"""
    
    for cat, cat_results in sorted(by_category.items()):
        avg = sum(r['evaluation']['overall'] for r in cat_results) / len(cat_results)
        html += f"""
                <div class="category-item">
                    <div class="category-name">{cat}</div>
                    <div class="category-stats">
                        <span>{len(cat_results)} tests</span>
                        <span class="score {'score-high' if avg >= 4 else 'score-medium' if avg >= 3 else 'score-low'}">{avg:.2f} / 5</span>
                    </div>
                </div>
"""
    
    html += """
            </div>
        </div>
"""
    
    if failing_tests:
        html += """
        <div class="section">
            <h2 class="section-title">⚠️ Tests Needing Improvement (< 3.0)</h2>
            <table>
                <thead>
                    <tr>
                        <th>Test ID</th>
                        <th>Category</th>
                        <th>Overall</th>
                        <th>R</th>
                        <th>F</th>
                        <th>S</th>
                        <th>Issue</th>
                    </tr>
                </thead>
                <tbody>
"""
        for test in failing_tests:
            eval_data = test['evaluation']
            html += f"""
                    <tr>
                        <td><strong>{test['id']}</strong></td>
                        <td>{test['category']}</td>
                        <td><span class="score score-low">{eval_data['overall']:.2f}</span></td>
                        <td>{eval_data['relevance']}</td>
                        <td>{eval_data['faithfulness']}</td>
                        <td>{eval_data['safety']}</td>
                        <td><span class="badge badge-fail">{', '.join(eval_data.get('issues', ['Unknown']))}</span></td>
                    </tr>
"""
        html += """
                </tbody>
            </table>
        </div>
"""
    
    html += """
        <div class="section">
            <h2 class="section-title">All Test Results</h2>
            <table>
                <thead>
                    <tr>
                        <th>Test ID</th>
                        <th>Category</th>
                        <th>Bot</th>
                        <th>Overall</th>
                        <th>R</th>
                        <th>F</th>
                        <th>S</th>
                        <th>IR</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
"""
    
    for test in results:
        eval_data = test['evaluation']
        score_class = 'score-high' if eval_data['overall'] >= 4 else 'score-medium' if eval_data['overall'] >= 3 else 'score-low'
        status_badge = 'badge-pass' if eval_data['overall'] >= 4 else 'badge-warning' if eval_data['overall'] >= 3 else 'badge-fail'
        status_text = 'Excellent' if eval_data['overall'] >= 4 else 'Acceptable' if eval_data['overall'] >= 3 else 'Needs Work'
        
        html += f"""
                    <tr>
                        <td><strong>{test['id']}</strong></td>
                        <td>{test['category']}</td>
                        <td>{test['bot_id']}</td>
                        <td><span class="score {score_class}">{eval_data['overall']:.2f}</span></td>
                        <td>{eval_data['relevance']}</td>
                        <td>{eval_data['faithfulness']}</td>
                        <td>{eval_data['safety']}</td>
                        <td>{eval_data['injection_resistance'] if eval_data['injection_resistance'] is not None else 'N/A'}</td>
                        <td><span class="badge {status_badge}">{status_text}</span></td>
                    </tr>
"""
    
    html += f"""
                </tbody>
            </table>
        </div>
        
        <div class="timestamp">
            Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
</body>
</html>
"""
    
    with open(output_file, 'w') as f:
        f.write(html)
    
    print(f"📊 Dashboard generated: {output_file}")
    return output_file


if __name__ == "__main__":
    generate_dashboard()
