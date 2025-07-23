"""
Report Handler
-------------
Generates and manages debugging reports.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any


class ReportHandler:
    """Handles report generation and management."""
    
    def __init__(self, config):
        self.config = config
        self.reports_dir = config.get('reports_dir', 'auto_debugger/reports')
        
        # Create reports directory if it doesn't exist
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def generate_report(self, analysis_results: Dict[str, Any]) -> str:
        """Generate a comprehensive debugging report."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = os.path.join(self.reports_dir, f'debug_report_{timestamp}.json')
        
        # Prepare report data
        report_data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'debugger_version': '1.0.0',
                'analysis_type': 'full_project_scan'
            },
            'summary': analysis_results.get('summary', {}),
            'issues': {
                'errors': analysis_results.get('errors', []),
                'warnings': analysis_results.get('warnings', []),
                'performance_issues': analysis_results.get('performance_issues', [])
            },
            'code_quality': analysis_results.get('code_quality', {}),
            'recommendations': self._generate_recommendations(analysis_results)
        }
        
        # Save JSON report
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        # Generate HTML report
        html_file = self._generate_html_report(report_data, timestamp)
        
        return report_file
    
    def _generate_recommendations(self, results: Dict[str, Any]) -> list:
        """Generate recommendations based on analysis results."""
        recommendations = []
        
        errors = results.get('errors', [])
        warnings = results.get('warnings', [])
        performance_issues = results.get('performance_issues', [])
        
        # Critical error recommendations
        critical_errors = [e for e in errors if e.get('severity') == 'CRITICAL']
        if critical_errors:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Critical Issues',
                'message': f'Fix {len(critical_errors)} critical syntax errors immediately',
                'action': 'Review and fix syntax errors to prevent runtime failures'
            })
        
        # Code quality recommendations
        if len(warnings) > 20:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Code Quality',
                'message': 'High number of code quality warnings detected',
                'action': 'Review coding standards and refactor problematic areas'
            })
        
        # Performance recommendations
        if len(performance_issues) > 5:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Performance',
                'message': 'Multiple performance issues detected',
                'action': 'Optimize loops, string operations, and imports'
            })
        
        return recommendations
    
    def _generate_html_report(self, report_data: Dict[str, Any], timestamp: str) -> str:
        """Generate an HTML version of the report."""
        html_file = os.path.join(self.reports_dir, f'debug_report_{timestamp}.html')
        
        html_content = self._create_html_template(report_data)
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return html_file
    
    def _create_html_template(self, data: Dict[str, Any]) -> str:
        """Create HTML template for the report."""
        summary = data.get('summary', {})
        issues = data.get('issues', {})
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Auto Debugger Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f4f4f4; padding: 20px; border-radius: 5px; }}
        .summary {{ display: flex; gap: 20px; margin: 20px 0; }}
        .stat-card {{ background: #e8f4fd; padding: 15px; border-radius: 5px; flex: 1; }}
        .critical {{ background-color: #ffe6e6; }}
        .warning {{ background-color: #fff3cd; }}
        .info {{ background-color: #e6f3ff; }}
        .issue {{ margin: 10px 0; padding: 10px; border-left: 4px solid #ccc; }}
        .issue.critical {{ border-left-color: #dc3545; }}
        .issue.high {{ border-left-color: #fd7e14; }}
        .issue.medium {{ border-left-color: #ffc107; }}
        .issue.low {{ border-left-color: #28a745; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 Auto Debugger Report</h1>
        <p>Generated: {data.get('metadata', {}).get('generated_at', 'Unknown')}</p>
    </div>
    
    <div class="summary">
        <div class="stat-card critical">
            <h3>🚨 Errors</h3>
            <p style="font-size: 24px; margin: 0;">{len(issues.get('errors', []))}</p>
        </div>
        <div class="stat-card warning">
            <h3>⚠️ Warnings</h3>
            <p style="font-size: 24px; margin: 0;">{len(issues.get('warnings', []))}</p>
        </div>
        <div class="stat-card info">
            <h3>📊 Performance Issues</h3>
            <p style="font-size: 24px; margin: 0;">{len(issues.get('performance_issues', []))}</p>
        </div>
        <div class="stat-card">
            <h3>📁 Files Analyzed</h3>
            <p style="font-size: 24px; margin: 0;">{summary.get('total_files', 0)}</p>
        </div>
    </div>
"""
        
        # Add errors section
        if issues.get('errors'):
            html += '<h2>🚨 Critical Errors</h2>'
            for error in issues['errors']:
                severity_class = error.get('severity', 'medium').lower()
                html += f'''
                <div class="issue {severity_class}">
                    <strong>{error.get('type', 'Error')}</strong> in {error.get('file', 'Unknown')}:{error.get('line', 0)}<br>
                    {error.get('message', 'No message')}
                </div>
                '''
        
        # Add recommendations
        recommendations = data.get('recommendations', [])
        if recommendations:
            html += '<h2>💡 Recommendations</h2>'
            for rec in recommendations:
                priority_class = rec.get('priority', 'medium').lower()
                html += f'''
                <div class="issue {priority_class}">
                    <strong>[{rec.get('priority', 'MEDIUM')}] {rec.get('category', 'General')}</strong><br>
                    {rec.get('message', '')}<br>
                    <em>Action: {rec.get('action', '')}</em>
                </div>
                '''
        
        html += '</body></html>'
        return html
    
    def get_latest_report(self) -> str:
        """Get the path to the latest report."""
        reports = [f for f in os.listdir(self.reports_dir) if f.endswith('.json')]
        if not reports:
            return ""
        
        reports.sort(reverse=True)
        return os.path.join(self.reports_dir, reports[0])
    
    def cleanup_old_reports(self, keep_count: int = 10):
        """Clean up old report files, keeping only the most recent ones."""
        reports = [f for f in os.listdir(self.reports_dir) if f.startswith('debug_report_')]
        reports.sort(reverse=True)
        
        # Remove old reports
        for report in reports[keep_count:]:
            try:
                os.remove(os.path.join(self.reports_dir, report))
            except OSError:
                pass
