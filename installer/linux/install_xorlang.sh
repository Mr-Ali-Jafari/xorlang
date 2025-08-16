#!/bin/bash

# XorLang v2.0.0 Linux Installer
# This script installs XorLang on Linux systems

set -e  # Exit on any error

# Configuration
APP_NAME="XorLang"
APP_VERSION="2.0.0"
INSTALL_DIR="/opt/xorlang"
BIN_DIR="/usr/local/bin"
DESKTOP_DIR="/usr/share/applications"
ICON_DIR="/usr/share/icons/hicolor/256x256/apps"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_warning "Running as root. This is not recommended for security reasons."
        read -p "Do you want to continue? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_error "Installation cancelled."
            exit 1
        fi
    fi
}

# Function to check system requirements
check_requirements() {
    print_status "Checking system requirements..."
    
    # Check if running on Linux
    if [[ "$OSTYPE" != "linux-gnu"* ]]; then
        print_error "This installer is designed for Linux systems only."
        exit 1
    fi
    
    # Check if required directories exist
    if [[ ! -d "/opt" ]]; then
        print_error "/opt directory does not exist. This is unusual for a Linux system."
        exit 1
    fi
    
    # Check if we have write permissions
    if [[ ! -w "/opt" ]]; then
        print_error "No write permission to /opt. Please run with sudo."
        exit 1
    fi
    
    print_success "System requirements check passed."
}

# Function to create installation directories
create_directories() {
    print_status "Creating installation directories..."
    
    # Create main installation directory
    if [[ ! -d "$INSTALL_DIR" ]]; then
        mkdir -p "$INSTALL_DIR"
        print_success "Created $INSTALL_DIR"
    else
        print_warning "$INSTALL_DIR already exists. Will overwrite existing installation."
    fi
    
    # Create subdirectories
    mkdir -p "$INSTALL_DIR/bin"
    mkdir -p "$INSTALL_DIR/stdlib"
    mkdir -p "$INSTALL_DIR/docs"
    mkdir -p "$INSTALL_DIR/examples"
    
    print_success "Installation directories created."
}

# Function to copy files
copy_files() {
    print_status "Copying XorLang files..."
    
    # Get the directory where this script is located
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
    
    # Copy executables
    if [[ -f "$PROJECT_ROOT/dist/xorlang" ]]; then
        cp "$PROJECT_ROOT/dist/xorlang" "$INSTALL_DIR/bin/"
        chmod +x "$INSTALL_DIR/bin/xorlang"
        print_success "Copied xorlang executable"
    else
        print_error "xorlang executable not found. Please build the project first."
        exit 1
    fi
    
    if [[ -f "$PROJECT_ROOT/dist/xorlang-ide" ]]; then
        cp "$PROJECT_ROOT/dist/xorlang-ide" "$INSTALL_DIR/bin/"
        chmod +x "$INSTALL_DIR/bin/xorlang-ide"
        print_success "Copied xorlang-ide executable"
    else
        print_warning "xorlang-ide executable not found. Skipping IDE installation."
    fi
    
    # Copy standard library
    if [[ -d "$PROJECT_ROOT/src/xorlang/stdlib" ]]; then
        cp -r "$PROJECT_ROOT/src/xorlang/stdlib/"* "$INSTALL_DIR/stdlib/"
        print_success "Copied standard library"
    else
        print_error "Standard library not found."
        exit 1
    fi
    
    # Copy documentation
    if [[ -f "$PROJECT_ROOT/README.md" ]]; then
        cp "$PROJECT_ROOT/README.md" "$INSTALL_DIR/docs/"
    fi
    if [[ -f "$PROJECT_ROOT/CHANGELOG.md" ]]; then
        cp "$PROJECT_ROOT/CHANGELOG.md" "$INSTALL_DIR/docs/"
    fi
    if [[ -f "$PROJECT_ROOT/PERFORMANCE_OPTIMIZATIONS.md" ]]; then
        cp "$PROJECT_ROOT/PERFORMANCE_OPTIMIZATIONS.md" "$INSTALL_DIR/docs/"
    fi
    print_success "Copied documentation"
    
    # Copy icon if available
    if [[ -f "$PROJECT_ROOT/src/xorlang/x.ico" ]]; then
        mkdir -p "$ICON_DIR"
        # Convert ICO to PNG for Linux (if ImageMagick is available)
        if command -v convert &> /dev/null; then
            convert "$PROJECT_ROOT/src/xorlang/x.ico" "$ICON_DIR/xorlang.png"
            print_success "Copied and converted icon"
        else
            print_warning "ImageMagick not found. Icon conversion skipped."
        fi
    fi
    
    print_success "All files copied successfully."
}

# Function to create symlinks
create_symlinks() {
    print_status "Creating symlinks..."
    
    # Create symlinks in /usr/local/bin
    if [[ -f "$INSTALL_DIR/bin/xorlang" ]]; then
        ln -sf "$INSTALL_DIR/bin/xorlang" "$BIN_DIR/xorlang"
        print_success "Created symlink: $BIN_DIR/xorlang"
    fi
    
    if [[ -f "$INSTALL_DIR/bin/xorlang-ide" ]]; then
        ln -sf "$INSTALL_DIR/bin/xorlang-ide" "$BIN_DIR/xorlang-ide"
        print_success "Created symlink: $BIN_DIR/xorlang-ide"
    fi
    
    print_success "Symlinks created successfully."
}

