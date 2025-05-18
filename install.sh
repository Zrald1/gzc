#!/bin/bash
# GZ Programming Language Installer
# This script installs the GZ compiler and sets up the 'gzc' command.

set -e

# Define colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== GZ Programming Language Installer ===${NC}"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
    echo "Please install Python 3 and try again."
    exit 1
fi

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Create installation directory
INSTALL_DIR="$HOME/.gz"
mkdir -p "$INSTALL_DIR"
echo -e "${GREEN}Creating installation directory: $INSTALL_DIR${NC}"

# Copy files to installation directory
echo -e "${GREEN}Copying files...${NC}"
cp -r "$SCRIPT_DIR/src" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/include" "$INSTALL_DIR/" 2>/dev/null || true
cp -r "$SCRIPT_DIR/examples" "$INSTALL_DIR/" 2>/dev/null || true
mkdir -p "$INSTALL_DIR/models"
cp -r "$SCRIPT_DIR/models"/* "$INSTALL_DIR/models/" 2>/dev/null || true

# Create bin directory if it doesn't exist
BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"

# Create gzc executable
echo -e "${GREEN}Creating gzc executable...${NC}"
cat > "$BIN_DIR/gzc" << EOF
#!/bin/bash
# GZ Programming Language Compiler

# Get the GZ installation directory
GZ_DIR="$INSTALL_DIR"

# Run the GZ compiler
python3 "\$GZ_DIR/src/gzc.py" "\$@"
EOF

# Make gzc executable
chmod +x "$BIN_DIR/gzc"

# Check if $BIN_DIR is in PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo -e "${YELLOW}Warning: $BIN_DIR is not in your PATH.${NC}"
    echo "Add the following line to your ~/.bashrc or ~/.zshrc file:"
    echo "export PATH=\"\$PATH:$BIN_DIR\""
    
    # Ask if we should add it automatically
    read -p "Would you like to add it automatically? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Determine shell configuration file
        if [[ -n "$ZSH_VERSION" ]]; then
            SHELL_CONFIG="$HOME/.zshrc"
        elif [[ -n "$BASH_VERSION" ]]; then
            SHELL_CONFIG="$HOME/.bashrc"
        else
            SHELL_CONFIG="$HOME/.profile"
        fi
        
        # Add to PATH
        echo "export PATH=\"\$PATH:$BIN_DIR\"" >> "$SHELL_CONFIG"
        echo -e "${GREEN}Added $BIN_DIR to your PATH in $SHELL_CONFIG${NC}"
        echo "Please restart your terminal or run 'source $SHELL_CONFIG' to apply the changes."
    fi
fi

# Create models directory and README
mkdir -p "$INSTALL_DIR/models"
cat > "$INSTALL_DIR/models/README.md" << EOF
# GZ AI Models

This directory contains the AI models used by the GZ programming language for:

1. Auto-generation of code
2. Auto-correction of syntax errors
3. Auto-optimization of code

The models will be downloaded automatically when needed.
EOF

echo -e "${GREEN}Installation complete!${NC}"
echo
echo -e "You can now use the ${YELLOW}gzc${NC} command to compile and run GZ programs."
echo -e "Example: ${YELLOW}gzc examples/hello.gz -r${NC}"
echo
echo -e "For more information, run: ${YELLOW}gzc --help${NC}"
echo
echo -e "${GREEN}Enjoy programming with GZ!${NC}"
