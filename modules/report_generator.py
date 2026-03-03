import os
from datetime import datetime
from typing import Dict, Any, List

class ReportGenerator:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def generate_audit_report(self, analysis_results: List[Dict[str, Any]], filename: str = None) -> str:
        """
        Generates a comprehensive Markdown audit report from password analysis results.
        """
        if filename is None:
            filename = f"password_audit_report_{self.timestamp}.md"
            
        weak_count = sum(1 for res in analysis_results if res['score'] < 3)
        strong_count = len(analysis_results) - weak_count
        
        report_lines = [
            "# Password Security Audit Report",
            f"**Date Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 1. Executive Summary",
            f"Total Passwords Analyzed: **{len(analysis_results)}**",
            f"- Strong Passwords (Score 3-4): **{strong_count}**",
            f"- Weak Passwords (Score 0-2): **{weak_count}**",
            "",
            "## 2. Detailed Findings",
            ""
        ]
        
        # Add table header
        report_lines.append("| Password (Masked) | Zxcvbn Score | Entropy (bits) | Est. Crack Time | Recommendations |")
        report_lines.append("|---|---|---|---|---|")
        
        for res in analysis_results:
            pwd = res['password']
            # Mask password for report
            if len(pwd) > 3:
                masked = pwd[:2] + "*" * (len(pwd)-3) + pwd[-1]
            else:
                masked = "***"
                
            score = res['score']
            entropy = res['math_entropy_bits']
            crack_time = res['crack_times_display'].get('offline_fast_hashing_1e10_per_second', 'Unknown')
            
            # Formulate short recommendations
            recs = " ".join([s for s in res.get('feedback', {}).get('suggestions', [])])
            if not recs:
                 recs = "None"
                 
            report_lines.append(f"| `{masked}` | {score}/4 | {entropy} | {crack_time} | {recs} |")
            
        report_lines.extend([
            "",
            "## 3. Recommended Password Policies",
            "- Enforce a minimum length of 12-16 characters.",
            "- Reject passwords found in common dictionaries or have been previously breached.",
            "- Do not rely solely on naive complexity requirements (e.g. 1 upper, 1 lower, 1 symbol) if the base word is common (e.g. `Password123!`).",
            "- Implement rate limiting and account lockouts to prevent online brute-force attacks."
        ])
        
        report_content = "\n".join(report_lines)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_content)
            
        return filename
