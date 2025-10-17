# Contributing to Security Scripts

Thank you for your interest in contributing to the Security Scripts project! This document provides guidelines for contributing to the repository.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Basic understanding of security concepts

### Development Setup
```bash
# Fork and clone the repository
git clone https://github.com/your-username/security-scripts.git
cd security-scripts

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

## 📝 Contribution Guidelines

### Code Style
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions small and focused

### Security Considerations
- **Never include real credentials or sensitive data**
- **Always validate user input**
- **Use secure coding practices**
- **Include proper error handling**
- **Add rate limiting where appropriate**

### Script Requirements
- Include proper argument parsing
- Add comprehensive error handling
- Include usage examples in docstrings
- Add logging for important operations
- Include legal disclaimers

## 🛠️ Development Process

### 1. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes
- Write clean, well-documented code
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes
```bash
# Run tests
python -m pytest tests/

# Check code style
flake8 scripts/
black scripts/

# Test your script
python scripts/your_script.py --help
```

### 4. Commit Your Changes
```bash
git add .
git commit -m "Add: Brief description of your changes"
```

### 5. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

## 📋 Pull Request Guidelines

### Before Submitting
- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] No sensitive data is included
- [ ] Script includes proper error handling
- [ ] Legal disclaimers are included

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Security improvement

## Testing
- [ ] Tested on multiple platforms
- [ ] Added unit tests
- [ ] Manual testing completed

## Security Considerations
- [ ] No sensitive data exposed
- [ ] Input validation implemented
- [ ] Error handling added
- [ ] Rate limiting considered
```

## 🧪 Testing Guidelines

### Unit Tests
- Write tests for all new functions
- Test edge cases and error conditions
- Aim for high code coverage

### Integration Tests
- Test scripts with real (safe) targets
- Verify output formats
- Test error handling

### Security Testing
- Test with malicious inputs
- Verify no sensitive data leakage
- Test rate limiting functionality

## 📚 Documentation Standards

### Script Documentation
Each script should include:
- Purpose and functionality
- Usage examples
- Parameter descriptions
- Security considerations
- Legal disclaimers

### Example Script Header
```python
#!/usr/bin/env python3
"""
Script Name - Brief description
Author: Your Name
License: MIT

Description:
    Detailed description of what the script does.

Usage:
    python script_name.py [options]

Security Considerations:
    - Only use on authorized targets
    - Respect rate limits
    - Follow responsible disclosure

Legal Disclaimer:
    This script is for educational and authorized testing only.
    Use only on systems you own or have permission to test.
"""
```

## 🔒 Security Guidelines

### Safe Practices
- Always validate input parameters
- Use parameterized queries for database operations
- Implement proper error handling
- Add rate limiting to prevent abuse
- Include legal disclaimers

### Prohibited Content
- Real credentials or API keys
- Malicious payloads without context
- Tools designed for illegal activities
- Scripts that could cause damage

## 🐛 Bug Reports

When reporting bugs, please include:
- Description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)
- Error messages or logs

## 💡 Feature Requests

When suggesting features:
- Describe the use case
- Explain the security benefit
- Provide implementation ideas
- Consider backward compatibility

## 📞 Getting Help

- Open an issue for questions
- Join discussions in the repository
- Check existing documentation
- Review similar scripts for examples

## 🏆 Recognition

Contributors will be:
- Listed in the README
- Mentioned in release notes
- Credited in script headers
- Invited to maintainer discussions

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Security Scripts! 🚀
