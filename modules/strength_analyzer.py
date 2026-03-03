import zxcvbn
import string
import math
from typing import Dict, Any

class PasswordStrengthAnalyzer:
    def __init__(self):
        pass

    def analyze(self, password: str) -> Dict[str, Any]:
        """
        Analyze the password using zxcvbn for entropy/predictability,
        and calculate standard complexity rules.
        """
        # Dictionary-based and predictability analysis via zxcvbn
        zxcvbn_results = zxcvbn.zxcvbn(password)
        
        # Base complexity checks
        complexity = self._check_complexity(password)
        
        # Calculate mathematical entropy based on character sets
        math_entropy = self._calculate_shannon_entropy(password)

        return {
            "password": password,
            "score": zxcvbn_results['score'],  # 0-4 score
            "guesses_log10": zxcvbn_results['guesses_log10'],
            "crack_times_display": zxcvbn_results['crack_times_display'],
            "feedback": zxcvbn_results['feedback'],
            "complexity_met": complexity['met_requirements'],
            "complexity_details": complexity['details'],
            "math_entropy_bits": math_entropy
        }

    def _check_complexity(self, password: str) -> Dict[str, Any]:
        """Check traditional complexity requirements."""
        details = {
            "length": len(password) >= 8,
            "uppercase": any(c.isupper() for c in password),
            "lowercase": any(c.islower() for c in password),
            "numbers": any(c.isdigit() for c in password),
            "symbols": any(c in string.punctuation for c in password),
        }
        
        met_requirements = all(details.values())
        return {
            "met_requirements": met_requirements,
            "details": details
        }

    def _calculate_shannon_entropy(self, password: str) -> float:
        """Calculate the theoretical Shannon entropy for the password based on its character set."""
        if not password:
            return 0.0
            
        charset_size = 0
        if any(c.islower() for c in password): charset_size += 26
        if any(c.isupper() for c in password): charset_size += 26
        if any(c.isdigit() for c in password): charset_size += 10
        if any(c in string.punctuation for c in password): charset_size += 32
        
        if charset_size == 0:
            return 0.0
            
        entropy = len(password) * math.log2(charset_size)
        return round(entropy, 2)

    def generate_recommendations(self, analysis_result: Dict[str, Any]) -> list[str]:
        """Generate actionable recommendations based on the analysis."""
        recommendations = []
        feedback = analysis_result.get('feedback', {})
        
        if feedback.get('warning'):
            recommendations.append(f"Warning: {feedback['warning']}")
            
        for suggestion in feedback.get('suggestions', []):
            recommendations.append(suggestion)
            
        comp_details = analysis_result.get('complexity_details', {})
        if not comp_details.get('length'):
            recommendations.append("Increase password length to at least 8 characters.")
        if not comp_details.get('uppercase'):
            recommendations.append("Add uppercase letters.")
        if not comp_details.get('numbers'):
            recommendations.append("Add numbers.")
        if not comp_details.get('symbols'):
            recommendations.append("Add special characters or symbols.")
            
        if not recommendations and analysis_result['score'] < 3:
            recommendations.append("Consider using a randomly generated password or a longer passphrase.")
            
        return recommendations
