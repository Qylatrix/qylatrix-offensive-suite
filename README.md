<div align="center">

<img src="static/logo.png" height="80"/>

# QYLXFORCE
### Offensive Credential Suite
**by [Qylatrix Industries](https://github.com/Qylatrix)**

🌐 **Live Site:** [qylxforce.pythonanywhere.com](https://qylxforce.pythonanywhere.com)

---

</div>

## ⚡ Install on Kali Linux

### One-line install
```bash
curl -sSL https://raw.githubusercontent.com/Qylatrix/qylatrix-offensive-suite/main/install.sh | sudo bash
```
That's it. After install the **browser opens the live site automatically.**

### Manual install
```bash
git clone https://github.com/Qylatrix/qylatrix-offensive-suite.git
cd qylatrix-offensive-suite
sudo bash install.sh
```

---

## 🚀 How to Use

After installing, run from any terminal:

| Command | What it does |
|---|---|
| `qylxforce` | Show banner + all commands |
| `qylxforce web` | Run the full web UI locally at `localhost:5000` |
| `qylxforce online` | Open the live site in browser |
| `qylxforce dict` | Dictionary / wordlist generator |
| `qylxforce analyze` | Password entropy analyzer |
| `qylxforce brute` | Brute-force time estimator |
| `qylxforce extract` | Hash extractor (Linux shadow / Windows SAM) |
| `qylxforce report` | Generate executive audit report |

### Examples
```bash
# Launch full web interface
qylxforce web

# Analyze a password
qylxforce analyze --password 'Admin@2024!'

# Generate wordlist
qylxforce dict --words alice,company,winter2024

# Open live site
qylxforce online
```

---

## 📦 Modules

| # | Module | Description |
|---|---|---|
| 01 | **Dictionary Forge** | L33tspeak, CamelCase, digit-suffix mutations |
| 02 | **Entropy Analyzer** | Shannon entropy, zxcvbn score, crack time |
| 03 | **Brute-Force Matrix** | ASIC/GPU attack surface modelling |
| 04 | **Hive Extraction** | Linux shadow / Windows SAM dump simulation |
| 05 | **Audit Report** | Executive security brief + remediation guide |

---

## 🔧 Requirements

- Kali Linux 2023+ / Debian 11+ / Ubuntu 22+
- Python 3.10+
- Internet connection for install

---

## ⚠️ Disclaimer

For **educational and authorized security testing only**. Unauthorized use is illegal. Authors assume no liability.

---

<div align="center">

**QYLXFORCE** · by Qylatrix Industries · *The Syntax of Safety*

[GitHub](https://github.com/Qylatrix) · [Live Site](https://qylxforce.pythonanywhere.com)

</div>
