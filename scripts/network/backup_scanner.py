#!/usr/bin/env python3
"""
BACKUP SCANNER - EFFICIENT DATABASE BACKUP DETECTION
====================================================
Lean scanner using regex patterns to find database backups.
No massive lists - just smart pattern matching.
"""

import requests
import re
import json
import time
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor

class BackupScanner:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.found_backups = []
    
    def scan_target(self, target):
        """Scan target for database backups"""
        print(f"🔍 Scanning {target} for database backups...")
        
        # Generate backup URLs using regex patterns
        backup_urls = self.generate_backup_urls(target)
        
        # Test URLs in parallel
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(self.test_backup_url, backup_urls))
        
        # Filter successful results
        found_backups = [url for url, success in zip(backup_urls, results) if success]
        
        if found_backups:
            print(f"🚨 FOUND {len(found_backups)} DATABASE BACKUPS!")
            for backup in found_backups:
                print(f"   📁 {backup}")
        else:
            print("✅ No database backups found")
        
        return found_backups
    
    def generate_backup_urls(self, target):
        """Generate backup URLs using efficient patterns"""
        urls = []
        
        # Ensure target has protocol
        if not target.startswith('http'):
            target = f"https://{target}"
        
        # Common backup paths
        paths = ['/backup/', '/backups/', '/db/', '/database/', '/dump/', '/sql/', '/data/', '/files/', '/downloads/', '/admin/', '/wp-content/', '/includes/', '/config/', '/temp/', '/tmp/', '/logs/', '/var/', '/home/', '/root/']
        
        # Backup filename patterns using regex
        backup_patterns = [
            r'backup\.(sql|db|sqlite|sqlite3|tar\.gz|zip|7z|rar|bak|dump)',
            r'database\.(sql|db|sqlite|sqlite3|tar\.gz|zip|7z|rar|bak|dump)',
            r'db\.(sql|db|sqlite|sqlite3|tar\.gz|zip|7z|rar|bak|dump)',
            r'dump\.(sql|db|sqlite|sqlite3|tar\.gz|zip|7z|rar|bak|dump)',
            r'data\.(sql|db|sqlite|sqlite3|tar\.gz|zip|7z|rar|bak|dump)',
            r'sql\.(sql|db|sqlite|sqlite3|tar\.gz|zip|7z|rar|bak|dump)',
            r'\.(sql|db|sqlite|sqlite3|tar\.gz|zip|7z|rar|bak|dump)$'
        ]
        
        # Generate URLs for each path and pattern
        for path in paths:
            for pattern in backup_patterns:
                # Extract extensions from pattern
                extensions = re.findall(r'\.(sql|db|sqlite|sqlite3|tar\.gz|zip|7z|rar|bak|dump)', pattern)
                
                for ext in extensions:
                    # Generate common backup filenames
                    filenames = ['backup', 'database', 'db', 'dump', 'data', 'sql', 'backup_' + time.strftime('%Y%m%d'), 'backup_' + time.strftime('%Y%m%d_%H%M%S')]
                    
                    for filename in filenames:
                        url = f"{target}{path}{filename}.{ext}"
                        urls.append(url)
        
        # Remove duplicates and limit
        urls = list(set(urls))[:100]  # Limit to prevent too many requests
        
        return urls
    
    def test_backup_url(self, url):
        """Test if backup URL is accessible"""
        try:
            response = self.session.head(url, timeout=5, allow_redirects=True)
            
            if response.status_code == 200:
                # Check if it's actually a backup file
                content_type = response.headers.get('content-type', '').lower()
                
                # Check for backup file indicators
                backup_indicators = ['sql', 'database', 'octet-stream', 'application/zip', 'application/x-rar', 'application/x-7z']
                
                if any(indicator in content_type for indicator in backup_indicators):
                    return True
                    
                # Check content length (backup files are usually large)
                content_length = response.headers.get('content-length')
                if content_length and int(content_length) > 1024:  # > 1KB
                    return True
                    
        except Exception:
            pass
        
        return False
    
    def download_backup_sample(self, backup_url, max_size=1024):
        """Download a small sample of the backup file"""
        try:
            response = self.session.get(backup_url, timeout=10, stream=True)
            
            if response.status_code == 200:
                # Read only first part of file
                content = b''
                for chunk in response.iter_content(chunk_size=1024):
                    content += chunk
                    if len(content) >= max_size:
                        break
                
                return content
                
        except Exception as e:
            print(f"⚠️ Error downloading backup: {e}")
        
        return None
    
    def analyze_backup_content(self, content):
        """Analyze backup content for sensitive data"""
        if not content:
            return None
        
        # Convert to string for analysis
        try:
            text = content.decode('utf-8', errors='ignore')
        except:
            text = str(content)
        
        # Look for sensitive data patterns
        sensitive_patterns = {
            'emails': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'passwords': r'password["\']?\s*[:=]\s*["\']?[^"\']+["\']?',
            'api_keys': r'api[_-]?key["\']?\s*[:=]\s*["\']?[A-Za-z0-9_-]+["\']?',
            'tokens': r'token["\']?\s*[:=]\s*["\']?[A-Za-z0-9_-]+["\']?',
            'credit_cards': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        }
        
        findings = {}
        
        for category, pattern in sensitive_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                findings[category] = matches[:5]  # Limit to first 5 matches
        
        return findings
    
    def run_backup_scan(self, target):
        """Run comprehensive backup scan"""
        print(f"🔥 BACKUP SCANNER - SCANNING {target} 🔥")
        print("=" * 60)
        
        start_time = time.time()
        
        # Scan for backups
        backups = self.scan_target(target)
        
        # Analyze found backups
        if backups:
            print(f"\n🔍 ANALYZING {len(backups)} BACKUP FILES...")
            
            for backup in backups[:3]:  # Analyze first 3 backups
                print(f"\n📁 Analyzing: {backup}")
                
                # Download sample
                sample = self.download_backup_sample(backup)
                
                if sample:
                    # Analyze content
                    findings = self.analyze_backup_content(sample)
                    
                    if findings:
                        print(f"🚨 SENSITIVE DATA FOUND:")
                        for category, data in findings.items():
                            print(f"   {category.upper()}: {len(data)} items")
                            for item in data[:3]:  # Show first 3 items
                                print(f"     - {item}")
                    else:
                        print("✅ No sensitive data detected in sample")
        
        duration = time.time() - start_time
        
        print("=" * 60)
        print("🎯 BACKUP SCAN COMPLETED!")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Backups found: {len(backups)}")
        print("=" * 60)
        
        return backups

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python3 backup_scanner.py <target>")
        print("Example: python3 backup_scanner.py example.com")
        sys.exit(1)
    
    target = sys.argv[1]
    
    scanner = BackupScanner()
    backups = scanner.run_backup_scan(target)
