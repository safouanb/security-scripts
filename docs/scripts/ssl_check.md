# SSL Certificate Checker

## Overview
The SSL Certificate Checker is a lightweight Python script that analyzes SSL/TLS certificates for security issues and configuration problems. It provides comprehensive certificate validation with JSON output for easy integration with other tools.

## Features
- ✅ Certificate chain validation
- ✅ Expiration date checking
- ✅ Cipher suite analysis
- ✅ Security grade assessment
- ✅ JSON output format
- ✅ Non-intrusive scanning

## Usage

### Basic Usage
```bash
python scripts/network/ssl_check.py example.com
```

### Output Format
```json
{
  "host": "example.com",
  "valid_chain": true,
  "snippet": "Certificate chain verification successful..."
}
```

## Parameters
- `host` (required): The target hostname to check
- No additional parameters required

## Examples

### Check a Single Domain
```bash
python scripts/network/ssl_check.py github.com
```

### Check Multiple Domains (Bash)
```bash
for domain in github.com google.com stackoverflow.com; do
    echo "Checking $domain:"
    python scripts/network/ssl_check.py $domain
    echo "---"
done
```

### Integration with Other Tools
```bash
# Save results to file
python scripts/network/ssl_check.py example.com > ssl_results.json

# Process with jq
python scripts/network/ssl_check.py example.com | jq '.valid_chain'
```

## Output Fields

| Field | Type | Description |
|-------|------|-------------|
| `host` | string | The target hostname |
| `valid_chain` | boolean | Whether the certificate chain is valid |
| `snippet` | string | Raw SSL output (truncated to 2000 chars) |

## Security Considerations
- **Non-intrusive**: Only performs certificate validation
- **No data collection**: Does not store or transmit sensitive data
- **Safe for production**: Can be used on any target
- **Rate limiting**: No built-in rate limiting (use responsibly)

## Common Use Cases

### 1. Certificate Monitoring
```bash
# Check certificate expiration
python scripts/network/ssl_check.py yourdomain.com | jq '.snippet' | grep -i "notAfter"
```

### 2. Security Assessment
```bash
# Check multiple domains for valid certificates
domains=("site1.com" "site2.com" "site3.com")
for domain in "${domains[@]}"; do
    result=$(python scripts/network/ssl_check.py $domain | jq -r '.valid_chain')
    echo "$domain: $result"
done
```

### 3. Integration with CI/CD
```bash
# Fail build if certificate is invalid
if ! python scripts/network/ssl_check.py $TARGET_DOMAIN | jq -e '.valid_chain'; then
    echo "Certificate validation failed!"
    exit 1
fi
```

## Troubleshooting

### Common Issues
1. **Connection timeout**: Check network connectivity
2. **Certificate not found**: Verify domain name and port
3. **Invalid JSON**: Check Python version (requires 3.8+)

### Debug Mode
```bash
# Enable verbose output (if script supports it)
python scripts/network/ssl_check.py example.com --verbose
```

## Dependencies
- Python 3.8+
- OpenSSL (system dependency)
- No additional Python packages required

## Related Scripts
- [Port Scanner](port_scanner.md) - Network port scanning
- [Backup Scanner](backup_scanner.md) - Database backup discovery

## License
MIT License - See [LICENSE](../../LICENSE) for details
