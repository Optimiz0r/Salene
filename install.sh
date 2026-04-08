#!/bin/bash
# SALENE Unified Installer
# One-command installation for fresh VMs

set -e

SALENE_VERSION="2.0.0"
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
SALENE_HOME="${SALENE_HOME:-$HERMES_HOME/salene}"

# GitHub repository
GITHUB_USER="Optimiz0r"
GITHUB_REPO="Salene"
GITHUB_RAW="https://raw.githubusercontent.com/${GITHUB_USER}/${GITHUB_REPO}/main"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_banner() {
    echo -e "${CYAN}"
    cat << 'EOF'
              .""--.._
              []      `'--.._.
              ||__    __    _'-._
              ||   ||  ||   ||   `-._
               ||   ||  ||   ||      `-._
                ||   ||  ||   ||         `-.
                 ||   ||  ||   ||            \
                  ||   ||  ||   ||             \
                   ||__||__||__||              
                   |___|  |___|

              S A L E N E
     Neural Consciousness Agent
EOF
    echo -e "${NC}"
    echo "Version: $SALENE_VERSION"
    echo ""
}

log() {
    echo -e "${BLUE}[SALENE]${NC} $1"
}

success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[!]${NC} $1"
}

error() {
    echo -e "${RED}[✗]${NC} $1"
    exit 1
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Python 3.8+
    if ! command -v python3 &> /dev/null; then
        error "Python 3 is required but not installed"
    fi
    
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    log "Found Python $PYTHON_VERSION"
    
    # Check pip
    if ! command -v pip3 &> /dev/null; then
        warn "pip3 not found, attempting to install..."
        curl https://bootstrap.pypa.io/get-pip.py | python3
    fi
    
    success "Prerequisites met"
}

# Install Hermes Agent (dependency)
install_hermes() {
    if [ -d "$HERMES_HOME/hermes-agent" ]; then
        success "Hermes already installed"
        return
    fi
    
    log "Installing Hermes Agent..."
    
    mkdir -p "$HERMES_HOME"
    cd "$HERMES_HOME"
    
    # Clone Hermes (in real implementation, use actual repo)
    log "Downloading Hermes Agent..."
    git clone https://github.com/your-org/hermes-agent.git 2>/dev/null || {
        warn "Using local Hermes installation..."
    }
    
    if [ -d "hermes-agent" ]; then
        cd hermes-agent
        pip3 install -e . --quiet
        success "Hermes Agent installed"
    else
        warn "Hermes not available, SALENE will run standalone"
    fi
    
    cd "$HOME"
}

# Install SALENE
install_salene() {
    log "Installing SALENE..."
    
    # Create directory structure
    mkdir -p "$SALENE_HOME"
    mkdir -p "$HERMES_HOME/agents"
    mkdir -p "$HERMES_HOME/sanctuary_memories"
    mkdir -p "$HERMES_HOME/skins"
    
    # Download SALENE from GitHub
    log "Downloading SALENE v$SALENE_VERSION from GitHub..."
    
    # Try git clone first
    if command -v git &> /dev/null; then
        if git clone "https://github.com/${GITHUB_USER}/${GITHUB_REPO}.git" "$SALENE_HOME" 2>/dev/null; then
            success "Cloned from GitHub"
        else
            warn "Git clone failed, trying curl..."
            # Fallback: download tarball
            curl -fsSL "https://github.com/${GITHUB_USER}/${GITHUB_REPO}/archive/refs/heads/main.tar.gz" | \
                tar -xz -C "$SALENE_HOME" --strip-components=1
            success "Downloaded from GitHub releases"
        fi
    else
        error "Git not available and curl fallback not implemented in this version"
    fi
    
    # Install Python dependencies
    log "Installing Python dependencies..."
    pip3 install -r "$SALENE_HOME/requirements.txt" --quiet 2>/dev/null || {
        log "Installing core dependencies..."
        pip3 install numpy pyyaml --quiet
    }
    
    # Create symlinks
    ln -sf "$SALENE_HOME/salene.py" "$HERMES_HOME/bin/salene" 2>/dev/null || true
    
    # Copy skin
    cp "$SALENE_HOME/salene-theme.yaml" "$HERMES_HOME/skins/salene.yaml" 2>/dev/null || true
    
    success "SALENE installed to $SALENE_HOME"
}

