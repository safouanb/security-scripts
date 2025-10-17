#!/usr/bin/env python3
"""
Test SSL Check Script
Author: Safouan Benali
License: MIT
"""

import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock

# Add the scripts directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts', 'network'))

from ssl_check import parse_and_output

class TestSSLCheck(unittest.TestCase):
    """Test cases for SSL check functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_host = "example.com"
    
    @patch('ssl_check.run_openssl')
    def test_valid_ssl_certificate(self, mock_run_openssl):
        """Test SSL check with valid certificate."""
        # Mock valid SSL response
        mock_run_openssl.return_value = """
        CONNECTED(00000003)
        depth=2 C = US, O = DigiCert Inc, OU = www.digicert.com, CN = DigiCert Global Root CA
        verify return:1
        depth=1 C = US, O = DigiCert Inc, CN = DigiCert SHA2 High Assurance Server CA
        verify return:1
        depth=0 C = US, ST = California, L = San Francisco, O = GitHub, Inc., CN = github.com
        verify return:1
        Verify return code: 0 (ok)
        """
        
        # Capture output
        import io
        from contextlib import redirect_stdout
        
        f = io.StringIO()
        with redirect_stdout(f):
            parse_and_output(self.test_host)
        
        output = f.getvalue()
        result = json.loads(output)
        
        # Assertions
        self.assertEqual(result['host'], self.test_host)
        self.assertTrue(result['valid_chain'])
        self.assertIn('Verify return code: 0 (ok)', result['snippet'])
    
    @patch('ssl_check.run_openssl')
    def test_invalid_ssl_certificate(self, mock_run_openssl):
        """Test SSL check with invalid certificate."""
        # Mock invalid SSL response
        mock_run_openssl.return_value = """
        CONNECTED(00000003)
        depth=0 C = US, ST = California, L = San Francisco, O = GitHub, Inc., CN = github.com
        verify error:num=20:unable to get local issuer certificate
        verify return:1
        Verify return code: 20 (unable to get local issuer certificate)
        """
        
        # Capture output
        import io
        from contextlib import redirect_stdout
        
        f = io.StringIO()
        with redirect_stdout(f):
            parse_and_output(self.test_host)
        
        output = f.getvalue()
        result = json.loads(output)
        
        # Assertions
        self.assertEqual(result['host'], self.test_host)
        self.assertFalse(result['valid_chain'])
        self.assertIn('Verify return code: 20', result['snippet'])
    
    def test_ssl_check_output_format(self):
        """Test that SSL check output is valid JSON."""
        # This test ensures the output format is consistent
        expected_keys = ['host', 'valid_chain', 'snippet']
        
        # Mock the openssl call
        with patch('ssl_check.run_openssl') as mock_run_openssl:
            mock_run_openssl.return_value = "Verify return code: 0 (ok)"
            
            import io
            from contextlib import redirect_stdout
            
            f = io.StringIO()
            with redirect_stdout(f):
                parse_and_output(self.test_host)
            
            output = f.getvalue()
            result = json.loads(output)
            
            # Check all expected keys are present
            for key in expected_keys:
                self.assertIn(key, result)
            
            # Check data types
            self.assertIsInstance(result['host'], str)
            self.assertIsInstance(result['valid_chain'], bool)
            self.assertIsInstance(result['snippet'], str)

if __name__ == '__main__':
    unittest.main()
