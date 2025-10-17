#!/usr/bin/env python3
"""
Security Report Generator - Automated security reporting
Author: Safouan Benali
License: MIT
"""

import json
import time
import argparse
from datetime import datetime
from typing import Dict, List, Any

class SecurityReportGenerator:
    """Generate comprehensive security reports."""
    
    def __init__(self):
        self.report_data = {
            'metadata': {},
            'summary': {},
            'vulnerabilities': [],
            'recommendations': []
        }
    
    def add_scan_result(self, scan_type: str, results: Dict):
        """Add scan results to report."""
        self.report_data['vulnerabilities'].append({
            'scan_type': scan_type,
            'timestamp': time.time(),
            'results': results
        })
    
    def generate_summary(self) -> Dict:
        """Generate executive summary."""
        total_vulns = len(self.report_data['vulnerabilities'])
        critical = sum(1 for v in self.report_data['vulnerabilities'] 
                       if v.get('results', {}).get('severity') == 'critical')
        high = sum(1 for v in self.report_data['vulnerabilities'] 
                  if v.get('results', {}).get('severity') == 'high')
        medium = sum(1 for v in self.report_data['vulnerabilities'] 
                    if v.get('results', {}).get('severity') == 'medium')
        low = sum(1 for v in self.report_data['vulnerabilities'] 
                 if v.get('results', {}).get('severity') == 'low')
        
        return {
            'total_vulnerabilities': total_vulns,
            'critical': critical,
            'high': high,
            'medium': medium,
            'low': low,
            'risk_score': (critical * 4 + high * 3 + medium * 2 + low * 1) / max(total_vulns, 1)
        }
    
    def generate_recommendations(self) -> List[Dict]:
        """Generate security recommendations."""
        recommendations = []
        
        # Check for common issues and provide recommendations
        vuln_types = [v.get('scan_type', '') for v in self.report_data['vulnerabilities']]
        
        if 'ssl' in str(vuln_types).lower():
            recommendations.append({
                'category': 'SSL/TLS',
                'priority': 'High',
                'recommendation': 'Update SSL certificates and use strong cipher suites',
                'action': 'Implement TLS 1.2+ and disable weak ciphers'
            })
        
        if 'sql' in str(vuln_types).lower():
            recommendations.append({
                'category': 'Database Security',
                'priority': 'Critical',
                'recommendation': 'Implement parameterized queries and input validation',
                'action': 'Review and fix SQL injection vulnerabilities'
            })
        
        if 'port' in str(vuln_types).lower():
            recommendations.append({
                'category': 'Network Security',
                'priority': 'Medium',
                'recommendation': 'Close unnecessary open ports',
                'action': 'Review firewall rules and close unused services'
            })
        
        return recommendations
    
    def generate_html_report(self) -> str:
        """Generate HTML security report."""
        summary = self.generate_summary()
        recommendations = self.generate_recommendations()
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Security Assessment Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
        .summary {{ background: #ecf0f1; padding: 20px; margin: 20px 0; border-radius: 5px; }}
        .vulnerability {{ background: #fff; border-left: 4px solid #e74c3c; padding: 15px; margin: 10px 0; }}
        .recommendation {{ background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        .critical {{ border-left-color: #e74c3c; }}
        .high {{ border-left-color: #f39c12; }}
        .medium {{ border-left-color: #f1c40f; }}
        .low {{ border-left-color: #27ae60; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Security Assessment Report</h1>
        <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="summary">
        <h2>Executive Summary</h2>
        <p><strong>Total Vulnerabilities:</strong> {summary['total_vulnerabilities']}</p>
        <p><strong>Critical:</strong> {summary['critical']} | <strong>High:</strong> {summary['high']} | 
           <strong>Medium:</strong> {summary['medium']} | <strong>Low:</strong> {summary['low']}</p>
        <p><strong>Risk Score:</strong> {summary['risk_score']:.2f}/4.0</p>
    </div>
    
    <h2>Vulnerabilities</h2>
    """
        
        for vuln in self.report_data['vulnerabilities']:
            severity = vuln.get('results', {}).get('severity', 'unknown')
            html += f"""
    <div class="vulnerability {severity}">
        <h3>{vuln.get('scan_type', 'Unknown')}</h3>
        <p><strong>Severity:</strong> {severity.upper()}</p>
        <p><strong>Details:</strong> {vuln.get('results', {}).get('description', 'No description available')}</p>
    </div>
    """
        
        html += """
    <h2>Recommendations</h2>
    """
        
        for rec in recommendations:
            html += f"""
    <div class="recommendation">
        <h3>{rec['category']} - {rec['priority']} Priority</h3>
        <p><strong>Recommendation:</strong> {rec['recommendation']}</p>
        <p><strong>Action:</strong> {rec['action']}</p>
    </div>
    """
        
        html += """
</body>
</html>
"""
        return html
    
    def save_report(self, filename: str, format_type: str = 'json'):
        """Save report to file."""
        if format_type == 'json':
            with open(filename, 'w') as f:
                json.dump(self.report_data, f, indent=2)
        elif format_type == 'html':
            html_content = self.generate_html_report()
            with open(filename, 'w') as f:
                f.write(html_content)
        else:
            raise ValueError(f"Unsupported format: {format_type}")

def main():
    parser = argparse.ArgumentParser(description='Security Report Generator')
    parser.add_argument('-o', '--output', required=True, help='Output file')
    parser.add_argument('-f', '--format', choices=['json', 'html'], default='json', help='Output format')
    parser.add_argument('--add-vuln', action='append', nargs=3, 
                       metavar=('TYPE', 'SEVERITY', 'DESCRIPTION'),
                       help='Add vulnerability to report')
    
    args = parser.parse_args()
    
    generator = SecurityReportGenerator()
    
    # Add sample vulnerabilities if specified
    if args.add_vuln:
        for vuln_type, severity, description in args.add_vuln:
            generator.add_scan_result(vuln_type, {
                'severity': severity,
                'description': description
            })
    
    generator.save_report(args.output, args.format)
    print(f"Report saved to {args.output}")

if __name__ == "__main__":
    main()
