# 🔒 Security Scripts Collection

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Security](https://img.shields.io/badge/Security-Focused-red.svg)](https://github.com/safouanb/security-scripts)

> A simple collection of security-focused Python scripts for penetration testing, vulnerability assessment, and security automation. These scripts I either found or wrote during my homelabbing sessions. Tried to add documentation to each

## 🎯 Table of Contents
- [🚀 Quick Start](#-quick-start)
- [📁 Script Categories](#-script-categories)
- [🛠️ Available Scripts](#️-available-scripts)
- [📊 Script Statistics](#-script-statistics)
- [🔧 Installation](#-installation)
- [📖 Usage Examples](#-usage-examples)
- [🛡️ Security Features](#️-security-features)
- [📚 Learning Resources](#-learning-resources)
- [⚠️ Legal & Ethical Guidelines](#️-legal--ethical-guidelines)
- [🤝 Contributing](#-contributing)

## 🎯 Overview

This repository contains a collection of professional security scripts designed for:
- **Network Security Assessment**
- **SSL/TLS Certificate Analysis**
- **Web Application Security Testing**
- **Cryptographic Operations**
- **Security Automation**

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/safouanb/security-scripts.git
cd security-scripts

# Install dependencies
pip install -r requirements.txt

# Run a script
python scripts/network/ssl_check.py example.com
```

## 📁 Script Categories

### 🌐 Network Security
- **SSL Certificate Checker** - Comprehensive SSL/TLS certificate validation
- **Port Scanner** - Fast and efficient port scanning
- **Backup Scanner** - Find exposed database backups and sensitive files

### 🔍 Web Security
- **SQL Injection Tester** - Automated SQL injection detection
- **Advanced Vulnerability Scanner** - Professional-grade vulnerability discovery
- **API Security Tester** - REST/GraphQL/WebSocket security testing
- **OAuth Scanner** - OAuth misconfiguration detection
- **Race Condition Tester** - Timing-based vulnerability testing
- **Advanced Parameter Fuzzer** - Parameter pollution, type confusion, prototype pollution
- **IDOR Tester** - Insecure Direct Object Reference vulnerability detection
- **Business Logic Scanner** - Business logic flaw detection and authorization bypass
- **HTTP Smuggling Tester** - HTTP request smuggling vulnerability testing

### 🔐 Cryptographic Tools
- **Hash Generator** - Multiple hash algorithm support

### 🤖 Automation Scripts
- **Security Report Generator** - Automated security reporting
- **Repository Summary** - Repository statistics and capabilities
- **Elite Attack Framework** - Professional-grade offensive security framework with stealth techniques
- **NBA Vulnerability Exploiter** - Advanced exploitation techniques for NBA bug bounty program

## 🛠️ Available Scripts

### SSL Certificate Checker
```bash
python scripts/network/ssl_check.py example.com
```
**Features:**
- Certificate chain validation
- Expiration date checking
- Cipher suite analysis
- Security grade assessment

### Port Scanner
```bash
python scripts/network/port_scanner.py -t 192.168.1.1 -p 1-1000
```
**Features:**
- Fast concurrent scanning
- Service detection
- Banner grabbing
- Custom port ranges

### SQL Injection Tester
```bash
python scripts/web/sql_injection_tester.py -u "https://example.com/search" -p "q"
```
**Features:**
- Multiple injection techniques
- Time-based blind SQLi detection
- Union-based injection testing
- Error-based detection

## 📊 Script Statistics

| Category | Scripts | Status |
|----------|---------|--------|
| Network Security | 3 | ✅ Active |
| Web Security | 9 | ✅ Active |
| Cryptographic | 1 | ✅ Active |
| Automation | 4 | ✅ Active |
| **Total** | **17** | **✅ All Working** |

## 🔧 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Dependencies
```bash
pip install -r requirements.txt
```

### Optional Dependencies
```bash
# For advanced network scanning
pip install scapy

# For web security testing
pip install requests beautifulsoup4

# For cryptographic operations
pip install cryptography pycryptodome
```

## 📖 Usage Examples

### SSL Certificate Analysis
```python
from scripts.network.ssl_check import SSLChecker

checker = SSLChecker("example.com")
result = checker.analyze()
print(f"SSL Grade: {result['grade']}")
print(f"Expires: {result['expiration']}")
```

### Network Port Scanning
```python
from scripts.network.port_scanner import PortScanner

scanner = PortScanner("192.168.1.1")
open_ports = scanner.scan_ports(1, 1000)
print(f"Open ports: {open_ports}")
```

### Web Vulnerability Testing
```python
from scripts.web.vulnerability_scanner import WebScanner

scanner = WebScanner("https://example.com")
vulnerabilities = scanner.scan()
for vuln in vulnerabilities:
    print(f"Found: {vuln['type']} at {vuln['url']}")
```

### Advanced Vulnerability Scanning
```bash
# Professional-grade vulnerability discovery
python scripts/web/advanced_vulnerability_scanner.py example.com

# API security testing
python scripts/web/api_security_tester.py https://api.example.com

# OAuth misconfiguration detection
python scripts/web/oauth_scanner.py example.com

# Race condition testing
python scripts/web/race_condition_tester.py https://example.com/api/purchase

# Backup and sensitive file discovery
python scripts/network/backup_scanner.py example.com

# Advanced parameter fuzzing (JUICY!)
python scripts/web/advanced_parameter_fuzzer.py https://example.com/api

# IDOR vulnerability testing (VERY JUICY!)
python scripts/web/idor_tester.py https://example.com/user/123

# Business logic flaw detection (EXTREMELY JUICY!)
python scripts/web/business_logic_scanner.py https://example.com

# HTTP request smuggling testing (ULTRA JUICY!)
python scripts/web/http_smuggling_tester.py https://example.com
```

## 🛡️ Security Features

### Safe by Design
- **Non-intrusive scanning** - All scripts designed for authorized testing only
- **Rate limiting** - Built-in delays to prevent overwhelming targets
- **Error handling** - Comprehensive error handling and logging
- **Legal compliance** - Scripts include usage warnings and legal disclaimers

### Professional Standards
- **Clean code** - Well-documented and maintainable code
- **Modular design** - Reusable components and functions
- **Testing** - Unit tests for critical functions
- **Logging** - Comprehensive logging for audit trails

## 📋 Requirements

### System Requirements
- **OS**: Linux, macOS, Windows
- **Python**: 3.8+
- **Memory**: 512MB minimum
- **Storage**: 100MB for scripts and dependencies

### Network Requirements
- **Internet access** for external scanning
- **Firewall configuration** for outbound connections
- **VPN support** for secure scanning

## 🏆 Essential Security Repositories

### 🔥 Must-Have Collections
- **[Awesome Hacking](https://github.com/Hack-with-Github/Awesome-Hacking)** - The ultimate curated list of hacking resources
- **[Awesome OSINT](https://github.com/jivoi/awesome-osint)** - OSINT tools and resources for intelligence gathering
- **[Awesome Pentest](https://github.com/enaqx/awesome-pentest)** - Penetration testing resources and tools
- **[Awesome Security](https://github.com/sbilly/awesome-security)** - General security resources and tools
- **[Awesome Bug Bounty](https://github.com/djadmin/awesome-bug-bounty)** - Bug bounty hunting resources and writeups

### 🛠️ Professional Tools
- **[Nmap](https://github.com/nmap/nmap)** - Network mapper and port scanner
- **[Metasploit](https://github.com/rapid7/metasploit-framework)** - Penetration testing framework
- **[Burp Suite](https://portswigger.net/burp)** - Web application security testing
- **[OWASP ZAP](https://github.com/zaproxy/zaproxy)** - Free web application security scanner
- **[SQLMap](https://github.com/sqlmapproject/sqlmap)** - Automatic SQL injection tool

### 🔍 OSINT & Reconnaissance
- **[theHarvester](https://github.com/laramies/theHarvester)** - Email, subdomain, and people names harvester
- **[Sherlock](https://github.com/sherlock-project/sherlock)** - Find usernames across social networks
- **[Recon-ng](https://github.com/lanmaster53/recon-ng)** - Modular web reconnaissance framework
- **[SpiderFoot](https://github.com/smicallef/spiderfoot)** - OSINT automation tool
- **[OSINT-SPY](https://github.com/SharadKumar97/OSINT-SPY)** - All-in-one OSINT tool
- **[Holehe](https://github.com/megadose/holehe)** - Check if email is attached to an account
- **[PhoneInfoga](https://github.com/sundowndev/phoneinfoga)** - Phone number OSINT reconnaissance

### 🌐 Web Security
- **[PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)** - Web application security payloads
- **[SecLists](https://github.com/danielmiessler/SecLists)** - Security testing wordlists and payloads
- **[FuzzDB](https://github.com/fuzzdb-project/fuzzdb)** - Attack patterns and resource database
- **[WSTG](https://github.com/OWASP/wstg)** - Web Security Testing Guide
- **[XSS Payloads](https://github.com/payloadbox/xss-payload-list)** - XSS attack payloads

### 🔐 Cryptography & Steganography
- **[John the Ripper](https://github.com/openwall/john)** - Password cracking tool
- **[Hashcat](https://github.com/hashcat/hashcat)** - Advanced password recovery
- **[Steghide](https://github.com/StefanoDeVuono/steghide)** - Steganography tool
- **[Cryptography](https://github.com/pyca/cryptography)** - Python cryptography library
- **[Fernet](https://github.com/fernet/spec)** - Symmetric encryption specification

### 🚀 Exploitation & Post-Exploitation
- **[Empire](https://github.com/EmpireProject/Empire)** - PowerShell and Python post-exploitation agent
- **[Cobalt Strike](https://www.cobaltstrike.com/)** - Commercial penetration testing framework
- **[Mimikatz](https://github.com/gentilkiwi/mimikatz)** - Windows credential extraction
- **[PowerSploit](https://github.com/PowerShellMafia/PowerSploit)** - PowerShell exploitation framework
- **[BloodHound](https://github.com/BloodHoundAD/BloodHound)** - Active Directory attack path analysis

### ☁️ Cloud Security
- **[Pacu](https://github.com/RhinoSecurityLabs/pacu)** - AWS exploitation framework
- **[CloudMapper](https://github.com/duo-labs/cloudmapper)** - Cloud security visualization
- **[Scout Suite](https://github.com/nccgroup/ScoutSuite)** - Multi-cloud security auditing
- **[CloudSploit](https://github.com/aquasecurity/cloudsploit)** - Cloud security posture management
- **[Prowler](https://github.com/toniblyx/prowler)** - AWS security best practices assessment

### 📱 Mobile Security
- **[MobSF](https://github.com/MobSF/Mobile-Security-Framework-MobSF)** - Mobile security testing framework
- **[Frida](https://github.com/frida/frida)** - Dynamic instrumentation toolkit
- **[Objection](https://github.com/sensepost/objection)** - Runtime mobile exploration
- **[iNalyzer](https://github.com/OWASP/iNalyzer)** - iOS security analysis
- **[QARK](https://github.com/linkedin/qark)** - Quick Android Review Kit

### 🔬 Malware Analysis
- **[Cuckoo Sandbox](https://github.com/cuckoosandbox/cuckoo)** - Automated malware analysis
- **[YARA](https://github.com/VirusTotal/yara)** - Pattern matching engine
- **[Capa](https://github.com/mandiant/capa)** - Capability analysis tool
- **[Ghidra](https://github.com/NationalSecurityAgency/ghidra)** - Software reverse engineering framework
- **[Radare2](https://github.com/radareorg/radare2)** - Reverse engineering framework

### 🎯 Specialized Tools
- **[Shodan](https://github.com/achillean/shodan-python)** - Internet-connected device search
- **[Censys](https://github.com/censys/censys-python)** - Internet scanning and search
- **[Masscan](https://github.com/robertdavidgraham/masscan)** - Ultra-fast port scanner
- **[Zmap](https://github.com/zmap/zmap)** - Fast network scanner
- **[Nuclei](https://github.com/projectdiscovery/nuclei)** - Vulnerability scanner

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Fork the repository
git clone https://github.com/your-username/security-scripts.git
cd security-scripts

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Learning Resources

### 📖 Essential Books
- **"The Web Application Hacker's Handbook"** by Dafydd Stuttard - Web security fundamentals
- **"Black Hat Python"** by Justin Seitz - Python for security professionals
- **"Metasploit: The Penetration Tester's Guide"** by David Kennedy - Exploitation framework
- **"OSINT Techniques"** by Michael Bazzell - Open source intelligence gathering

### 🎓 Online Learning Platforms
- **[TryHackMe](https://tryhackme.com/)** - Hands-on cybersecurity learning
- **[HackTheBox](https://www.hackthebox.eu/)** - Penetration testing practice
- **[Cybrary](https://www.cybrary.it/)** - Free cybersecurity courses
- **[OverTheWire](https://overthewire.org/)** - Wargames for learning

### 🎥 YouTube Channels
- **[LiveOverflow](https://www.youtube.com/c/LiveOverflow)** - Security research and tutorials
- **[IppSec](https://www.youtube.com/c/ippsec)** - HackTheBox walkthroughs
- **[John Hammond](https://www.youtube.com/c/JohnHammond010)** - Cybersecurity content
- **[NetworkChuck](https://www.youtube.com/c/NetworkChuck)** - Networking and security

### 🔧 Essential GitHub Repositories
- **[Awesome Hacking](https://github.com/Hack-with-Github/Awesome-Hacking)** - Ultimate hacking resources
- **[Awesome OSINT](https://github.com/jivoi/awesome-osint)** - OSINT tools and resources
- **[Awesome Pentest](https://github.com/enaqx/awesome-pentest)** - Penetration testing resources
- **[PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)** - Web application security payloads

## ⚠️ Legal & Ethical Guidelines

### 🚨 IMPORTANT DISCLAIMERS
- **ONLY test systems you own or have explicit permission to test**
- **Never use these tools for malicious purposes**
- **Always follow applicable laws and regulations**
- **Respect privacy and data protection laws**
- **Use responsible disclosure for vulnerabilities**

### 📋 Best Practices
1. **Get Written Permission** - Always obtain explicit authorization
2. **Document Everything** - Keep detailed logs of all activities
3. **Stay Legal** - Understand and comply with local laws
4. **Ethical Conduct** - Use skills to protect, not harm
5. **Continuous Learning** - Stay updated with latest techniques and laws

## 📞 Contact

- **GitHub**: [@safouanb](https://github.com/safouanb)
- **Email**: [Your Email]
- **LinkedIn**: [Your LinkedIn]

## 🙏 Acknowledgments

- Security community for inspiration and feedback
- Open source projects that made this possible
- Contributors and testers

---

## 🔥 Pro Tips

1. **Start with the basics** - Don't rush into advanced topics
2. **Practice regularly** - Use platforms like TryHackMe and HackTheBox
3. **Join communities** - Connect with other security professionals
4. **Stay curious** - The field is constantly evolving
5. **Document everything** - Keep a lab notebook of your learning
6. **Build your lab** - Set up a home lab for safe practice
7. **Follow responsible disclosure** - Report vulnerabilities ethically
8. **Stay legal** - Always get proper authorization before testing

**Remember: With great power comes great responsibility. Use your skills ethically and legally!**

---

**⭐ Star this repository if you find it useful!**

[![GitHub stars](https://img.shields.io/github/stars/safouanb/security-scripts?style=social)](https://github.com/safouanb/security-scripts/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/safouanb/security-scripts?style=social)](https://github.com/safouanb/security-scripts/network)

*Happy Hacking! 🚀*
