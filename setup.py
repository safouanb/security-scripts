#!/usr/bin/env python3
"""
Security Scripts - Setup Configuration
Author: Safouan Benali
License: MIT
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="security-scripts",
    version="1.0.0",
    author="Safouan Benali",
    author_email="your.email@example.com",
    description="A curated collection of security-focused Python scripts for penetration testing and security automation",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/safouanb/security-scripts",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: Security",
        "Topic :: System :: Networking",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.2.0",
            "pytest-cov>=4.0.0",
            "black>=22.12.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "advanced": [
            "scapy>=2.4.5",
            "python-nmap>=0.7.1",
            "selenium>=4.8.0",
            "playwright>=1.30.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ssl-check=scripts.network.ssl_check:main",
            "port-scan=scripts.network.port_scanner:main",
            "sql-test=scripts.web.sql_injection_tester:main",
            "hash-gen=scripts.crypto.hash_generator:main",
            "security-report=scripts.automation.security_report_generator:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.json", "*.yaml", "*.yml"],
    },
    keywords="security, penetration-testing, vulnerability-assessment, network-security, web-security, cryptography, automation",
    project_urls={
        "Bug Reports": "https://github.com/safouanb/security-scripts/issues",
        "Source": "https://github.com/safouanb/security-scripts",
        "Documentation": "https://github.com/safouanb/security-scripts/blob/main/docs/",
    },
)