# Function to create desktop files
create_desktop_files() {
    print_status "Creating desktop integration..."
    
    # Create desktop file for CLI
    cat > "$DESKTOP_DIR/xorlang.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=XorLang
Comment=Modern programming language interpreter
Exec=xorlang
Icon=xorlang
Terminal=true
Categories=Development;Programming;
EOF
    
    # Create desktop file for IDE (if available)
    if [[ -f "$INSTALL_DIR/bin/xorlang-ide" ]]; then
        cat > "$DESKTOP_DIR/xorlang-ide.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=XorLang IDE
Comment=Integrated Development Environment for XorLang
Exec=xorlang-ide
Icon=xorlang
Terminal=false
Categories=Development;IDE;Programming;
EOF
        print_success "Created desktop files for CLI and IDE"
    else
        print_success "Created desktop file for CLI"
    fi
    
    # Update desktop database
    if command -v update-desktop-database &> /dev/null; then
        update-desktop-database "$DESKTOP_DIR"
        print_success "Updated desktop database"
    fi
}

# Function to create uninstall script
create_uninstall_script() {
    print_status "Creating uninstall script..."
    
    cat > "$INSTALL_DIR/uninstall.sh" << 'EOF'
#!/bin/bash

# XorLang Uninstaller

set -e

INSTALL_DIR="/opt/xorlang"
BIN_DIR="/usr/local/bin"
DESKTOP_DIR="/usr/share/applications"
ICON_DIR="/usr/share/icons/hicolor/256x256/apps"

echo "Uninstalling XorLang..."

# Remove symlinks
rm -f "$BIN_DIR/xorlang"
rm -f "$BIN_DIR/xorlang-ide"

# Remove desktop files
rm -f "$DESKTOP_DIR/xorlang.desktop"
rm -f "$DESKTOP_DIR/xorlang-ide.desktop"

# Remove icon
rm -f "$ICON_DIR/xorlang.png"

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$DESKTOP_DIR"
fi

# Remove installation directory
rm -rf "$INSTALL_DIR"

echo "XorLang has been uninstalled successfully."
EOF
    
    chmod +x "$INSTALL_DIR/uninstall.sh"
    print_success "Uninstall script created: $INSTALL_DIR/uninstall.sh"
}

# Function to set permissions
set_permissions() {
    print_status "Setting file permissions..."
    
    # Set ownership to root:root if running as root
    if [[ $EUID -eq 0 ]]; then
        chown -R root:root "$INSTALL_DIR"
    fi
    
    # Set executable permissions
    chmod +x "$INSTALL_DIR/bin/"*
    chmod +x "$INSTALL_DIR/uninstall.sh"
    
    # Set read permissions for documentation
    chmod 644 "$INSTALL_DIR/docs/"*
    
    print_success "Permissions set successfully."
}

# Function to verify installation
verify_installation() {
    print_status "Verifying installation..."
    
    # Check if executables are accessible
    if command -v xorlang &> /dev/null; then
        print_success "xorlang command is available"
    else
        print_error "xorlang command is not available in PATH"
        return 1
    fi
    
    # Test xorlang version
    if xorlang --version &> /dev/null; then
        print_success "XorLang is working correctly"
    else
        print_error "XorLang is not working correctly"
        return 1
    fi
    
    print_success "Installation verification completed."
}

# Function to display installation summary
show_summary() {
    echo
    echo "=========================================="
    echo "XorLang v$APP_VERSION Installation Complete"
    echo "=========================================="
    echo
    echo "Installation Directory: $INSTALL_DIR"
    echo "Executables:"
    echo "  - xorlang (CLI interpreter)"
    if [[ -f "$INSTALL_DIR/bin/xorlang-ide" ]]; then
        echo "  - xorlang-ide (Integrated Development Environment)"
    fi
    echo
    echo "Documentation: $INSTALL_DIR/docs/"
    echo "Standard Library: $INSTALL_DIR/stdlib/"
    echo
    echo "Usage Examples:"
    echo "  xorlang --version                    # Check version"
    echo "  xorlang script.xor                   # Run a script"
    echo "  xorlang -i                           # Start interactive mode"
    echo "  xorlang -c 'print(\"Hello World\")'  # Execute code"
    echo
    if [[ -f "$INSTALL_DIR/bin/xorlang-ide" ]]; then
        echo "IDE Usage:"
        echo "  xorlang-ide                       # Start the IDE"
    fi
    echo
    echo "To uninstall, run: $INSTALL_DIR/uninstall.sh"
    echo
    print_success "Installation completed successfully!"
}

# Main installation function
main() {
    echo "=========================================="
    echo "XorLang v$APP_VERSION Linux Installer"
    echo "=========================================="
    echo
    
    check_root
    check_requirements
    create_directories
    copy_files
    create_symlinks
    create_desktop_files
    create_uninstall_script
    set_permissions
    verify_installation
    show_summary
}

# Run main function
main "$@"
