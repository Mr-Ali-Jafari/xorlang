# XorLang Release Process

This document describes how to create releases for XorLang across multiple platforms.

## Automated Releases with GitHub Actions

The project includes a GitHub Actions workflow that automatically builds executables for Linux, Windows, and macOS when you create a release.

### Creating a Release

1. **Tag your release**:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

2. **Create a GitHub release**:
   - Go to your GitHub repository
   - Click "Releases" → "Create a new release"
   - Choose the tag you just created
   - Fill in release notes
   - Click "Publish release"

3. **Automatic builds**:
   - GitHub Actions will automatically build for all platforms
   - Executables will be uploaded to the release
   - Windows installer will be created and uploaded

### What Gets Built

- **Linux**: `xorlang-linux.tar.gz` containing CLI and IDE executables
- **Windows**: `xorlang-windows.zip` containing CLI and IDE executables + `XorLang-Setup.exe` installer
- **macOS**: `xorlang-macos.tar.gz` containing CLI and IDE executables

## Manual Local Builds

### Linux (Current System)
```bash
python build.py
# Creates: dist/xorlang and dist/xorlang-ide
```

### Windows (Requires Windows Machine)
```cmd
python build.py
# Creates: dist/xorlang.exe and dist/xorlang-ide.exe
```

### macOS (Requires macOS Machine)
```bash
python build.py
# Creates: dist/xorlang and dist/xorlang-ide
```

## Build Requirements

- Python 3.8+
- PyInstaller
- Virtual environment (recommended)

## Cross-Platform Compatibility

All builds include:
- XorLang CLI interpreter
- XorLang IDE (GUI)
- Complete standard library (gui, http, collections, string, object, prelude)
- Proper path resolution for bundled executables

## Troubleshooting

If builds fail:
1. Check that all dependencies are installed
2. Ensure virtual environment is activated
3. Verify Python version compatibility
4. Check GitHub Actions logs for detailed error messages
