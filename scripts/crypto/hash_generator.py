#!/usr/bin/env python3
"""
Hash Generator - Multiple hash algorithm support
Author: Safouan Benali
License: MIT
"""

import hashlib
import argparse
import sys
from typing import Dict, List

class HashGenerator:
    """Generate hashes using multiple algorithms."""
    
    def __init__(self):
        self.algorithms = {
            'md5': hashlib.md5,
            'sha1': hashlib.sha1,
            'sha256': hashlib.sha256,
            'sha512': hashlib.sha512,
            'blake2b': hashlib.blake2b,
            'blake2s': hashlib.blake2s
        }
    
    def generate_hash(self, data: str, algorithm: str) -> str:
        """Generate hash for given data and algorithm."""
        if algorithm not in self.algorithms:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
        
        hash_obj = self.algorithms[algorithm]()
        hash_obj.update(data.encode('utf-8'))
        return hash_obj.hexdigest()
    
    def generate_all_hashes(self, data: str) -> Dict[str, str]:
        """Generate hashes using all supported algorithms."""
        results = {}
        for algorithm in self.algorithms:
            try:
                results[algorithm] = self.generate_hash(data, algorithm)
            except Exception as e:
                results[algorithm] = f"Error: {str(e)}"
        return results
    
    def verify_hash(self, data: str, hash_value: str, algorithm: str) -> bool:
        """Verify if hash matches the data."""
        try:
            generated_hash = self.generate_hash(data, algorithm)
            return generated_hash.lower() == hash_value.lower()
        except Exception:
            return False

def main():
    parser = argparse.ArgumentParser(description='Hash Generator')
    parser.add_argument('data', help='Data to hash')
    parser.add_argument('-a', '--algorithm', default='sha256', 
                       choices=['md5', 'sha1', 'sha256', 'sha512', 'blake2b', 'blake2s'],
                       help='Hash algorithm to use')
    parser.add_argument('--all', action='store_true', help='Generate all hash types')
    parser.add_argument('--verify', help='Verify hash against data')
    parser.add_argument('-f', '--file', help='Read data from file')
    
    args = parser.parse_args()
    
    generator = HashGenerator()
    
    # Read data from file if specified
    if args.file:
        try:
            with open(args.file, 'rb') as f:
                data = f.read().decode('utf-8')
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)
    else:
        data = args.data
    
    if args.verify:
        # Verify mode
        is_valid = generator.verify_hash(data, args.verify, args.algorithm)
        print(f"Hash verification: {'✓ Valid' if is_valid else '✗ Invalid'}")
    elif args.all:
        # Generate all hashes
        results = generator.generate_all_hashes(data)
        print(f"Hash results for: {data[:50]}{'...' if len(data) > 50 else ''}")
        print("-" * 60)
        for algorithm, hash_value in results.items():
            print(f"{algorithm.upper():>8}: {hash_value}")
    else:
        # Generate single hash
        try:
            hash_value = generator.generate_hash(data, args.algorithm)
            print(f"{args.algorithm.upper()}: {hash_value}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
