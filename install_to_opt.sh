#!/bin/bash

# XorLang Enhanced Installer - Copy to /opt
# Version: 2.0.0
# Author: XorLang Development Team
# Description: Enhanced installer with backup, logging, and better error handling

set -euo pipefail  # Exit on any error, undefined variables, and pipe failures

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly CYAN='\033[0;36m'
readonly BOLD='\033[1m'
readonly NC='\033[0m' # No Color

# Configuration
readonly VERSION="2.0.0"
readonly INSTALL_DIR="/opt/xorlang"
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly DIST_DIR="$SCRIPT_DIR/dist"
readonly ICON_SOURCE="$SCRIPT_DIR/icon/X.ico"
readonly LOG_FILE="/tmp/xorlang-install-$(date +%Y%m%d-%H%M%S).log"
readonly BACKUP_DIR="/tmp/xorlang-backup-$(date +%Y%m%d-%H%M%S)"

# Global variables
FORCE_INSTALL=false
SKIP_BACKUP=false
VERBOSE=false

# Logging function
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"
    
    case "$level" in
        "INFO")  echo -e "${BLUE}[INFO]${NC} $message" ;;
        "WARN")  echo -e "${YELLOW}[WARN]${NC} $message" ;;
        "ERROR") echo -e "${RED}[ERROR]${NC} $message" ;;
        "SUCCESS") echo -e "${GREEN}[SUCCESS]${NC} $message" ;;
        "DEBUG") [[ "$VERBOSE" == true ]] && echo -e "${CYAN}[DEBUG]${NC} $message" ;;
    esac
}

# Error handler
error_exit() {
    log "ERROR" "$1"
    echo -e "${RED}Installation failed. Check log file: $LOG_FILE${NC}"
    exit 1
}

# Cleanup function
cleanup() {
    if [[ -d "$BACKUP_DIR" && "$SKIP_BACKUP" == false ]]; then
        log "INFO" "Backup created at: $BACKUP_DIR"
        echo -e "${CYAN}Backup available at: $BACKUP_DIR${NC}"
    fi
}

# Set up signal handlers
trap cleanup EXIT
trap 'error_exit "Installation interrupted by user"' INT TERM

# Help function
show_help() {
    cat << EOF
${BOLD}XorLang Enhanced Installer v$VERSION${NC}

${BOLD}USAGE:${NC}
    sudo ./install_to_opt.sh [OPTIONS]

${BOLD}OPTIONS:${NC}
    -f, --force         Force installation even if XorLang is already installed
    -s, --skip-backup   Skip creating backup of existing installation
    -v, --verbose       Enable verbose output
    -h, --help          Show this help message

${BOLD}EXAMPLES:${NC}
    sudo ./install_to_opt.sh                    # Standard installation
    sudo ./install_to_opt.sh --force            # Force reinstall
    sudo ./install_to_opt.sh --verbose          # Verbose installation
    sudo ./install_to_opt.sh --skip-backup -f   # Force install without backup

${BOLD}DESCRIPTION:${NC}
    This script installs XorLang to /opt/xorlang and creates symlinks in /usr/local/bin.
    It includes backup functionality, dependency checking, and comprehensive logging.

EOF
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -f|--force)
                FORCE_INSTALL=true
                shift
                ;;
            -s|--skip-backup)
                SKIP_BACKUP=true
                shift
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                error_exit "Unknown option: $1. Use --help for usage information."
                ;;
        esac
    done
}

# Check system requirements
check_requirements() {
    log "INFO" "Checking system requirements..."
    
    # Check if running as root
    if [[ $EUID -ne 0 ]]; then
        error_exit "This script must be run as root (use sudo)"
    fi
    
    # Check available disk space (at least 100MB)
    local available_space=$(df /opt 2>/dev/null | awk 'NR==2 {print $4}' || echo "0")
    if [[ $available_space -lt 102400 ]]; then
        error_exit "Insufficient disk space. At least 100MB required in /opt"
    fi
    
    # Check for required commands
    local required_commands=("cp" "chmod" "ln" "mkdir")
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            error_exit "Required command '$cmd' not found"
        fi
    done
    
    log "SUCCESS" "System requirements check passed"
}

