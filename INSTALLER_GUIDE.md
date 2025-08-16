# XorLang v2.0.0 Installer Guide

This guide explains how to build and use the XorLang installers for Windows and Linux.

## Overview

XorLang v2.0.0 provides automated installer creation for both Windows and Linux platforms. The installers package the XorLang interpreter, IDE, standard library, and documentation for easy distribution and installation.

## Prerequisites

### For Building Installers

#### Windows
- Python 3.8 or higher
- PyInstaller (`pip install PyInstaller`)
- NSIS (for Windows installer creation) - [Download here](https://nsis.sourceforge.io/)

#### Linux
- Python 3.8 or higher
- pip3
- tar (usually pre-installed)
- ImageMagick (optional, for icon conversion)

### For Using Installers

#### Windows
- Windows 7 or later
- Administrator privileges (for installation)

#### Linux
- Linux distribution with bash shell
- sudo privileges (for installation)

## Building Installers

### Quick Start

#### Windows
```batch
# Run the Windows build script
build_windows.bat
```

#### Linux
```bash
# Run the Linux build script
./build_linux.sh
```

### Manual Build Process

If you prefer to run the build manually:

```bash
# Install PyInstaller if not already installed
pip install PyInstaller

# Run the build script
python build_with_installers.py
```

### What Gets Built

The build process creates:

1. **Executables** (in `dist/` directory):
   - `xorlang` / `xorlang.exe` - Command-line interpreter
   - `xorlang-ide` / `xorlang-ide.exe` - Integrated Development Environment

2. **Windows Installer** (in `installer/windows/`):
   - `XorLang-2.0.0-Setup.exe` - NSIS-based installer

3. **Linux Package** (in `installer/linux/`):
   - `xorlang-2.0.0-linux.tar.gz` - Compressed package with install script

## Using the Installers

### Windows Installation

#### Method 1: Using the Installer
1. Download `XorLang-2.0.0-Setup.exe`
2. Run the installer as Administrator
3. Follow the installation wizard
4. Choose installation options:
   - **Main Application** (required)
   - **Start Menu Shortcuts** (recommended)
   - **Desktop Shortcuts** (optional)
   - **Add to PATH** (recommended)

#### Method 2: Manual Installation
1. Extract the executable files
2. Copy to a directory (e.g., `C:\Program Files\XorLang`)
3. Add the directory to your system PATH
4. Create shortcuts manually if desired

### Linux Installation

#### Method 1: Using the Package
```bash
# Extract the package
tar -xzf xorlang-2.0.0-linux.tar.gz

# Run the installer
sudo ./xorlang-2.0.0/install_xorlang.sh
```

#### Method 2: Manual Installation
```bash
# Copy executables to /opt/xorlang/bin
sudo mkdir -p /opt/xorlang/bin
sudo cp xorlang xorlang-ide /opt/xorlang/bin/

# Copy standard library
sudo cp -r stdlib /opt/xorlang/

# Create symlinks
sudo ln -sf /opt/xorlang/bin/xorlang /usr/local/bin/xorlang
sudo ln -sf /opt/xorlang/bin/xorlang-ide /usr/local/bin/xorlang-ide
```

## Installer Features

### Windows Installer Features

- **Modern UI**: Professional installation wizard
- **Registry Integration**: Proper Windows registry entries
- **Start Menu Integration**: Automatic shortcut creation
- **Desktop Shortcuts**: Optional desktop icons
- **PATH Integration**: Automatic PATH environment variable setup
- **Uninstall Support**: Complete uninstallation through Control Panel
- **File Association**: (Future feature) Associate .xor files with XorLang

### Linux Installer Features

- **System Integration**: Installs to `/opt/xorlang` following Linux conventions
- **PATH Integration**: Creates symlinks in `/usr/local/bin`
- **Desktop Integration**: Creates desktop application entries
- **Icon Support**: Converts and installs application icons
- **Permission Management**: Proper file permissions and ownership
- **Uninstall Script**: Complete uninstallation script provided
- **Package Management**: Creates compressed package for distribution

## Installation Locations

### Windows
- **Installation Directory**: `C:\Program Files\XorLang\` (default)
- **Executables**: `C:\Program Files\XorLang\xorlang.exe`
- **Standard Library**: `C:\Program Files\XorLang\stdlib\`
- **Documentation**: `C:\Program Files\XorLang\docs\`

### Linux
- **Installation Directory**: `/opt/xorlang/`
- **Executables**: `/opt/xorlang/bin/xorlang`
- **Standard Library**: `/opt/xorlang/stdlib/`
- **Documentation**: `/opt/xorlang/docs/`
- **Symlinks**: `/usr/local/bin/xorlang`

## Verification

After installation, verify that XorLang is working correctly:

### Windows
```cmd
# Check version
xorlang --version

# Test interactive mode
xorlang -i

# Run a test script
echo print("Hello, XorLang!") > test.xor
xorlang test.xor
```

### Linux
```bash
# Check version
xorlang --version

# Test interactive mode
xorlang -i

# Run a test script
echo 'print("Hello, XorLang!")' > test.xor
xorlang test.xor
```

## Uninstallation

### Windows
1. Go to Control Panel > Programs and Features
2. Find "XorLang 2.0.0"
3. Click "Uninstall"
4. Follow the uninstallation wizard

### Linux
```bash
# Run the uninstall script
sudo /opt/xorlang/uninstall.sh
```

## Troubleshooting

### Common Issues

#### Windows
- **"Access Denied"**: Run installer as Administrator
- **"Not found in PATH"**: Restart command prompt after installation
- **"Missing DLL"**: Install Visual C++ Redistributable

#### Linux
- **"Permission denied"**: Use `sudo` for installation
- **"Command not found"**: Check if symlinks were created correctly
- **"Icon not found"**: Install ImageMagick for icon conversion

### Build Issues

#### PyInstaller Errors
```bash
# Clean PyInstaller cache
rm -rf build/ dist/ *.spec

# Reinstall PyInstaller
pip uninstall PyInstaller
pip install PyInstaller
```

#### NSIS Errors (Windows)
- Ensure NSIS is installed and `makensis` is in PATH
- Check NSIS script syntax
- Verify file paths in the script

#### Icon Conversion Errors (Linux)
- Install ImageMagick: `sudo apt-get install imagemagick`
- Check icon file format and permissions

## Customization

### Modifying Installer Behavior

#### Windows (NSIS Script)
Edit `installer/windows/xorlang_installer.nsi`:
- Change installation directory
- Modify registry entries
- Add custom installation steps
- Change installer branding

#### Linux (Bash Script)
Edit `installer/linux/install_xorlang.sh`:
- Change installation paths
- Modify system integration
- Add custom dependencies
- Change package structure

### Adding Custom Files
1. Modify the build script to include additional files
2. Update installer scripts to copy custom files
3. Test the installation process

## Distribution

### Windows Distribution
- Distribute `XorLang-2.0.0-Setup.exe`
- File size: ~10-20 MB (depending on dependencies)
- Compatible with Windows 7 and later

### Linux Distribution
- Distribute `xorlang-2.0.0-linux.tar.gz`
- File size: ~5-15 MB (depending on dependencies)
- Compatible with most Linux distributions

### Package Managers (Future)
- **Windows**: Chocolatey, Scoop packages
- **Linux**: Debian/Ubuntu packages, RPM packages
- **macOS**: Homebrew formula

## Security Considerations

### Windows
- Installer requires Administrator privileges
- Files are installed to Program Files (protected location)
- Registry entries are properly managed

### Linux
- Installer requires sudo privileges
- Files are installed to /opt (standard location)
- Proper file permissions are set
- Symlinks are created in system directories

## Support

For issues with the installers:

1. Check the troubleshooting section above
2. Verify system requirements
3. Check build logs for errors
4. Test on a clean system
5. Report issues with detailed system information

## Future Enhancements

### Planned Features
- **Silent Installation**: Command-line installation options
- **Custom Installations**: Selective component installation
- **Auto-Updates**: Built-in update mechanism
- **Multi-Language Support**: Localized installers
- **Digital Signatures**: Code signing for Windows
- **Package Manager Integration**: Official packages for major distributions

### Contributing
To contribute to installer development:
1. Fork the repository
2. Make your changes
3. Test thoroughly on target platforms
4. Submit a pull request with detailed description

---

**XorLang v2.0.0** - Professional installation experience for all platforms.
