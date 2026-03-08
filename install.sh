#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════
#  qylxforce — Qylatrix Offensive Credential Suite
#  Kali Linux Installer  |  by Qylatrix Industries
#  Usage: sudo bash install.sh
# ══════════════════════════════════════════════════════════════════

set -e

# ── Configuration ─────────────────────────────────────────────────
TOOL_NAME="qylxforce"
REPO="https://github.com/Qylatrix/qylatrix-offensive-suite"
LIVE_URL="https://qylxforce.pythonanywhere.com"   # live site
INSTALL_DIR="/opt/$TOOL_NAME"
BIN_LINK="/usr/local/bin/$TOOL_NAME"

# ── Colours ───────────────────────────────────────────────────────
CYAN=$'\033[0;36m'; BCYAN=$'\033[1;36m'
BLUE=$'\033[0;34m'; BBLUE=$'\033[1;34m'
WHITE=$'\033[1;37m'; DIM=$'\033[2m'
GREEN=$'\033[0;32m'; BGREEN=$'\033[1;32m'
RED=$'\033[0;31m';  BOLD=$'\033[1m'
NC=$'\033[0m'

clear
echo ""
echo -e "${BCYAN}"
cat << 'LOGO'
   ██████╗ ██╗   ██╗██╗     ██╗  ██╗███████╗ ██████╗ ██████╗  ██████╗███████╗
  ██╔═══██╗╚██╗ ██╔╝██║     ╚██╗██╔╝██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝
  ██║   ██║ ╚████╔╝ ██║      ╚███╔╝ █████╗  ██║   ██║██████╔╝██║     █████╗
  ██║▄▄ ██║  ╚██╔╝  ██║      ██╔██╗ ██╔══╝  ██║   ██║██╔══██╗██║     ██╔══╝
  ╚██████╔╝   ██║   ███████╗██╔╝ ██╗██║     ╚██████╔╝██║  ██║╚██████╗███████╗
   ╚══▀▀═╝    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚══════╝
LOGO
echo -e "${NC}"
echo -e "  ${DIM}┌────────────────────────────────────────────────────────────┐${NC}"
echo -e "  ${DIM}│${NC}  ${BCYAN}qylxforce${NC} ${DIM}—${NC} Offensive Credential Suite ${DIM}v2.0${NC}             ${DIM}│${NC}"
echo -e "  ${DIM}│${NC}  ${WHITE}The Syntax of Safety${NC}  ${DIM}|${NC}  ${BLUE}by Qylatrix Industries${NC}           ${DIM}│${NC}"
echo -e "  ${DIM}│${NC}  ${DIM}github.com/Qylatrix/qylatrix-offensive-suite${NC}             ${DIM}│${NC}"
echo -e "  ${DIM}└────────────────────────────────────────────────────────────┘${NC}"
echo ""

# ── Root check ────────────────────────────────────────────────────
if [[ "$EUID" -ne 0 ]]; then
    echo -e "  ${RED}[✗]${NC} Please run as root:  ${CYAN}sudo bash install.sh${NC}"
    exit 1
fi

echo -e "  ${CYAN}[*]${NC} Updating package index..."
apt-get update -qq 2>/dev/null

echo -e "  ${CYAN}[*]${NC} Installing dependencies (python3, pip, git)..."
apt-get install -y -qq python3 python3-pip python3-venv git curl xdg-utils 2>/dev/null

echo -e "  ${CYAN}[*]${NC} Cloning / updating repository..."
if [ -d "$INSTALL_DIR/.git" ]; then
    cd "$INSTALL_DIR" && git pull --quiet
else
    git clone --depth=1 --quiet "$REPO" "$INSTALL_DIR"
fi

echo -e "  ${CYAN}[*]${NC} Setting up Python environment..."
python3 -m venv "$INSTALL_DIR/.venv" --quiet
# shellcheck source=/dev/null
source "$INSTALL_DIR/.venv/bin/activate"
pip install --quiet -r "$INSTALL_DIR/requirements.txt"

echo -e "  ${CYAN}[*]${NC} Installing ${BCYAN}qylxforce${NC} command..."
cat > "$BIN_LINK" << LAUNCHER
#!/usr/bin/env bash
# qylxforce — by Qylatrix Industries
INSTALL_DIR="/opt/qylxforce"
LIVE_URL="https://qylxforce.pythonanywhere.com"
source "\$INSTALL_DIR/.venv/bin/activate"
cd "\$INSTALL_DIR"

