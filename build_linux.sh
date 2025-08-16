#!/bin/bash

# XorLang v2.0.0 Linux Build Script
# This script builds XorLang and creates installers on Linux

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "=========================================="
echo "XorLang v2.0.0 Linux Build Script"
echo "=========================================="
echo

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

# Check if Python is available
print_status "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher and try again"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
print_success "Python $PYTHON_VERSION found"

# Check if pip is available
print_status "Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed"
    echo "Please install pip3 and try again"
    exit 1
fi

print_success "pip3 found"

# Check if PyInstaller is available
print_status "Checking PyInstaller..."
if ! python3 -c "import PyInstaller" &> /dev/null; then
    print_warning "PyInstaller not found. Installing..."
    pip3 install PyInstaller
    if [ $? -ne 0 ]; then
        print_error "Failed to install PyInstaller"
        exit 1
    fi
    print_success "PyInstaller installed"
else
    print_success "PyInstaller found"
fi

# Check if tar is available for creating Linux package
print_status "Checking tar..."
if ! command -v tar &> /dev/null; then
    print_error "tar is not installed"
    echo "Please install tar and try again"
    exit 1
fi

print_success "tar found"

# Check if ImageMagick is available for icon conversion
print_status "Checking ImageMagick..."
if ! command -v convert &> /dev/null; then
    print_warning "ImageMagick not found. Icon conversion will be skipped."
    echo "To enable icon conversion, install ImageMagick:"
    echo "  Ubuntu/Debian: sudo apt-get install imagemagick"
    echo "  CentOS/RHEL: sudo yum install ImageMagick"
    echo "  Arch: sudo pacman -S imagemagick"
else
    print_success "ImageMagick found"
fi

echo
print_status "Dependencies check completed."
echo

# Make the build script executable
chmod +x build_with_installers.py

# Run the build script
print_status "Starting build process..."
python3 build_with_installers.py

if [ $? -ne 0 ]; then
    echo
    print_error "Build failed! Check the error messages above."
    exit 1
fi

echo
echo "=========================================="
print_success "Build completed successfully!"
echo "=========================================="
echo
echo "Generated files:"
echo "  - CLI executable: dist/xorlang"
echo "  - IDE executable: dist/xorlang-ide"
if [ -f "installer/linux/xorlang-2.0.0-linux.tar.gz" ]; then
    echo "  - Linux package: installer/linux/xorlang-2.0.0-linux.tar.gz"
fi
echo
echo "Installation instructions:"
echo "  1. Extract the Linux package:"
echo "     tar -xzf installer/linux/xorlang-2.0.0-linux.tar.gz"
echo "  2. Run the installer:"
echo "     sudo ./xorlang-2.0.0/install_xorlang.sh"
echo
echo "You can now distribute these files to users."
