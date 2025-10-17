# Real-World Security Testing Scenarios

This document provides practical examples of how to use the security scripts in real-world scenarios for penetration testing, bug bounty hunting, and security assessments.

## 🎯 Bug Bounty Hunting

### Scenario 1: Web Application Security Assessment
```bash
# 1. Start with reconnaissance
python scripts/network/port_scanner.py -t target.com --common

# 2. Check SSL configuration
python scripts/network/ssl_check.py target.com

# 3. Perform comprehensive vulnerability scan
python scripts/web/advanced_vulnerability_scanner.py https://target.com \
    --depth 3 \
    --threads 20 \
    --output bug_bounty_scan.json

# 4. Test specific API endpoints
python scripts/web/api_security_tester.py https://api.target.com

# 5. Check for OAuth misconfigurations
python scripts/web/oauth_scanner.py target.com
```

### Scenario 2: API Security Testing
```bash
# Test REST API security
python scripts/web/api_security_tester.py https://api.example.com/v1 \
    --methods GET,POST,PUT,DELETE \
    --auth-header "Authorization: Bearer token123"

# Test GraphQL endpoints
python scripts/web/api_security_tester.py https://api.example.com/graphql \
    --graphql-introspection \
    --graphql-injection
```

## 🔍 Penetration Testing

### Scenario 3: Internal Network Assessment
```bash
# 1. Network discovery
for ip in 192.168.1.{1..254}; do
    echo "Scanning $ip:"
    python scripts/network/port_scanner.py -t $ip --common
done

# 2. Check for exposed services
python scripts/network/backup_scanner.py 192.168.1.0/24

# 3. Test web applications
python scripts/web/advanced_vulnerability_scanner.py http://192.168.1.100
```

### Scenario 4: External Security Assessment
```bash
# 1. External port scan
python scripts/network/port_scanner.py -t target.com -p 1-1000

# 2. SSL/TLS analysis
python scripts/network/ssl_check.py target.com

# 3. Web application testing
python scripts/web/advanced_vulnerability_scanner.py https://target.com

# 4. API security testing
python scripts/web/api_security_tester.py https://api.target.com
```

## 🏢 Enterprise Security Testing

### Scenario 5: Corporate Network Assessment
```bash
# 1. Network segmentation testing
python scripts/network/port_scanner.py -t 10.0.0.0/24 --common

# 2. Check for exposed databases
python scripts/network/backup_scanner.py 10.0.0.0/24

# 3. Test internal web applications
python scripts/web/advanced_vulnerability_scanner.py http://internal-app.company.com

# 4. OAuth configuration review
python scripts/web/oauth_scanner.py company.com
```

### Scenario 6: Cloud Security Assessment
```bash
# 1. Test cloud endpoints
python scripts/web/api_security_tester.py https://cloud-api.company.com

# 2. Check for misconfigured services
python scripts/network/backup_scanner.py cloud-instance.company.com

# 3. Test authentication mechanisms
python scripts/web/oauth_scanner.py cloud.company.com
```

## 🔐 Cryptographic Security

### Scenario 7: Hash Analysis
```bash
# 1. Generate hashes for password analysis
python scripts/crypto/hash_generator.py "password123" --all

# 2. Verify hash integrity
python scripts/crypto/hash_generator.py "data.txt" --verify "expected_hash"

# 3. Test password strength
python scripts/crypto/hash_generator.py "weak_password" -a sha256
```

## 📊 Security Reporting

### Scenario 8: Automated Security Reporting
```bash
# 1. Run comprehensive scan
python scripts/web/advanced_vulnerability_scanner.py https://target.com \
    --output vulnerabilities.json

# 2. Generate security report
python scripts/automation/security_report_generator.py \
    --add-vuln "XSS" "High" "Reflected XSS in search parameter" \
    --add-vuln "SQL Injection" "Critical" "SQL injection in login form" \
    -o security_report.html -f html
```

## 🚀 Continuous Security Testing

### Scenario 9: CI/CD Integration
```bash
#!/bin/bash
# security_test.sh - CI/CD security testing script

TARGET=$1
if [ -z "$TARGET" ]; then
    echo "Usage: $0 <target>"
    exit 1
fi

echo "Starting security tests for $TARGET"

# SSL/TLS check
echo "Checking SSL configuration..."
python scripts/network/ssl_check.py $TARGET

# Port scan
echo "Scanning ports..."
python scripts/network/port_scanner.py -t $TARGET --common

# Vulnerability scan
echo "Running vulnerability scan..."
python scripts/web/advanced_vulnerability_scanner.py https://$TARGET \
    --output security_scan.json

# Generate report
echo "Generating security report..."
python scripts/automation/security_report_generator.py \
    -o security_report.html -f html

echo "Security testing completed"
```

