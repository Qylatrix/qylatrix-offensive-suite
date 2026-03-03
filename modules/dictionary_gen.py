import itertools
from typing import List, Set

class DictionaryGenerator:
    def __init__(self):
        self.leet_map = {
            'a': ['a', '@', '4'],
            'e': ['e', '3'],
            'i': ['i', '1', '!'],
            'o': ['o', '0'],
            's': ['s', '$', '5'],
            't': ['t', '7'],
            'l': ['l', '1']
        }
        
    def generate_base_words(self, inputs: List[str]) -> Set[str]:
        """Generate base combinations from inputs like names & dob."""
        results = set(inputs)
        
        # Combinations of 2 components
        for comb in itertools.permutations(inputs, 2):
            results.add("".join(comb))
            results.add("_".join(comb))
            results.add("-".join(comb))
            
        return results

    def apply_mutations(self, base_words: Set[str], append_numbers: bool = True, leetspeak: bool = True) -> Set[str]:
        """Apply various mutation rules to a set of words."""
        mutated_words = set(base_words)
        
        for word in base_words:
            # Case variations
            mutated_words.add(word.lower())
            mutated_words.add(word.upper())
            mutated_words.add(word.capitalize())
            
            # Common appended numbers
            if append_numbers:
                suffixes = ['123', '1234', '1!', '!', '2023', '2024', '69', '99']
                for suffix in suffixes:
                    mutated_words.add(word + suffix)
                    mutated_words.add(word.capitalize() + suffix)
            
            # Leet-speak mutations (basic generator)
            if leetspeak:
                leet_vars = self._generate_leet_variations(word)
                mutated_words.update(leet_vars)
                
        return mutated_words
        
    def _generate_leet_variations(self, word: str) -> List[str]:
        """Generate common leet-speak variations for a given word."""
        options = []
        for char in word.lower():
            if char in self.leet_map:
                options.append(self.leet_map[char])
            else:
                options.append([char])
                
        # Generate all combinations
        variations = []
        for combo in itertools.product(*options):
            variations.append("".join(combo))
        
        return variations

    def export_wordlist(self, words: Set[str], filename: str):
        """Export the generated wordlist to a file."""
        with open(filename, 'w') as f:
            for word in sorted(words):
                f.write(word + "\n")
        return len(words)
