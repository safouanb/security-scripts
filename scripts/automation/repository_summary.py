#!/usr/bin/env python3
"""
Repository Summary - Display repository statistics and capabilities
Author: Safouan Benali
License: MIT
"""

import os
import json
import sys
from pathlib import Path

class RepositorySummary:
    """Generate comprehensive repository statistics and capabilities."""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.stats = {
            'scripts': {},
            'categories': {},
            'total_files': 0,
            'total_lines': 0,
            'capabilities': []
        }
    
    def analyze_repository(self):
        """Analyze the repository structure and capabilities."""
        # Count files by category
        categories = ['network', 'web', 'crypto', 'automation']
        
        for category in categories:
            category_path = self.repo_path / 'scripts' / category
            if category_path.exists():
                scripts = list(category_path.glob('*.py'))
                self.stats['categories'][category] = {
                    'scripts': len(scripts),
                    'files': [s.name for s in scripts]
                }
        
        # Count total files and lines
        for py_file in self.repo_path.rglob('*.py'):
            if 'test' not in str(py_file):
                self.stats['total_files'] += 1
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        lines = len(f.readlines())
                        self.stats['total_lines'] += lines
                except Exception:
                    pass
        
        # Define capabilities
        self.stats['capabilities'] = [
            "SSL/TLS Certificate Analysis",
            "Network Port Scanning",
            "SQL Injection Testing", 
            "Hash Generation & Verification",
            "Security Report Generation",
            "Automated Vulnerability Assessment",
            "Cryptographic Operations",
            "Web Security Testing"
        ]
    
    def generate_summary(self):
        """Generate a formatted summary."""
        self.analyze_repository()
        
        print("🔒 Security Scripts Repository Summary")
        print("=" * 50)
        print(f"📁 Total Scripts: {self.stats['total_files']}")
        print(f"📝 Total Lines of Code: {self.stats['total_lines']:,}")
        print(f"🏷️  Categories: {len(self.stats['categories'])}")
        
        print("\n📊 Script Categories:")
        for category, data in self.stats['categories'].items():
            print(f"  {category.title()}: {data['scripts']} scripts")
            for script in data['files']:
                print(f"    - {script}")
        
        print("\n🛠️  Capabilities:")
        for capability in self.stats['capabilities']:
            print(f"  ✓ {capability}")
        
        print("\n📋 Repository Structure:")
        print("  scripts/")
        print("    ├── network/     # Network security tools")
        print("    ├── web/         # Web application security")
        print("    ├── crypto/      # Cryptographic utilities")
        print("    └── automation/  # Security automation")
        print("  tests/            # Unit tests")
        print("  docs/             # Documentation")
        print("  examples/         # Usage examples")
        
        print("\n🚀 Quick Start:")
        print("  python scripts/network/ssl_check.py example.com")
        print("  python scripts/network/port_scanner.py -t 192.168.1.1")
        print("  python scripts/web/sql_injection_tester.py -u https://example.com")
        
        print("\n📄 Documentation:")
        print("  README.md - Main documentation")
        print("  CONTRIBUTING.md - Contribution guidelines")
        print("  docs/script_documentation.md - Detailed script docs")
        
        return self.stats

def main():
    """Main function to run repository summary."""
    parser = argparse.ArgumentParser(description='Repository Summary Generator')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--path', default='.', help='Repository path')
    
    args = parser.parse_args()
    
    summary = RepositorySummary(args.path)
    stats = summary.generate_summary()
    
    if args.json:
        print("\n" + "="*50)
        print("JSON Output:")
        print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    import argparse
    main()
