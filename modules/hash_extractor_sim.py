import re
from typing import List, Dict, Any, Optional

class HashExtractorSim:
    def __init__(self):
        # Common hash types and their characteristics for identification
        self.algorithms = {
            '$1$': 'MD5-Crypt',
            '$2a$': 'Bcrypt',
            '$2y$': 'Bcrypt',
            '$5$': 'SHA-256 Crypt',
            '$6$': 'SHA-512 Crypt',
            '$y$': 'Yescrypt'
        }

    def parse_linux_shadow(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Parses a standard Linux /etc/shadow or simulated shadow file.
        Returns extracted users and their hashes.
        """
        extracted_accounts = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                        
                    parts = line.split(':')
                    if len(parts) >= 2:
                        username = parts[0]
                        hash_str = parts[1]
                        
                        alg = self.identify_linux_algorithm(hash_str)
                        
                        # Only include valid hash strings, skip lock accounts
                        if alg != 'Unknown' and not hash_str in ['*', '!', '!!']:
                            extracted_accounts.append({
                                'username': username,
                                'hash_string': hash_str,
                                'algorithm': alg,
                                'type': 'Linux Shadow'
                            })
                            
        except FileNotFoundError:
             extracted_accounts.append({"error": f"File not found: {file_path}"})
             
        return extracted_accounts

    def parse_windows_sam_dump(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Parses a simulated output from tools dumping Windows SAM (e.g., pwdump/secretsdump format).
        Format: username:RID:LM_HASH:NTLM_HASH:::
        """
        extracted_accounts = []
        try:
             with open(file_path, 'r', encoding='utf-8') as f:
                 for line in f:
                     line = line.strip()
                     if not line or line.startswith('#'):
                         continue
                         
                     # User:SID:LM:NTLM:::
                     parts = line.split(':')
                     if len(parts) >= 4:
                         username = parts[0]
                         ntlm_hash = parts[3]
                         
                         if ntlm_hash and ntlm_hash != "31d6cfe0d16ae931b73c59d7e0c089c0": # empty string NTLM
                             extracted_accounts.append({
                                 'username': username,
                                 'hash_string': ntlm_hash,
                                 'algorithm': 'NTLM',
                                 'type': 'Windows SAM'
                             })
        except FileNotFoundError:
            extracted_accounts.append({"error": f"File not found: {file_path}"})
            
        return extracted_accounts

    def identify_linux_algorithm(self, hash_str: str) -> str:
        """Helper to identify the hash type from standard Linux prefix indicators."""
        if not hash_str or len(hash_str) < 3:
            return 'None/Disabled'
            
        if hash_str.startswith('$'):
            prefix = hash_str[:3]
            if len(hash_str) >= 4 and hash_str[3] == '$': 
                prefix = hash_str[:4]
                
            return self.algorithms.get(prefix, 'Unknown Crypt Format')
            
        return 'Unknown'
