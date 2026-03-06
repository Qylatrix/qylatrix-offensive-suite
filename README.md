# qylxforce — Qylatrix Offensive Credential Suite

> **The Syntax of Safety** | A premium credential security assessment toolkit for ethical security research.

---

## 🛡️ What is qylxforce?

**qylxforce** is a unique, Kali Linux–native offensive credential suite built by Qylatrix Industries. It combines password policy testing, entropy analysis, brute-force modelling, hash extraction simulation, and executive reporting into a single professional-grade toolkit.

---

## 🔧 Installation on Kali Linux

### One-line install (recommended)

```bash
curl -sSL https://raw.githubusercontent.com/Qylatrix/qylatrix-offensive-suite/main/install.sh | sudo bash
```

### Manual install

```bash
git clone https://github.com/Qylatrix/qylatrix-offensive-suite
cd qylatrix-offensive-suite
sudo bash install.sh
```

After installation, run anywhere:

```bash
qylxforce
```

---

## 🚀 Usage

| Command | Description |
|---|---|
| `qylxforce web` | Launch premium web UI at `http://localhost:5000` |
| `qylxforce dict` | Dictionary generator — wordlist synthesis |
| `qylxforce analyze` | Entropy analyzer — password strength audit |
| `qylxforce brute` | Brute-force time estimator |
| `qylxforce extract` | Credential hash extractor (shadow / SAM) |
| `qylxforce report` | Executive audit report generator |

### Examples

```bash
# Launch the full web interface
qylxforce web

# Analyze a password from terminal
qylxforce analyze --password 'Admin@2024!'

# Generate a wordlist from base words
qylxforce dict --words alice,company,winter2024

# Generate executive audit report
qylxforce report --file passwords.txt
```

---

## 📦 Modules

| # | Module | Description |
|---|---|---|
| 01 | **Dictionary Forge** | L33tspeak, CamelCase, digit-suffix mutations |
| 02 | **Entropy Analyzer** | Shannon entropy, zxcvbn score, crack-time estimation |
| 03 | **Brute-Force Matrix** | ASIC/GPU attack surface modelling |
| 04 | **Hive Extraction** | Linux shadow / Windows SAM dump simulation |
| 05 | **Audit Report** | Executive security brief with remediation guidance |

---

## 📋 Requirements

- Kali Linux 2023+ / Debian 11+ / Ubuntu 22+
- Python 3.10+
- Internet connection (for install)

---

## ⚠️ Disclaimer

This tool is for **educational and authorized security testing purposes only**. Unauthorized use against systems you do not own or have explicit permission to test is illegal. The authors assume no liability.

---

## 🔗 Links

- GitHub: [Qylatrix/qylatrix-offensive-suite](https://github.com/Qylatrix/qylatrix-offensive-suite)
- Author: Qylatrix Industries
- License: MIT
