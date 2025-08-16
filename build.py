import PyInstaller.__main__
import os
import shutil
import platform

# The name of your application
APP_NAME = "xorlang"

# The entry point of your application
ENTRY_POINT = os.path.join("src", "xorlang", "cli.py")

# Path to the standard library
STDLIB_PATH = os.path.join("src", "xorlang", "stdlib")


ICON = os.path.join("src", "xorlang", "x.ico")


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


def main():
    """Main build script function."""
    build_os = get_build_os()
    if build_os == "unknown":
        print(f"Unsupported operating system: {platform.system()}")
        return

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

    print(f"Running PyInstaller for CLI...")
    try:
        PyInstaller.__main__.run(cli_options)
        print(f"\nCLI build successful! Executable: {os.path.join('dist', APP_NAME)}")
    except Exception as e:
        print(f"\nAn error occurred during the CLI build: {e}")
        return

    # --- Build IDE (Windowed App) ---
    ide_entry_point = os.path.join("src", "xorlang", "ide.py")
    ide_app_name = f"{APP_NAME}-ide"
    ide_options = [
        '--name=%s' % ide_app_name,
        '--onefile',
        '--windowed',  # Use --windowed for GUI apps
        f'--add-data={STDLIB_PATH}{path_separator}xorlang/stdlib',
        ide_entry_point,
    ]

    print(f"\nRunning PyInstaller for IDE...")
    try:
        PyInstaller.__main__.run(ide_options)
        print(f"\nIDE build successful! Executable: {os.path.join('dist', ide_app_name)}")
    except Exception as e:
        print(f"\nAn error occurred during the IDE build: {e}")
        return

    # Optional: Clean up temporary build files
    print("Cleaning up temporary build files...")
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists(f'{APP_NAME}.spec'):
        os.remove(f'{APP_NAME}.spec')
    print("Cleanup complete.")


if __name__ == '__main__':
    main()
