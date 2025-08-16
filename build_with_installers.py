#!/usr/bin/env python3
"""
XorLang v2.0.0 Build and Installer Creation Script

This script builds XorLang executables and creates installers for Windows and Linux.
"""

import PyInstaller.__main__
import os
import shutil
import platform
import subprocess
import sys
from pathlib import Path

# Configuration
APP_NAME = "xorlang"
APP_VERSION = "2.0.0"
ENTRY_POINT = os.path.join("src", "xorlang", "cli.py")
IDE_ENTRY_POINT = os.path.join("src", "xorlang", "ide.py")
STDLIB_PATH = os.path.join("src", "xorlang", "stdlib")
ICON = os.path.join("src", "xorlang", "x.ico")

# Installer paths
INSTALLER_DIR = "installer"
WINDOWS_INSTALLER_DIR = os.path.join(INSTALLER_DIR, "windows")
LINUX_INSTALLER_DIR = os.path.join(INSTALLER_DIR, "linux")


def get_build_os():
    """Determines the current operating system for build purposes."""
    system = platform.system()
    if system == "Windows":
        return "win"
    elif system == "Linux":
        return "linux"
    elif system == "Darwin":
        return "mac"
    return "unknown"


def create_directories():
    """Create necessary directories for the build process."""
    directories = [
        "dist",
        INSTALLER_DIR,
        WINDOWS_INSTALLER_DIR,
        LINUX_INSTALLER_DIR
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")


def build_executables():
    """Build the XorLang executables using PyInstaller."""
    build_os = get_build_os()
    if build_os == "unknown":
        print(f"Unsupported operating system: {platform.system()}")
        return False

    # PyInstaller uses ';' as a path separator on Windows, and ':' on other systems.
    path_separator = ';' if build_os == 'win' else ':'

    # --- Build CLI (Console App) ---
    cli_options = [
        '--name=%s' % APP_NAME,
        '--onefile',
        '--console',
        f'--add-data={STDLIB_PATH}{path_separator}xorlang/stdlib',
        f'--icon={ICON}',
        ENTRY_POINT,
    ]

    print(f"Building CLI executable...")
    try:
        PyInstaller.__main__.run(cli_options)
        print(f"CLI build successful! Executable: {os.path.join('dist', APP_NAME)}")
    except Exception as e:
        print(f"An error occurred during the CLI build: {e}")
        return False

    # --- Build IDE (Windowed App) ---
    ide_app_name = f"{APP_NAME}-ide"
    ide_options = [
        '--name=%s' % ide_app_name,
        '--onefile',
        '--windowed',  # Use --windowed for GUI apps
        f'--add-data={STDLIB_PATH}{path_separator}xorlang/stdlib',
        IDE_ENTRY_POINT,
    ]

    print(f"Building IDE executable...")
    try:
        PyInstaller.__main__.run(ide_options)
        print(f"IDE build successful! Executable: {os.path.join('dist', ide_app_name)}")
    except Exception as e:
        print(f"An error occurred during the IDE build: {e}")
        return False

    return True


def create_windows_installer():
    """Create Windows installer using NSIS."""
    print("Creating Windows installer...")
    
    # Check if NSIS is available
    try:
        subprocess.run(["makensis", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Warning: NSIS (makensis) not found. Windows installer creation skipped.")
        print("To create Windows installer, install NSIS and ensure 'makensis' is in PATH.")
        return False
    
    # Path to the NSIS script
    nsis_script = os.path.join(WINDOWS_INSTALLER_DIR, "xorlang_installer.nsi")
    
    if not os.path.exists(nsis_script):
        print(f"Error: NSIS script not found: {nsis_script}")
        return False
    
    try:
        # Run NSIS compiler
        result = subprocess.run(["makensis", nsis_script], 
                              cwd=WINDOWS_INSTALLER_DIR,
                              capture_output=True, 
                              text=True)
        
        if result.returncode == 0:
            print("Windows installer created successfully!")
            # Look for the created installer
            installer_files = list(Path(WINDOWS_INSTALLER_DIR).glob("XorLang-*.exe"))
            if installer_files:
                print(f"Installer location: {installer_files[0]}")
            return True
        else:
            print(f"Error creating Windows installer: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error running NSIS: {e}")
        return False


def create_linux_installer():
    """Create Linux installer package."""
    print("Creating Linux installer...")
    
    # Copy the install script to the installer directory
    install_script = os.path.join(LINUX_INSTALLER_DIR, "install_xorlang.sh")
    
    if not os.path.exists(install_script):
        print(f"Error: Linux install script not found: {install_script}")
        return False
    
    # Make the script executable
    try:
        os.chmod(install_script, 0o755)
        print("Linux install script made executable")
    except Exception as e:
        print(f"Warning: Could not make install script executable: {e}")
    
    # Create a simple package structure
    package_dir = os.path.join(LINUX_INSTALLER_DIR, "xorlang-package")
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    
    os.makedirs(package_dir)
    
    # Copy files to package
    if os.path.exists("dist/xorlang"):
        shutil.copy2("dist/xorlang", os.path.join(package_dir, "xorlang"))
    
    if os.path.exists("dist/xorlang-ide"):
        shutil.copy2("dist/xorlang-ide", os.path.join(package_dir, "xorlang-ide"))
    
    # Copy standard library
    stdlib_dest = os.path.join(package_dir, "stdlib")
    if os.path.exists(STDLIB_PATH):
        shutil.copytree(STDLIB_PATH, stdlib_dest)
    
    # Copy documentation
    docs_dest = os.path.join(package_dir, "docs")
    os.makedirs(docs_dest, exist_ok=True)
    
    for doc_file in ["README.md", "CHANGELOG.md", "PERFORMANCE_OPTIMIZATIONS.md"]:
        if os.path.exists(doc_file):
            shutil.copy2(doc_file, docs_dest)
    
    # Copy install script
    shutil.copy2(install_script, package_dir)
    
    # Create a simple README for the package
    package_readme = os.path.join(package_dir, "INSTALL.txt")
    with open(package_readme, 'w') as f:
        f.write("""XorLang v2.0.0 Linux Package

To install XorLang on Linux:

1. Extract this package to a temporary location
2. Run the installer script with sudo:
   sudo ./install_xorlang.sh

The installer will:
- Install XorLang to /opt/xorlang
- Create symlinks in /usr/local/bin
- Add desktop integration
- Create an uninstall script

For more information, see the documentation in the docs/ directory.
""")
    
    # Create a compressed archive
    try:
        import tarfile
        archive_name = f"xorlang-{APP_VERSION}-linux.tar.gz"
        archive_path = os.path.join(LINUX_INSTALLER_DIR, archive_name)
        
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(package_dir, arcname=f"xorlang-{APP_VERSION}")
        
        print(f"Linux package created: {archive_path}")
        return True
        
    except Exception as e:
        print(f"Error creating Linux package: {e}")
        return False


def cleanup_build_files():
    """Clean up temporary build files."""
    print("Cleaning up temporary build files...")
    
    # Remove PyInstaller build artifacts
    if os.path.exists('build'):
        shutil.rmtree('build')
        print("Removed build directory")
    
    # Remove .spec files
    for spec_file in [f'{APP_NAME}.spec', f'{APP_NAME}-ide.spec']:
        if os.path.exists(spec_file):
            os.remove(spec_file)
            print(f"Removed {spec_file}")
    
    print("Cleanup complete.")


def verify_build():
    """Verify that the build was successful."""
    print("Verifying build...")
    
    # Check if executables exist
    cli_executable = os.path.join("dist", APP_NAME)
    ide_executable = os.path.join("dist", f"{APP_NAME}-ide")
    
    if not os.path.exists(cli_executable):
        print(f"Error: CLI executable not found: {cli_executable}")
        return False
    
    print(f"✓ CLI executable found: {cli_executable}")
    
    if os.path.exists(ide_executable):
        print(f"✓ IDE executable found: {ide_executable}")
    else:
        print("⚠ IDE executable not found (this is optional)")
    
    # Check file sizes
    cli_size = os.path.getsize(cli_executable)
    print(f"✓ CLI executable size: {cli_size / (1024*1024):.1f} MB")
    
    if os.path.exists(ide_executable):
        ide_size = os.path.getsize(ide_executable)
        print(f"✓ IDE executable size: {ide_size / (1024*1024):.1f} MB")
    
    return True


def main():
    """Main build function."""
    print("=" * 50)
    print(f"XorLang v{APP_VERSION} Build and Installer Creation")
    print("=" * 50)
    print()
    
    # Create directories
    create_directories()
    
    # Build executables
    if not build_executables():
        print("Build failed. Exiting.")
        sys.exit(1)
    
    # Verify build
    if not verify_build():
        print("Build verification failed. Exiting.")
        sys.exit(1)
    
    # Create installers based on platform
    build_os = get_build_os()
    
    if build_os == "win":
        create_windows_installer()
    elif build_os == "linux":
        create_linux_installer()
    else:
        print(f"Installer creation not supported on {platform.system()}")
    
    # Cleanup
    cleanup_build_files()
    
    print()
    print("=" * 50)
    print("Build completed successfully!")
    print("=" * 50)
    print()
    print("Generated files:")
    print(f"  - CLI executable: dist/{APP_NAME}")
    print(f"  - IDE executable: dist/{APP_NAME}-ide")
    
    if build_os == "win":
        print("  - Windows installer: installer/windows/XorLang-2.0.0-Setup.exe")
    elif build_os == "linux":
        print("  - Linux package: installer/linux/xorlang-2.0.0-linux.tar.gz")
    
    print()
    print("Next steps:")
    print("  1. Test the executables")
    print("  2. Distribute the installers")
    print("  3. Update documentation if needed")


if __name__ == '__main__':
    main()