CYAN=\$'\\033[0;36m'; BCYAN=\$'\\033[1;36m'
BLUE=\$'\\033[0;34m'; DIM=\$'\\033[2m'
WHITE=\$'\\033[1;37m'; NC=\$'\\033[0m'
BGREEN=\$'\\033[1;32m'

banner() {
echo ""
echo -e "\${BCYAN}"
cat << 'ART'
   ██████╗ ██╗   ██╗██╗     ██╗  ██╗███████╗ ██████╗ ██████╗  ██████╗███████╗
  ██╔═══██╗╚██╗ ██╔╝██║     ╚██╗██╔╝██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝
  ██║   ██║ ╚████╔╝ ██║      ╚███╔╝ █████╗  ██║   ██║██████╔╝██║     █████╗
  ██║▄▄ ██║  ╚██╔╝  ██║      ██╔██╗ ██╔══╝  ██║   ██║██╔══██╗██║     ██╔══╝
  ╚██████╔╝   ██║   ███████╗██╔╝ ██╗██║     ╚██████╔╝██║  ██║╚██████╗███████╗
   ╚══▀▀═╝    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚══════╝
ART
echo -e "\${NC}"
echo -e "  \${DIM}by Qylatrix Industries  |  The Syntax of Safety\${NC}"
echo -e "  \${CYAN}\$LIVE_URL\${NC}"
echo ""
}

case "\$1" in
    web)
        banner
        echo -e "  \${BCYAN}[*]\${NC} Starting local server at \${CYAN}http://localhost:5000\${NC}"
        echo -e "  \${BCYAN}[*]\${NC} Live site: \${CYAN}\$LIVE_URL\${NC}"
        echo ""
        python "\$INSTALL_DIR/webapp.py"
        ;;
    online|live|site)
        echo -e "  \${BCYAN}[*]\${NC} Opening live site: \${CYAN}\$LIVE_URL\${NC}"
        xdg-open "\$LIVE_URL" 2>/dev/null || echo "Visit: \$LIVE_URL"
        ;;
    dict)   shift; python "\$INSTALL_DIR/main.py" --mode dict "\$@" ;;
    analyze) shift; python "\$INSTALL_DIR/main.py" --mode analyze "\$@" ;;
    brute)  shift; python "\$INSTALL_DIR/main.py" --mode brute "\$@" ;;
    extract) shift; python "\$INSTALL_DIR/main.py" --mode extract "\$@" ;;
    report) shift; python "\$INSTALL_DIR/main.py" --mode report "\$@" ;;
    --version|-v)
        echo "qylxforce v2.0  |  by Qylatrix Industries"
        ;;
    *)
        banner
        echo "  Usage: qylxforce <command>"
        echo ""
        echo "  \${BCYAN}Commands:\${NC}"
        echo "    \${CYAN}web\${NC}        Run local web interface at localhost:5000"
        echo "    \${CYAN}online\${NC}     Open live site in browser (\$LIVE_URL)"
        echo "    \${CYAN}dict\${NC}       Dictionary generator"
        echo "    \${CYAN}analyze\${NC}    Password entropy analyzer"
        echo "    \${CYAN}brute\${NC}      Brute-force time estimator"
        echo "    \${CYAN}extract\${NC}    Hash extractor (shadow / SAM)"
        echo "    \${CYAN}report\${NC}     Executive audit report"
        echo ""
        echo "  \${DIM}by Qylatrix Industries  |  github.com/Qylatrix/qylatrix-offensive-suite\${NC}"
        echo ""
        ;;
esac
LAUNCHER

chmod +x "$BIN_LINK"
chmod -R 755 "$INSTALL_DIR"

# ── Done ──────────────────────────────────────────────────────────
echo ""
echo -e "  ${BGREEN}[✔]${NC} ${BOLD}${BCYAN}qylxforce${NC} installed successfully!"
echo ""
echo -e "  ${DIM}┌────────────────────────────────────────────────────────────┐${NC}"
echo -e "  ${DIM}│${NC}  ${CYAN}qylxforce web${NC}     — launch local web interface            ${DIM}│${NC}"
echo -e "  ${DIM}│${NC}  ${CYAN}qylxforce online${NC}  — open live site in browser             ${DIM}│${NC}"
echo -e "  ${DIM}│${NC}  ${CYAN}qylxforce${NC}         — show all commands                     ${DIM}│${NC}"
echo -e "  ${DIM}└────────────────────────────────────────────────────────────┘${NC}"
echo ""
echo -e "  ${BCYAN}[*]${NC} Opening live site in 3 seconds..."
sleep 3
xdg-open "$LIVE_URL" 2>/dev/null || echo -e "  ${CYAN}[→]${NC} Visit: $LIVE_URL"
echo ""
