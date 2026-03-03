# Password Security Audit Report
**Date Generated:** 2026-03-03 00:05:58

## 1. Executive Summary
Total Passwords Analyzed: **4**
- Strong Passwords (Score 3-4): **1**
- Weak Passwords (Score 0-2): **3**

## 2. Detailed Findings

| Password (Masked) | Zxcvbn Score | Entropy (bits) | Est. Crack Time | Recommendations |
|---|---|---|---|---|
| `pa********3` | 0/4 | 56.87 | less than a second | Add another word or two. Uncommon words are better. |
| `ad**n` | 0/4 | 23.5 | less than a second | Add another word or two. Uncommon words are better. |
| `P@**********!` | 2/4 | 85.21 | less than a second | Add another word or two. Uncommon words are better. Capitalization doesn't help very much. Predictable substitutions like '@' instead of 'a' don't help very much. |
| `co*************************e` | 4/4 | 131.61 | centuries | None |

## 3. Recommended Password Policies
- Enforce a minimum length of 12-16 characters.
- Reject passwords found in common dictionaries or have been previously breached.
- Do not rely solely on naive complexity requirements (e.g. 1 upper, 1 lower, 1 symbol) if the base word is common (e.g. `Password123!`).
- Implement rate limiting and account lockouts to prevent online brute-force attacks.