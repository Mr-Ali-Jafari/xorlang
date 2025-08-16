# XorLang Installation Guide

Complete installation guide for XorLang Programming Language v2.1.0 with IDE support.

## Table of Contents

- [System Requirements](#system-requirements)
- [Installation Methods](#installation-methods)
- [Quick Installation](#quick-installation)
- [Manual Installation](#manual-installation)
- [Verification](#verification)
- [Desktop Integration](#desktop-integration)
- [Uninstallation](#uninstallation)
- [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements
- **Operating System**: Linux (Ubuntu 18.04+, CentOS 7+, Debian 9+, or equivalent)
- **Architecture**: x86_64 (64-bit)
- **RAM**: 512 MB minimum, 1 GB recommended
- **Disk Space**: 100 MB for installation
- **Privileges**: Root access (sudo) for system-wide installation

### Supported Linux Distributions
- Ubuntu 18.04 LTS and newer
- Debian 9 (Stretch) and newer
- CentOS 7 and newer
- Fedora 28 and newer
- openSUSE Leap 15.0 and newer
- Arch Linux (current)

## Installation Methods

XorLang offers two installation methods:

1. **Enhanced Installer** (Recommended) - Automated installation with desktop integration
2. **Manual Installation** - Step-by-step manual setup

## Quick Installation

### Method 1: Enhanced Installer (Recommended)

The enhanced installer provides automatic installation with desktop integration, icon support, and comprehensive logging.

```bash
# Navigate to XorLang directory
cd /path/to/xorlang

# Run the enhanced installer
sudo ./install_to_opt.sh
```

#### Installation Options

```bash
# Standard installation
sudo ./install_to_opt.sh

# Force reinstall over existing installation
sudo ./install_to_opt.sh --force

# Verbose installation with detailed output
sudo ./install_to_opt.sh --verbose

# Skip backup creation during reinstall
sudo ./install_to_opt.sh --skip-backup

# Show help and all options
./install_to_opt.sh --help
```

### Method 2: From Release Package

```bash
# Download latest release
wget https://github.com/Mr-Ali-Jafari/Xorlang/releases/latest/download/xorlang-linux-installer-2.1.0.tar.gz

# Extract package
tar -xzf xorlang-linux-installer-2.1.0.tar.gz
cd xorlang-linux-installer-2.1.0

# Run installer
sudo ./install_xorlang.sh
```

## Manual Installation

If you prefer manual installation or need custom setup:

### Step 1: Build from Source

```bash
# Clone repository
git clone https://github.com/Mr-Ali-Jafari/Xorlang.git
cd Xorlang

# Install dependencies
pip install -r requirements.txt

# Build executables
python build.py
```

### Step 2: Manual System Installation

```bash
# Create installation directory
sudo mkdir -p /opt/xorlang

# Copy executables
sudo cp dist/xorlang /opt/xorlang/
sudo cp dist/xorlang-ide /opt/xorlang/
sudo chmod +x /opt/xorlang/xorlang
sudo chmod +x /opt/xorlang/xorlang-ide

# Create system-wide symlinks
sudo ln -sf /opt/xorlang/xorlang /usr/local/bin/xorlang
sudo ln -sf /opt/xorlang/xorlang-ide /usr/local/bin/xorlang-ide

# Install icon (optional)
sudo cp src/xorlang/X.ico /usr/share/pixmaps/xorlang.ico
```

### Step 3: Desktop Integration (Optional)

```bash
# Create desktop entry for IDE
sudo tee /usr/share/applications/xorlang-ide.desktop > /dev/null << EOF
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

# Create MIME type for .xor files
sudo tee /usr/share/mime/packages/xorlang.xml > /dev/null << EOF
<?xml version="1.0" encoding="UTF-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
    <mime-type type="text/x-xorlang">
        <comment>XorLang source code</comment>
        <icon name="xorlang"/>
        <glob pattern="*.xor"/>
        <glob pattern="*.xorlang"/>
    </mime-type>
</mime-info>
EOF

# Update system databases
sudo update-mime-database /usr/share/mime
sudo update-desktop-database /usr/share/applications
```

## Verification

### Test Installation

```bash
# Check CLI version
xorlang --version

# Check CLI help
xorlang --help

# Test interactive mode
xorlang -i

# Start IDE
xorlang-ide
```

### Expected Output

```bash
$ xorlang --version
XorLang v2.1.0

$ xorlang --help
XorLang Programming Language v2.1.0

Usage: xorlang [options] [file]

Options:
  -h, --help     Show this help message
  -v, --version  Show version information
  -i, --interactive  Start interactive mode (REPL)
  -c, --command  Execute command directly
```

### Verify Desktop Integration

1. **Applications Menu**: Look for "XorLang IDE" in your applications menu
2. **File Association**: Right-click a `.xor` file → "Open with" → Should show XorLang IDE
3. **Icon Display**: XorLang applications should display the custom icon

## Desktop Integration

The enhanced installer automatically sets up:

### File Associations
- `.xor` files open with XorLang IDE by default
- `.xorlang` files also supported

### Applications Menu
- XorLang IDE appears in Development category
- Searchable by keywords: xorlang, programming, development, ide

### Custom Icon
- Custom XorLang icon for all applications
- Consistent branding across desktop environment

### MIME Types
- Proper file type recognition
- Integration with file managers

## Uninstallation

### Method 1: Enhanced Uninstaller (Recommended)

```bash
# Navigate to XorLang directory
cd /path/to/xorlang

# Run uninstaller
sudo ./uninstall_xorlang.sh
```

#### Uninstaller Options

```bash
# Interactive uninstallation (recommended)
sudo ./uninstall_xorlang.sh

# Preview what will be removed (dry run)
sudo ./uninstall_xorlang.sh --dry-run

# Force removal without confirmation
sudo ./uninstall_xorlang.sh --force

# Skip backup creation
sudo ./uninstall_xorlang.sh --no-backup

# Verbose uninstallation
sudo ./uninstall_xorlang.sh --verbose

# Show help
./uninstall_xorlang.sh --help
```

### Method 2: Manual Uninstallation

```bash
# Remove installation directory
sudo rm -rf /opt/xorlang

# Remove symlinks
sudo rm -f /usr/local/bin/xorlang
sudo rm -f /usr/local/bin/xorlang-ide

# Remove desktop integration
sudo rm -f /usr/share/pixmaps/xorlang.ico
sudo rm -f /usr/share/applications/xorlang*.desktop
sudo rm -f /usr/share/mime/packages/xorlang.xml

# Update system databases
sudo update-mime-database /usr/share/mime
sudo update-desktop-database /usr/share/applications
```

## Troubleshooting

### Common Issues

#### 1. Permission Denied
```bash
# Error: Permission denied
# Solution: Run with sudo
sudo ./install_to_opt.sh
```

#### 2. Command Not Found After Installation
```bash
# Error: xorlang: command not found
# Solution: Check PATH or use full path
/usr/local/bin/xorlang --version

# Or restart terminal/shell
source ~/.bashrc
```

#### 3. Installation Hangs at Validation
```bash
# Error: Installer stops at "Validating source files..."
# Solution: Check if dist/ directory exists and contains executables
ls -la dist/

# If missing, build first:
python build.py
```

#### 4. Desktop Integration Not Working
```bash
# Error: .xor files don't open with XorLang IDE
# Solution: Update MIME database manually
sudo update-mime-database /usr/share/mime
sudo update-desktop-database /usr/share/applications

# Log out and log back in
```

#### 5. Icon Not Displaying
```bash
# Error: Applications show generic icon
# Solution: Check icon installation
ls -la /usr/share/pixmaps/xorlang.ico

# If missing, copy manually:
sudo cp src/xorlang/X.ico /usr/share/pixmaps/xorlang.ico
```

### Log Files

Installation and uninstallation create detailed log files:

```bash
# Installation logs
/tmp/xorlang-install-YYYYMMDD-HHMMSS.log

# Uninstallation logs
/tmp/xorlang-uninstall-YYYYMMDD-HHMMSS.log

# View recent installation log
ls -t /tmp/xorlang-install-*.log | head -1 | xargs cat
```

### Getting Help

1. **Check log files** for detailed error information
2. **Run with verbose mode** for more detailed output
3. **Use dry-run mode** to preview actions without executing
4. **Check system requirements** and compatibility
5. **Report issues** on GitHub with log files

### System Compatibility

If you encounter issues on your Linux distribution:

1. **Check kernel version**: `uname -r`
2. **Check glibc version**: `ldd --version`
3. **Check available space**: `df -h /opt`
4. **Check permissions**: `sudo -v`

### Clean Reinstallation

For a completely clean reinstallation:

```bash
# 1. Uninstall completely
sudo ./uninstall_xorlang.sh --force

# 2. Verify removal
xorlang --version  # Should show "command not found"

# 3. Clean build (if building from source)
rm -rf dist/
python build.py

# 4. Fresh installation
sudo ./install_to_opt.sh
```

## Advanced Configuration

### Custom Installation Directory

To install to a custom directory, modify the installer:

```bash
# Edit install_to_opt.sh
# Change: readonly INSTALL_DIR="/opt/xorlang"
# To:     readonly INSTALL_DIR="/your/custom/path"
```

### User-Only Installation

For user-only installation without system-wide access:

```bash
# Create user directories
mkdir -p ~/.local/bin
mkdir -p ~/.local/share/applications

# Copy executables
cp dist/xorlang ~/.local/bin/
cp dist/xorlang-ide ~/.local/bin/
chmod +x ~/.local/bin/xorlang*

# Add to PATH (add to ~/.bashrc)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## Support

For additional support:

- **Documentation**: [XorLang Documentation](https://github.com/Mr-Ali-Jafari/Xorlang/wiki)
- **Issues**: [GitHub Issues](https://github.com/Mr-Ali-Jafari/Xorlang/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Mr-Ali-Jafari/Xorlang/discussions)

---

**XorLang v2.1.0** - Modern programming language with comprehensive tooling.