# Check if XorLang is already installed
check_existing_installation() {
    if [[ -d "$INSTALL_DIR" || -L "/usr/local/bin/xorlang" || -L "/usr/local/bin/xorlang-ide" ]]; then
        if [[ "$FORCE_INSTALL" == false ]]; then
            echo -e "${YELLOW}XorLang appears to be already installed.${NC}"
            echo "Installation directory: $INSTALL_DIR"
            echo "Use --force to reinstall or --help for more options."
            exit 1
        else
            log "WARN" "Existing installation detected, but --force specified"
            return 0
        fi
    fi
}

# Create backup of existing installation
create_backup() {
    if [[ "$SKIP_BACKUP" == true ]]; then
        log "INFO" "Skipping backup as requested"
        return 0
    fi
    
    if [[ -d "$INSTALL_DIR" ]]; then
        log "INFO" "Creating backup of existing installation..."
        mkdir -p "$BACKUP_DIR"
        
        if cp -r "$INSTALL_DIR" "$BACKUP_DIR/"; then
            log "SUCCESS" "Backup created successfully at $BACKUP_DIR"
        else
            log "WARN" "Failed to create backup, continuing anyway..."
        fi
    fi
}

# Validate source files
validate_source_files() {
    log "INFO" "Validating source files..."
    
    if [[ ! -d "$DIST_DIR" ]]; then
        error_exit "Distribution directory not found: $DIST_DIR"
    fi
    
    # Check icon file
    if [[ ! -f "$ICON_SOURCE" ]]; then
        log "WARN" "Icon file not found: $ICON_SOURCE (desktop entries will be created without icon)"
    else
        log "DEBUG" "Icon file found: $ICON_SOURCE"
    fi
    
    local required_files=("xorlang" "xorlang-ide")
    for file in "${required_files[@]}"; do
        local file_path="$DIST_DIR/$file"
        if [[ ! -f "$file_path" ]]; then
            error_exit "Required file not found: $file_path"
        fi
        
        if [[ ! -x "$file_path" ]]; then
            error_exit "File is not executable: $file_path"
        fi
        
        # Check file size (should be > 1KB) - simplified approach
        if [[ ! -s "$file_path" ]]; then
            error_exit "File appears to be empty or corrupted: $file_path"
        fi
        
        # Get file size for logging (non-blocking)
        local file_size=$(wc -c < "$file_path" 2>/dev/null || echo "unknown")
        log "DEBUG" "Validated: $file_path (${file_size} bytes)"
    done
    
    log "SUCCESS" "Source files validation passed"
}