### Scenario 10: Scheduled Security Monitoring
```bash
#!/bin/bash
# daily_security_check.sh - Daily security monitoring

TARGETS=("example.com" "api.example.com" "admin.example.com")
DATE=$(date +%Y%m%d)
LOG_DIR="logs/security_checks/$DATE"

mkdir -p "$LOG_DIR"

for target in "${TARGETS[@]}"; do
    echo "Checking $target..."
    
    # SSL check
    python scripts/network/ssl_check.py $target > "$LOG_DIR/${target}_ssl.json"
    
    # Port scan
    python scripts/network/port_scanner.py -t $target --common > "$LOG_DIR/${target}_ports.json"
    
    # Vulnerability scan
    python scripts/web/advanced_vulnerability_scanner.py https://$target \
        --output "$LOG_DIR/${target}_vulns.json"
done

# Generate daily report
python scripts/automation/security_report_generator.py \
    -o "$LOG_DIR/daily_security_report.html" -f html
```

## 🎯 Specialized Testing Scenarios

### Scenario 11: E-commerce Security Testing
```bash
# 1. Test payment processing
python scripts/web/advanced_vulnerability_scanner.py https://shop.example.com/checkout

# 2. Test user authentication
python scripts/web/advanced_vulnerability_scanner.py https://shop.example.com/login

# 3. Test API endpoints
python scripts/web/api_security_tester.py https://api.shop.example.com

# 4. Test for race conditions
python scripts/web/race_condition_tester.py https://shop.example.com/api/purchase
```

### Scenario 12: Social Media Security Testing
```bash
# 1. Test social media APIs
python scripts/web/api_security_tester.py https://api.social.example.com

# 2. Test OAuth implementations
python scripts/web/oauth_scanner.py social.example.com

# 3. Test for authentication bypass
python scripts/web/advanced_vulnerability_scanner.py https://social.example.com
```

## 🔧 Custom Integration Examples

### Scenario 13: Custom Security Dashboard
```python
#!/usr/bin/env python3
"""
Custom Security Dashboard
Integrates multiple security scripts for comprehensive monitoring
"""

import subprocess
import json
import time
from datetime import datetime

class SecurityDashboard:
    def __init__(self, targets):
        self.targets = targets
        self.results = {}
    
    def run_ssl_check(self, target):
        """Run SSL certificate check"""
        cmd = f"python scripts/network/ssl_check.py {target}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return json.loads(result.stdout)
    
    def run_port_scan(self, target):
        """Run port scan"""
        cmd = f"python scripts/network/port_scanner.py -t {target} --common"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout
    
    def run_vulnerability_scan(self, target):
        """Run vulnerability scan"""
        cmd = f"python scripts/web/advanced_vulnerability_scanner.py https://{target}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout
    
    def generate_report(self):
        """Generate comprehensive security report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "targets": self.targets,
            "results": self.results
        }
        
        with open("security_dashboard_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        print("Security dashboard report generated: security_dashboard_report.json")

# Usage
if __name__ == "__main__":
    targets = ["example.com", "api.example.com", "admin.example.com"]
    dashboard = SecurityDashboard(targets)
    
    for target in targets:
        print(f"Scanning {target}...")
        dashboard.results[target] = {
            "ssl": dashboard.run_ssl_check(target),
            "ports": dashboard.run_port_scan(target),
            "vulnerabilities": dashboard.run_vulnerability_scan(target)
        }
    
    dashboard.generate_report()
```

## 📋 Best Practices

### 1. Pre-Scan Preparation
- ✅ **Obtain proper authorization** before testing
- ✅ **Document the scope** of testing
- ✅ **Set up monitoring** for the target systems
- ✅ **Prepare incident response** procedures

### 2. During Testing
- ✅ **Start with low-intensity scans** to avoid overwhelming targets
- ✅ **Monitor target systems** for any issues
- ✅ **Document all findings** with proper evidence
- ✅ **Respect rate limits** and system resources

### 3. Post-Testing
- ✅ **Generate comprehensive reports** of all findings
- ✅ **Prioritize vulnerabilities** by severity and impact
- ✅ **Follow responsible disclosure** practices
- ✅ **Provide remediation guidance** for each finding

## ⚠️ Legal and Ethical Considerations

### Authorization Requirements
- **Written permission** from system owners
- **Clear scope definition** of what can be tested
- **Time boundaries** for testing activities
- **Contact information** for incident response

### Responsible Disclosure
- **Report vulnerabilities** through proper channels
- **Provide adequate time** for remediation
- **Avoid public disclosure** until fixed
- **Follow coordinated disclosure** practices

### Legal Compliance
- **Understand local laws** regarding security testing
- **Comply with data protection** regulations
- **Respect privacy** and confidentiality
- **Maintain professional** standards

---

**Remember: These scenarios are for educational and authorized testing purposes only. Always obtain proper authorization before testing any systems.**