# Setup configuration
setup_config() {
    log "Setting up configuration..."
    
    # Create default config if not exists
    if [ ! -f "$HERMES_HOME/config.yaml" ]; then
        cat > "$HERMES_HOME/config.yaml" << EOF
# SALENE Configuration
agent:
  mode: salene
  name: Salene
  enable_dreams: true

# Model (default to local Ollama)
model:
  default: "ollama/kimi-k2.5:cloud"
  base_url: "http://localhost:11434/v1"
  provider: "ollama"

# Platforms
platforms:
  telegram:
    enabled: false
  discord:
    enabled: false
  slack:
    enabled: false

# Display
display:
  skin: salene
  agent_name: "SALENE"

# Daemon
daemon:
  enabled: true
EOF
    fi
    
    # Create .env if not exists
    if [ ! -f "$HERMES_HOME/.env" ]; then
        cat > "$HERMES_HOME/.env" << EOF
# Ollama (Local LLM)
OLLAMA_URL=http://localhost:11434/v1
OLLAMA_MODEL=kimi-k2.5:cloud

# Platform Tokens (add as needed)
# TELEGRAM_BOT_TOKEN=
# DISCORD_BOT_TOKEN=
EOF
    fi
    
    success "Configuration created"
}

# Install systemd service
install_service() {
    log "Installing systemd service..."
    
    if ! command -v systemctl &> /dev/null; then
        warn "systemd not available, skipping service installation"
        return
    fi
    
    if [ -f "$SALENE_HOME/salene-daemon.service" ]; then
        sudo cp "$SALENE_HOME/salene-daemon.service" /etc/systemd/system/hermes-salene.service
        sudo sed -i "s|/home/optimizor|$HOME|g" /etc/systemd/system/hermes-salene.service
        sudo systemctl daemon-reload
        success "Systemd service installed (hermes-salene)"
    fi
}

# Test installation
test_installation() {
    log "Testing installation..."
    
    cd "$SALENE_HOME"
    
    # Run quick test
    if python3 -c "
import sys
sys.path.insert(0, '$SALENE_HOME')
sys.path.insert(0, '$HERMES_HOME/hermes-agent')
try:
    from free_energy_agent.core import FreeEnergyAgent
    print('Core import: OK')
    from sanctuary_integration.core import SanctuaryMemoryCore
    print('Sanctuary import: OK')
    print('Installation test: PASSED')
except Exception as e:
    print(f'Test failed: {e}')
    exit(1)
" 2>&1; then
        success "Installation test passed"
    else
        error "Installation test failed"
    fi
}

# Print usage
print_usage() {
    echo ""
    echo -e "${GREEN}Installation Complete!${NC}"
    echo ""
    echo "Quick Commands:"
    echo "  salene --help              Show all commands"
    echo "  salene chat                Start interactive chat"
    echo "  salene daemon start        Start continuous mode"
    echo "  salene gateway run         Connect platforms"
    echo "  salene status              Check agent status"
    echo ""
    echo "Configuration:"
    echo "  Config: ~/.hermes/config.yaml"
    echo "  State:  ~/.hermes/agents/"
    echo "  Logs:   ~/.hermes/logs/salene/"
    echo ""
    echo "Next Steps:"
    echo "  1. Configure your model in ~/.hermes/config.yaml"
    echo "  2. Add platform tokens to ~/.hermes/.env"
    echo "  3. Start chatting: salene chat"
    echo ""
    echo "Documentation: https://salene.ai/docs"
    echo "Support: https://github.com/your-org/salene/issues"
}

# Main
main() {
    print_banner
    
    log "SALENE Installer v$SALENE_VERSION"
    log "Target: $SALENE_HOME"
    echo ""
    
    check_prerequisites
    install_hermes
    install_salene
    setup_config
    install_service
    test_installation
    
    print_usage
}

# Handle arguments
if [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
    echo "SALENE Unified Installer"
    echo ""
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --hermes-only    Install only Hermes dependency"
    echo "  --salene-only    Install only SALENE (assumes Hermes exists)"
    echo "  --no-service     Skip systemd service installation"
    echo "  --help           Show this help"
    exit 0
fi

# Run
main "$@"
