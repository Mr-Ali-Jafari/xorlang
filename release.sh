#!/bin/bash

# XorLang Release Script
# This script commits changes, pushes to GitHub, and creates a new release
# which triggers automated builds for Windows, Linux, and macOS

set -e  # Exit on any error

# Configuration
VERSION="1.0.1"
RELEASE_TITLE="XorLang v${VERSION}"
RELEASE_NOTES="## XorLang v${VERSION}

### ✅ Features
- Cross-platform XorLang interpreter and IDE
- Zero-dependency GUI standard library (tkinter backend)
- Zero-dependency HTTP standard library (http.client backend)
- Complete object-oriented programming support
- VS Code syntax highlighting extension

### 🔧 Fixes
- Fixed import errors in PyInstaller bundled executables
- Resolved standard library path resolution issues
- Added missing HTTP standard library
- Fixed circular dependency issues with type hints

### 📦 Downloads
- **Windows**: Download \`XorLang-Setup.exe\` for easy installation with Start Menu shortcuts
- **Linux**: Download \`xorlang-linux.tar.gz\` 
- **macOS**: Download \`xorlang-macos.tar.gz\`

### 🚀 Quick Start
\`\`\`bash
# Run XorLang programs
xorlang your_program.xor

# Launch XorLang IDE
xorlang-ide
\`\`\`"

echo "🚀 XorLang Release Script v${VERSION}"
echo "======================================"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Check if there are any changes to commit
if git diff-index --quiet HEAD --; then
    echo "ℹ️  No changes to commit"
else
    echo "📝 Committing changes..."
    git add .
    git commit -m "Release v${VERSION}: Cross-platform builds with Windows installer

- Fixed import errors in PyInstaller bundled executables
- Added missing HTTP standard library
- Implemented GitHub Actions for automated cross-platform builds
- Created Windows installer with Inno Setup
- Added VS Code extension and comprehensive documentation"
fi

# Push changes to remote
echo "📤 Pushing changes to remote..."
git push origin main || git push origin master

# Create and push the tag
echo "🏷️  Creating release tag v${VERSION}..."
git tag -a "v${VERSION}" -m "${RELEASE_TITLE}"
git push origin "v${VERSION}"

echo "🎉 Release tag v${VERSION} created and pushed!"
echo ""
echo "📋 Next steps:"
echo "1. Go to your GitHub repository"
echo "2. Navigate to 'Releases'"
echo "3. You should see the new tag v${VERSION}"
echo "4. Click 'Create release from tag'"
echo "5. Use this title: ${RELEASE_TITLE}"
echo "6. Copy and paste the release notes below:"
echo ""
echo "=================================="
echo "${RELEASE_NOTES}"
echo "=================================="
echo ""
echo "7. Click 'Publish release'"
echo ""
echo "🤖 GitHub Actions will automatically:"
echo "   ✅ Build Windows executables (.exe)"
echo "   ✅ Create Windows installer (XorLang-Setup.exe)"
echo "   ✅ Build Linux executables"
echo "   ✅ Build macOS executables"
echo "   ✅ Upload all files to the release"
echo ""
echo "⏱️  Build process takes about 5-10 minutes"
echo "🔗 Check progress at: https://github.com/Mr-Ali-Jafari/Xorlang/actions"
echo ""
echo "🎯 Release v${VERSION} process initiated successfully!"
