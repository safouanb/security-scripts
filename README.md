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

### 🔐 Cryptographic Tools
- **Hash Generator** - Multiple hash algorithm support

### 🤖 Automation Scripts
- **Security Report Generator** - Automated security reporting
- **Repository Summary** - Repository statistics and capabilities

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
| Web Security | 5 | ✅ Active |
| Cryptographic | 1 | ✅ Active |
| Automation | 2 | ✅ Active |
| **Total** | **11** | **✅ All Working** |

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

## 🎓 Learning Path

### 🥉 Beginner (0-6 months)
1. **Linux Fundamentals** - Master command line and basic system administration
2. **Networking Basics** - Understand TCP/IP, protocols, and network architecture
3. **Web Technologies** - HTML, CSS, JavaScript, and web application basics
4. **Basic Tools** - Nmap, Wireshark, Burp Suite Community
5. **Scripting** - Python, Bash for automation

### 🥈 Intermediate (6-18 months)
1. **Advanced Networking** - Deep dive into protocols and network security
2. **Web Application Security** - OWASP Top 10, injection attacks, authentication bypass
3. **Vulnerability Assessment** - Manual and automated testing
4. **API Security** - REST/GraphQL security testing
5. **Cryptography** - Hash functions, encryption, digital signatures

### 🥇 Advanced (18+ months)
1. **Exploit Development** - Buffer overflows, ROP, shellcode
2. **Advanced OSINT** - Deep web, dark web, advanced techniques
3. **Red Team Operations** - Full-spectrum attack simulation
4. **Malware Analysis** - Reverse engineering and threat hunting
5. **Cloud Security** - AWS, Azure, GCP security assessment

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