# Install icon and desktop entries
install_desktop_integration() {
    log "INFO" "Installing desktop integration..."
    
    # Install icon if available
    if [[ -f "$ICON_SOURCE" ]]; then
        log "INFO" "Installing application icon..."
        
        # Copy icon to system location
        local icon_dest="/usr/share/pixmaps/xorlang.ico"
        if cp "$ICON_SOURCE" "$icon_dest"; then
            log "SUCCESS" "Icon installed to $icon_dest"
        else
            log "WARN" "Failed to install icon, continuing without icon support"
            return 0
        fi
    else
        log "WARN" "Icon file not found, skipping icon installation"
        return 0
    fi
    
    # Create desktop entry for XorLang IDE
    log "INFO" "Creating desktop entry for XorLang IDE..."
    cat > /usr/share/applications/xorlang-ide.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=XorLang IDE
Comment=XorLang Integrated Development Environment
Exec=xorlang-ide %F
Icon=/usr/share/pixmaps/xorlang.ico
Terminal=false
StartupNotify=true
MimeType=text/x-xorlang;
Categories=Development;IDE;
Keywords=xorlang;programming;development;ide;
StartupWMClass=XorLang IDE
EOF
    
    if [[ $? -eq 0 ]]; then
        log "SUCCESS" "XorLang IDE desktop entry created"
    else
        log "WARN" "Failed to create XorLang IDE desktop entry"
    fi
    
    # Create desktop entry for XorLang CLI (for file associations)
    log "INFO" "Creating desktop entry for XorLang CLI..."
    cat > /usr/share/applications/xorlang.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=XorLang
Comment=XorLang Programming Language Interpreter
Exec=xorlang %F
Icon=/usr/share/pixmaps/xorlang.ico
Terminal=true
StartupNotify=false
MimeType=text/x-xorlang;
Categories=Development;
Keywords=xorlang;programming;interpreter;
NoDisplay=true
EOF
    
    if [[ $? -eq 0 ]]; then
        log "SUCCESS" "XorLang CLI desktop entry created"
    else
        log "WARN" "Failed to create XorLang CLI desktop entry"
    fi
    
    # Create MIME type definition for .xor files
    log "INFO" "Creating MIME type definition..."
    cat > /usr/share/mime/packages/xorlang.xml << EOF
<?xml version="1.0" encoding="UTF-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
    <mime-type type="text/x-xorlang">
        <comment>XorLang source code</comment>
        <comment xml:lang="en">XorLang source code</comment>
        <icon name="xorlang"/>
        <glob pattern="*.xor"/>
        <glob pattern="*.xorlang"/>
    </mime-type>
</mime-info>
EOF
    
    if [[ $? -eq 0 ]]; then
        log "SUCCESS" "MIME type definition created"
        
        # Update MIME database
        if command -v update-mime-database &> /dev/null; then
            log "INFO" "Updating MIME database..."
            if update-mime-database /usr/share/mime; then
                log "SUCCESS" "MIME database updated"
            else
                log "WARN" "Failed to update MIME database"
            fi
        else
            log "WARN" "update-mime-database not found, MIME types may not work immediately"
        fi
        
        # Update desktop database
        if command -v update-desktop-database &> /dev/null; then
            log "INFO" "Updating desktop database..."
            if update-desktop-database /usr/share/applications; then
                log "SUCCESS" "Desktop database updated"
            else
                log "WARN" "Failed to update desktop database"
            fi
        else
            log "WARN" "update-desktop-database not found, desktop entries may not appear immediately"
        fi
    else
        log "WARN" "Failed to create MIME type definition"
    fi
    
    log "SUCCESS" "Desktop integration installation completed"
}

# Install XorLang
install_xorlang() {
    log "INFO" "Starting XorLang installation to $INSTALL_DIR..."
    
    # Remove existing installation if present
    if [[ -d "$INSTALL_DIR" ]]; then
        log "INFO" "Removing existing installation..."
        rm -rf "$INSTALL_DIR" || error_exit "Failed to remove existing installation"
    fi
    
    # Create installation directory
    mkdir -p "$INSTALL_DIR" || error_exit "Failed to create installation directory"
    log "DEBUG" "Created installation directory: $INSTALL_DIR"
    
    # Copy executables with progress indication
    local files=("xorlang" "xorlang-ide")
    for file in "${files[@]}"; do
        log "INFO" "Installing $file..."
        if cp "$DIST_DIR/$file" "$INSTALL_DIR/" && chmod +x "$INSTALL_DIR/$file"; then
            log "SUCCESS" "Successfully installed $file"
        else
            error_exit "Failed to install $file"
        fi
    done
    
    # Create symlinks in /usr/local/bin
    log "INFO" "Creating system-wide symlinks..."
    
    # Remove existing symlinks if they exist
    [[ -L "/usr/local/bin/xorlang" ]] && rm -f "/usr/local/bin/xorlang"
    [[ -L "/usr/local/bin/xorlang-ide" ]] && rm -f "/usr/local/bin/xorlang-ide"
    
    if ln -sf "$INSTALL_DIR/xorlang" "/usr/local/bin/xorlang" && \
       ln -sf "$INSTALL_DIR/xorlang-ide" "/usr/local/bin/xorlang-ide"; then
        log "SUCCESS" "System-wide symlinks created successfully"
    else
        error_exit "Failed to create system-wide symlinks"
    fi
    
    # Install desktop integration (icon, desktop entries, MIME types)
    install_desktop_integration
}

