# XorLang Installation Guide

Complete installation guide for XorLang Programming Language v2.1.0 with comprehensive IDE support, desktop integration, and professional tooling.

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

The enhanced installer (`install_to_opt.sh` v2.1.0) provides:
- **Automatic installation** with comprehensive error handling
- **Desktop integration** with file associations and MIME types
- **Icon support** using the custom XorLang icon (`X.ico`)
- **Comprehensive logging** with timestamped logs in `/tmp/`
- **Backup functionality** for existing installations
- **System validation** including disk space and dependency checks

```bash
# Navigate to XorLang directory
cd /path/to/xorlang

# Build executables first (if not already built)
python build.py

# Run the enhanced installer
sudo ./install_to_opt.sh
```

#### What the Enhanced Installer Does

1. **System Requirements Check**
   - Verifies root privileges (sudo)
   - Checks available disk space (minimum 100MB)
   - Validates required system commands

2. **Source File Validation**
   - Confirms `dist/xorlang` and `dist/xorlang-ide` exist
   - Verifies executables are not corrupted
   - Checks for icon file `src/xorlang/X.ico`

3. **Installation Process**
   - Creates `/opt/xorlang/` directory
   - Copies executables with proper permissions
   - Creates symlinks in `/usr/local/bin/`
   - Installs icon to `/usr/share/pixmaps/xorlang.ico`

4. **Desktop Integration**
   - Creates desktop entries for both CLI and IDE
   - Sets up MIME types for `.xor` and `.xorlang` files
   - Updates system databases for immediate recognition

5. **Verification**
   - Tests executable functionality
   - Confirms all files are properly installed
   - Provides installation summary with paths

#### Installation Options

```bash
# Standard installation
sudo ./install_to_opt.sh

# Force reinstall over existing installation
sudo ./install_to_opt.sh --force

# Verbose installation with detailed debug output
sudo ./install_to_opt.sh --verbose

# Skip backup creation during reinstall (faster)
sudo ./install_to_opt.sh --skip-backup

# Force reinstall with verbose output (recommended for troubleshooting)
sudo ./install_to_opt.sh --force --verbose

# Show comprehensive help with all options
./install_to_opt.sh --help
```

#### Installation Locations

The enhanced installer creates the following structure:

```
/opt/xorlang/
├── xorlang          # CLI executable
└── xorlang-ide      # IDE executable

/usr/local/bin/
├── xorlang -> /opt/xorlang/xorlang
└── xorlang-ide -> /opt/xorlang/xorlang-ide

/usr/share/pixmaps/
└── xorlang.ico      # Application icon

/usr/share/applications/
├── xorlang.desktop      # CLI desktop entry
└── xorlang-ide.desktop  # IDE desktop entry

/usr/share/mime/packages/
└── xorlang.xml      # MIME type definitions
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

# Install Python dependencies
pip install -r requirements.txt

# Build executables using PyInstaller
python build.py
```

#### Build Process Details

The `build.py` script:
- Uses **PyInstaller** to create standalone executables
- Builds both `xorlang` (CLI) and `xorlang-ide` (GUI) executables
- Includes the **stdlib** (standard library) in the build
- Creates executables in the `dist/` directory
- Handles platform-specific optimizations for Linux
- Includes the icon file (`X.ico`) for the IDE

#### Build Requirements

- **Python 3.8+** with pip
- **PyInstaller** (installed via requirements.txt)
- **Tkinter** (for IDE GUI) - usually included with Python
- **Linux development tools** (gcc, make) - for some Python packages

#### Expected Build Output

```
dist/
├── xorlang          # CLI executable (~12-13MB)
└── xorlang-ide      # IDE executable (~13-14MB)
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

The dedicated uninstaller (`uninstall_xorlang.sh` v2.1.0) provides:
- **Complete removal** of all XorLang files and integration
- **Safety features** with backup creation and confirmation prompts
- **Dry-run mode** to preview what will be removed
- **Comprehensive logging** with detailed removal tracking
- **System cleanup** including database updates

```bash
# Navigate to XorLang directory
cd /path/to/xorlang

# Run interactive uninstaller (recommended)
sudo ./uninstall_xorlang.sh
```

#### What the Uninstaller Removes

The uninstaller completely removes:

1. **Installation Directory**
   - `/opt/xorlang/` (entire directory)

2. **System Symlinks**
   - `/usr/local/bin/xorlang`
   - `/usr/local/bin/xorlang-ide`

3. **Desktop Integration**
   - `/usr/share/applications/xorlang.desktop`
   - `/usr/share/applications/xorlang-ide.desktop`
   - `/usr/share/mime/packages/xorlang.xml`

4. **Visual Assets**
   - `/usr/share/pixmaps/xorlang.ico`

5. **Documentation** (if installed)
   - `/usr/share/doc/xorlang/`
   - `/usr/share/man/man1/xorlang.1`
   - `/usr/share/man/man1/xorlang-ide.1`

6. **System Database Updates**
   - MIME database refresh
   - Desktop database refresh
   - Manual page database refresh

#### Uninstaller Options

```bash
# Interactive uninstallation with confirmation prompts (recommended)
sudo ./uninstall_xorlang.sh

# Preview what will be removed without actually removing (safe)
sudo ./uninstall_xorlang.sh --dry-run

# Force removal without any confirmation prompts
sudo ./uninstall_xorlang.sh --force

# Skip backup creation (faster, but less safe)
sudo ./uninstall_xorlang.sh --no-backup

# Verbose uninstallation with detailed debug output
sudo ./uninstall_xorlang.sh --verbose

# Combine options for different scenarios
sudo ./uninstall_xorlang.sh --force --verbose    # Fast removal with details
sudo ./uninstall_xorlang.sh --dry-run --verbose  # Detailed preview

# Show comprehensive help with all options
./uninstall_xorlang.sh --help
```

#### Uninstaller Safety Features

1. **Backup Creation**
   - Creates backup in `/tmp/xorlang-uninstall-backup-YYYYMMDD-HHMMSS/`
   - Preserves all removed files for recovery
   - Can be disabled with `--no-backup`

2. **Confirmation Prompts**
   - Shows preview of what will be removed
   - Requires explicit "yes" confirmation
   - Can be bypassed with `--force`

3. **Dry Run Mode**
   - Shows exactly what would be removed
   - No actual file removal performed
   - Perfect for verification before real removal

4. **Comprehensive Logging**
   - Logs all actions to `/tmp/xorlang-uninstall-YYYYMMDD-HHMMSS.log`
   - Tracks successful and failed removals
   - Useful for troubleshooting

5. **Verification**
   - Confirms complete removal after uninstallation
   - Reports any remaining files
   - Provides final status summary

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
