#!/usr/bin/env python3
"""
OAUTH SCANNER - EFFICIENT OAUTH MISCONFIGURATION DETECTION
==========================================================
Lean scanner using regex patterns to find OAuth misconfigurations.
No massive lists - just smart pattern matching.
"""

import requests
import re
import json
import time
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor

class OAuthScanner:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.misconfigs = []
    
    def scan_target(self, target):
        """Scan target for OAuth misconfigurations"""
        print(f"🔍 Scanning {target} for OAuth misconfigurations...")
        
        # Generate OAuth URLs
        oauth_urls = self.generate_oauth_urls(target)
        
        # Test URLs in parallel
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(self.test_oauth_endpoint, oauth_urls))
        
        # Filter successful results
        found_endpoints = [url for url, success in zip(oauth_urls, results) if success]
        
        if found_endpoints:
            print(f"🚨 FOUND {len(found_endpoints)} OAUTH ENDPOINTS!")
            for endpoint in found_endpoints:
                print(f"   🔐 {endpoint}")
        else:
            print("✅ No OAuth endpoints found")
        
        return found_endpoints
    
    def generate_oauth_urls(self, target):
        """Generate OAuth URLs using efficient patterns"""
        urls = []
        
        # Ensure target has protocol
        if not target.startswith('http'):
            target = f"https://{target}"
        
        # OAuth endpoint patterns using regex
        oauth_patterns = [
            r'/.well-known/openid_configuration',
            r'/oauth/authorize',
            r'/oauth/token',
            r'/oauth/userinfo',
            r'/api/oauth/authorize',
            r'/api/oauth/token',
            r'/api/oauth/userinfo',
            r'/auth/oauth/authorize',
            r'/auth/oauth/token',
            r'/auth/oauth/userinfo',
            r'/v1/oauth/authorize',
            r'/v1/oauth/token',
            r'/v1/oauth/userinfo',
            r'/v2/oauth/authorize',
            r'/v2/oauth/token',
            r'/v2/oauth/userinfo'
        ]
        
        # Generate URLs for each pattern
        for pattern in oauth_patterns:
            url = f"{target}{pattern}"
            urls.append(url)
        
        return urls
    
    def test_oauth_endpoint(self, url):
        """Test if OAuth endpoint is accessible"""
        try:
            response = self.session.get(url, timeout=5)
            
            if response.status_code == 200:
                # Check if it's actually an OAuth endpoint
                content = response.text.lower()
                
                # OAuth indicators
                oauth_indicators = ['oauth', 'openid', 'authorization', 'token', 'userinfo', 'issuer', 'endpoint']
                
                if any(indicator in content for indicator in oauth_indicators):
                    return True
                    
        except Exception:
            pass
        
        return False
    
    def analyze_oauth_config(self, url):
        """Analyze OAuth configuration for misconfigurations"""
        try:
            response = self.session.get(url, timeout=5)
            
            if response.status_code == 200:
                content = response.text
                
                # Parse JSON if possible
                try:
                    config = json.loads(content)
                    return self.check_oauth_misconfig(config, url)
                except:
                    # Not JSON, check for other misconfigurations
                    return self.check_oauth_misconfig_text(content, url)
                    
        except Exception:
            pass
        
        return None
    
    def check_oauth_misconfig(self, config, url):
        """Check OAuth configuration for misconfigurations"""
        misconfigs = []
        
        # Check for common misconfigurations
        checks = [
            {
                'name': 'Issuer Mismatch',
                'pattern': r'"issuer":\s*"https://[^"]*"',
                'severity': 'HIGH',
                'description': 'OAuth issuer may be misconfigured'
            },
            {
                'name': 'Authorization Endpoint',
                'pattern': r'"authorization_endpoint":\s*"https://[^"]*"',
                'severity': 'MEDIUM',
                'description': 'Authorization endpoint found'
            },
            {
                'name': 'Token Endpoint',
                'pattern': r'"token_endpoint":\s*"https://[^"]*"',
                'severity': 'MEDIUM',
                'description': 'Token endpoint found'
            },
            {
                'name': 'Userinfo Endpoint',
                'pattern': r'"userinfo_endpoint":\s*"https://[^"]*"',
                'severity': 'MEDIUM',
                'description': 'Userinfo endpoint found'
            },
            {
                'name': 'JWKS Endpoint',
                'pattern': r'"jwks_uri":\s*"https://[^"]*"',
                'severity': 'MEDIUM',
                'description': 'JWKS endpoint found'
            }
        ]
        
        for check in checks:
            if re.search(check['pattern'], json.dumps(config), re.IGNORECASE):
                misconfigs.append({
                    'type': check['name'],
                    'severity': check['severity'],
                    'url': url,
                    'description': check['description']
                })
        
        return misconfigs
    
    def check_oauth_misconfig_text(self, content, url):
        """Check OAuth configuration text for misconfigurations"""
        misconfigs = []
        
        # Check for common misconfigurations in text
        checks = [
            {
                'name': 'OAuth Configuration',
                'pattern': r'oauth|openid|authorization|token|userinfo',
                'severity': 'MEDIUM',
                'description': 'OAuth configuration found'
            },
            {
                'name': 'API Key Exposure',
                'pattern': r'api[_-]?key["\']?\s*[:=]\s*["\']?[A-Za-z0-9_-]+["\']?',
                'severity': 'HIGH',
                'description': 'API key may be exposed'
            },
            {
                'name': 'Client Secret Exposure',
                'pattern': r'client[_-]?secret["\']?\s*[:=]\s*["\']?[A-Za-z0-9_-]+["\']?',
                'severity': 'CRITICAL',
                'description': 'Client secret may be exposed'
            }
        ]
        
        for check in checks:
            if re.search(check['pattern'], content, re.IGNORECASE):
                misconfigs.append({
                    'type': check['name'],
                    'severity': check['severity'],
                    'url': url,
                    'description': check['description']
                })
        
        return misconfigs
    
    def run_oauth_scan(self, target):
        """Run comprehensive OAuth scan"""
        print(f"🔥 OAUTH SCANNER - SCANNING {target} 🔥")
        print("=" * 60)
        
        start_time = time.time()
        
        # Scan for OAuth endpoints
        endpoints = self.scan_target(target)
        
        # Analyze found endpoints
        if endpoints:
            print(f"\n🔍 ANALYZING {len(endpoints)} OAUTH ENDPOINTS...")
            
            for endpoint in endpoints:
                print(f"\n🔐 Analyzing: {endpoint}")
                
                # Analyze configuration
                misconfigs = self.analyze_oauth_config(endpoint)
                
                if misconfigs:
                    print(f"🚨 MISCONFIGURATIONS FOUND:")
                    for misconfig in misconfigs:
                        print(f"   {misconfig['severity']}: {misconfig['type']}")
                        print(f"     {misconfig['description']}")
                else:
                    print("✅ No misconfigurations detected")
        
        duration = time.time() - start_time
        
        print("=" * 60)
        print("🎯 OAUTH SCAN COMPLETED!")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Endpoints found: {len(endpoints)}")
        print("=" * 60)
        
        return endpoints

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python3 oauth_scanner.py <target>")
        print("Example: python3 oauth_scanner.py example.com")
        sys.exit(1)
    
    target = sys.argv[1]
    
    scanner = OAuthScanner()
    endpoints = scanner.run_oauth_scan(target)