# Verify installation
verify_installation() {
    log "INFO" "Verifying installation..."
    
    # Check if files exist and are executable
    local files=("$INSTALL_DIR/xorlang" "$INSTALL_DIR/xorlang-ide")
    for file in "${files[@]}"; do
        if [[ ! -f "$file" || ! -x "$file" ]]; then
            error_exit "Installation verification failed: $file"
        fi
    done
    
    # Check symlinks
    local symlinks=("/usr/local/bin/xorlang" "/usr/local/bin/xorlang-ide")
    for symlink in "${symlinks[@]}"; do
        if [[ ! -L "$symlink" ]]; then
            error_exit "Installation verification failed: $symlink"
        fi
    done
    
    # Test executables (basic version check)
    if timeout 5 "$INSTALL_DIR/xorlang" --version &>/dev/null; then
        log "SUCCESS" "XorLang CLI executable verified"
    else
        log "WARN" "Could not verify XorLang CLI executable (this may be normal)"
    fi
    
    log "SUCCESS" "Installation verification completed"
}

# Show installation summary
show_summary() {
    echo ""
    echo -e "${GREEN}${BOLD}✓ XorLang Installation Completed Successfully!${NC}"
    echo -e "${BLUE}=================================${NC}"
    echo ""
    echo -e "${BOLD}Installation Details:${NC}"
    echo "  • Installation Directory: $INSTALL_DIR"
    echo "  • Icon: /usr/share/pixmaps/xorlang.ico"
    echo "  • Desktop Entries: /usr/share/applications/xorlang*.desktop"
    echo "  • MIME Types: /usr/share/mime/packages/xorlang.xml"
    echo "  • Log File: $LOG_FILE"
    [[ -d "$BACKUP_DIR" && "$SKIP_BACKUP" == false ]] && echo "  • Backup Directory: $BACKUP_DIR"
    echo ""
    echo -e "${BOLD}Available Commands:${NC}"
    echo "  • xorlang          - CLI interpreter"
    echo "  • xorlang-ide      - Graphical IDE"
    echo ""
    echo -e "${BOLD}Desktop Integration:${NC}"
    echo "  • .xor files will open with XorLang IDE"
    echo "  • XorLang IDE available in Applications menu"
    echo "  • Custom icon for XorLang applications"
    echo ""
    echo -e "${BOLD}Quick Start:${NC}"
    echo "  xorlang --help     - Show CLI help"
    echo "  xorlang --version  - Show version"
    echo "  xorlang-ide        - Start the IDE"
    echo ""
    echo -e "${BOLD}Uninstall Options:${NC}"
    echo -e "${CYAN}  ./uninstall_xorlang.sh        - Use the dedicated uninstaller (recommended)${NC}"
    echo -e "${CYAN}  ./uninstall_xorlang.sh --help - Show uninstaller options${NC}"
    echo ""
    echo -e "${BOLD}Manual Uninstall Command:${NC}"
    echo -e "${CYAN}  sudo rm -rf $INSTALL_DIR && sudo rm -f /usr/local/bin/xorlang* /usr/share/pixmaps/xorlang.ico /usr/share/applications/xorlang*.desktop /usr/share/mime/packages/xorlang.xml${NC}"
    echo ""
}

# Main installation function
main() {
    # Initialize logging
    echo "XorLang Enhanced Installer v$VERSION - $(date)" > "$LOG_FILE"
    
    # Show header
    echo -e "${BLUE}${BOLD}XorLang Enhanced Installer v$VERSION${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    
    # Parse arguments
    parse_args "$@"
    
    # Run installation steps
    check_requirements
    check_existing_installation
    validate_source_files
    create_backup
    install_xorlang
    verify_installation
    show_summary
    
    log "SUCCESS" "Installation completed successfully"
}

# Run main function with all arguments
main "$@"
