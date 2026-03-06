#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
#  qylxforce — Qylatrix Offensive Credential Suite
#  Kali Linux / Debian installer
#  Usage: sudo bash install.sh
# ─────────────────────────────────────────────────────────────

set -e

TOOL_NAME="qylxforce"
REPO="https://github.com/Qylatrix/qylatrix-offensive-suite"
INSTALL_DIR="/opt/$TOOL_NAME"
BIN_LINK="/usr/local/bin/$TOOL_NAME"
CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${CYAN}${BOLD}"
echo "  ██████╗ ██╗   ██╗██╗      █████╗ ████████╗██████╗ ██╗██╗  ██╗"
echo "  ██╔═══██╗╚██╗ ██╔╝██║     ██╔══██╗╚══██╔══╝██╔══██╗██║╚██╗██╔╝"
echo "  ██║   ██║ ╚████╔╝ ██║     ███████║   ██║   ██████╔╝██║ ╚███╔╝ "
echo "  ██║▄▄ ██║  ╚██╔╝  ██║     ██╔══██║   ██║   ██╔══██╗██║ ██╔██╗ "
echo "  ╚██████╔╝   ██║   ███████╗██║  ██║   ██║   ██║  ██║██║██╔╝ ██╗"
echo "   ╚══▀▀═╝    ╚═╝   ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝"
echo -e "${NC}"
echo -e "${CYAN}  [ qylxforce — The Syntax of Safety ]${NC}"
echo -e "${CYAN}  Qylatrix Offensive Credential Suite Installer${NC}"
echo ""

# Check root
if [[ "$EUID" -ne 0 ]]; then
    echo -e "${RED}[!] Please run as root: sudo bash install.sh${NC}"
    exit 1
fi

echo -e "${CYAN}[*] Updating package lists...${NC}"
apt-get update -qq

echo -e "${CYAN}[*] Installing system dependencies...${NC}"
apt-get install -y -qq python3 python3-pip python3-venv git curl

echo -e "${CYAN}[*] Cloning qylxforce repository...${NC}"
if [ -d "$INSTALL_DIR" ]; then
    echo -e "    [~] Updating existing installation..."
    cd "$INSTALL_DIR" && git pull --quiet
else
    git clone --quiet "$REPO" "$INSTALL_DIR"
fi

echo -e "${CYAN}[*] Setting up Python virtual environment...${NC}"
python3 -m venv "$INSTALL_DIR/.venv"
source "$INSTALL_DIR/.venv/bin/activate"

echo -e "${CYAN}[*] Installing Python requirements...${NC}"
pip install --quiet flask zxcvbn

echo -e "${CYAN}[*] Creating launcher script...${NC}"
cat > "$BIN_LINK" << 'LAUNCHER'
#!/usr/bin/env bash
# qylxforce launcher
INSTALL_DIR="/opt/qylxforce"
source "$INSTALL_DIR/.venv/bin/activate"
cd "$INSTALL_DIR"

case "$1" in
    web)
        echo "[*] Starting qylxforce web interface on http://localhost:5000"
        python "$INSTALL_DIR/webapp.py"
        ;;
    dict)
        shift
        python "$INSTALL_DIR/main.py" --mode dict "$@"
        ;;
    analyze)
        shift
        python "$INSTALL_DIR/main.py" --mode analyze "$@"
        ;;
    brute)
        shift
        python "$INSTALL_DIR/main.py" --mode brute "$@"
        ;;
    extract)
        shift
        python "$INSTALL_DIR/main.py" --mode extract "$@"
        ;;
    report)
        shift
        python "$INSTALL_DIR/main.py" --mode report "$@"
        ;;
    --version|-v)
        echo "qylxforce v2.0 — Qylatrix Offensive Credential Suite"
        echo "  by Qylatrix Industries | The Syntax of Safety"
        ;;
    *)
        echo ""
        echo "  ┌─────────────────────────────────────────────────────┐"
        echo "  │  qylxforce — Qylatrix Offensive Credential Suite    │"
        echo "  │  The Syntax of Safety                               │"
        echo "  └─────────────────────────────────────────────────────┘"
        echo ""
        echo "  Usage: qylxforce <module> [options]"
        echo ""
        echo "  Modules:"
        echo "    web          Launch premium web interface (default port 5000)"
        echo "    dict         Dictionary generator — wordlist synthesis"
        echo "    analyze      Entropy analyzer — password strength audit"
        echo "    brute        Brute-force time estimator"
        echo "    extract      Credential hash extractor (shadow/SAM)"
        echo "    report       Executive audit report generator"
        echo ""
        echo "  Examples:"
        echo "    qylxforce web"
        echo "    qylxforce dict --words alice,company2024"
        echo "    qylxforce analyze --password 'P@ssw0rd!'"
        echo "    qylxforce report --file passwords.txt"
        echo ""
        echo "  GitHub: https://github.com/Qylatrix/qylatrix-offensive-suite"
        ;;
esac
LAUNCHER

chmod +x "$BIN_LINK"

echo -e "${CYAN}[*] Setting permissions...${NC}"
chmod -R 755 "$INSTALL_DIR"

echo ""
echo -e "${GREEN}${BOLD}[✔] qylxforce installed successfully!${NC}"
echo ""
echo -e "    Run ${CYAN}qylxforce${NC} to see all commands."
echo -e "    Run ${CYAN}qylxforce web${NC} to launch the web UI."
echo ""
