import time
import itertools
import string
import hashlib
from typing import Dict, Any, Optional

class BruteForceSimulator:
    def __init__(self):
        # Simulated hash rates (hashes per second) for demonstration
        self.assumed_hash_rates = {
            'md5': 100_000_000_000,        # 100 Billion h/s (e.g., modern GPU)
            'sha512': 1_500_000_000,       # 1.5 Billion h/s
            'ntlm': 150_000_000_000,       # 150 Billion h/s
            'bcrypt': 100_000              # 100 k/s (depends on work factor, very slow)
        }

    def simulate_dictionary_attack(self, target_hash: str, wordlist_path: str, hash_type: str = 'md5') -> Dict[str, Any]:
        """
        Simulate a dictionary attack. In reality, it compares hashes.
        For this simulation, if the hash type matches a simple implementation, we test it.
        """
        start_time = time.time()
        attempts = 0
        found_password = None
        
        try:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    attempts += 1
                    word = line.strip()
                    
                    # Basic simulation for md5 to prove it works
                    if hash_type == 'md5':
                        hashed_word = hashlib.md5(word.encode()).hexdigest()
                        if hashed_word == target_hash:
                            found_password = word
                            break
                    elif hash_type == 'sha256':
                        hashed_word = hashlib.sha256(word.encode()).hexdigest()
                        if hashed_word == target_hash:
                            found_password = word
                            break
                            
        except FileNotFoundError:
            return {"error": f"Wordlist not found: {wordlist_path}"}
            
        elapsed_time = time.time() - start_time
        
        return {
            "attack_type": "dictionary",
            "success": found_password is not None,
            "password": found_password,
            "attempts": attempts,
            "time_taken_seconds": elapsed_time,
            "hashes_per_second": attempts / elapsed_time if elapsed_time > 0 else 0
        }

    def estimate_brute_force_time(self, password: str, charset: str = 'all', hash_type: str = 'ntlm') -> Dict[str, Any]:
        """
        Calculate the theoretical time to brute-force a password.
        """
        length = len(password)
        
        # Determine character set size
        charset_size = 0
        if charset == 'numeric' or password.isdigit():
            charset_size = 10
        elif charset == 'alpha' or password.isalpha():
            charset_size = 52 # upper + lower
        elif charset == 'alphanumeric' or password.isalnum():
            charset_size = 62
        else:
            charset_size = 94 # all printable ASCII
            
        # Total possible combinations for exactly this length
        combinations = charset_size ** length
        
        hash_rate = self.assumed_hash_rates.get(hash_type, 1_000_000)
        
        seconds = combinations / hash_rate
        
        # Format time nicely
        time_str = self._format_time(seconds)
        
        return {
            "password": password,
            "length": length,
            "combinations": combinations,
            "hash_type": hash_type,
            "assumed_hash_rate": hash_rate,
            "estimated_seconds": seconds,
            "formatted_time": time_str
        }

    def _format_time(self, seconds: float) -> str:
        """Format seconds into readable time string."""
        if seconds < 1:
            return "Instant (Less than 1 second)"
        elif seconds < 60:
            return f"{seconds:.2f} seconds"
        elif seconds < 3600:
            return f"{seconds/60:.2f} minutes"
        elif seconds < 86400:
            return f"{seconds/3600:.2f} hours"
        elif seconds < 31536000:
            return f"{seconds/86400:.2f} days"
        elif seconds < 3153600000:
            return f"{seconds/31536000:.2f} years"
        else:
            return "Centuries (Offline cracking infeasible)"
