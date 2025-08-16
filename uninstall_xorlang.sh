#!/bin/bash

# XorLang Enhanced Uninstaller
# Version: 2.0.0
# Author: XorLang Development Team
# Description: Complete uninstaller for XorLang IDE and CLI with logging and verification

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
readonly LOG_FILE="/tmp/xorlang-uninstall-$(date +%Y%m%d-%H%M%S).log"
readonly BACKUP_DIR="/tmp/xorlang-uninstall-backup-$(date +%Y%m%d-%H%M%S)"

# Global variables
FORCE_REMOVE=false
CREATE_BACKUP=true
VERBOSE=false
DRY_RUN=false

# Files and directories to remove
readonly SYSTEM_FILES=(
    "/opt/xorlang"
    "/usr/local/bin/xorlang"
    "/usr/local/bin/xorlang-ide"
    "/usr/share/pixmaps/xorlang.ico"
    "/usr/share/applications/xorlang.desktop"
    "/usr/share/applications/xorlang-ide.desktop"
    "/usr/share/mime/packages/xorlang.xml"
    "/usr/share/doc/xorlang"
    "/usr/share/man/man1/xorlang.1"
    "/usr/share/man/man1/xorlang-ide.1"
)

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
    echo -e "${RED}Uninstallation failed. Check log file: $LOG_FILE${NC}"
    exit 1
}

# Cleanup function
cleanup() {
    if [[ -d "$BACKUP_DIR" && "$CREATE_BACKUP" == true ]]; then
        log "INFO" "Backup created at: $BACKUP_DIR"
        echo -e "${CYAN}Backup available at: $BACKUP_DIR${NC}"
    fi
}

# Set up signal handlers
trap cleanup EXIT
trap 'error_exit "Uninstallation interrupted by user"' INT TERM

# Help function
show_help() {
    cat << EOF
${BOLD}XorLang Enhanced Uninstaller v$VERSION${NC}

${BOLD}USAGE:${NC}
    sudo ./uninstall_xorlang.sh [OPTIONS]

${BOLD}OPTIONS:${NC}
    -f, --force         Force removal without confirmation prompts
    -n, --no-backup     Skip creating backup of removed files
    -v, --verbose       Enable verbose output
    -d, --dry-run       Show what would be removed without actually removing
    -h, --help          Show this help message

${BOLD}EXAMPLES:${NC}
    sudo ./uninstall_xorlang.sh                 # Interactive uninstallation
    sudo ./uninstall_xorlang.sh --force         # Force uninstall without prompts
    sudo ./uninstall_xorlang.sh --dry-run       # Preview what will be removed
    sudo ./uninstall_xorlang.sh --verbose       # Verbose uninstallation

${BOLD}DESCRIPTION:${NC}
    This script completely removes XorLang IDE and CLI from your system, including:
    • Executables and installation directory
    • System-wide symlinks
    • Desktop entries and MIME types
    • Icons and documentation
    • Manual pages

EOF
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -f|--force)
                FORCE_REMOVE=true
                shift
                ;;
            -n|--no-backup)
                CREATE_BACKUP=false
                shift
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -d|--dry-run)
                DRY_RUN=true
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
    
    log "SUCCESS" "System requirements check passed"
}

# Check if XorLang is installed
check_installation() {
    log "INFO" "Checking for XorLang installation..."
    
    local found_files=()
    local missing_files=()
    
    for file in "${SYSTEM_FILES[@]}"; do
        if [[ -e "$file" ]]; then
            found_files+=("$file")
            log "DEBUG" "Found: $file"
        else
            missing_files+=("$file")
            log "DEBUG" "Not found: $file"
        fi
    done
    
    if [[ ${#found_files[@]} -eq 0 ]]; then
        log "INFO" "No XorLang installation found on this system"
        echo -e "${YELLOW}XorLang does not appear to be installed on this system.${NC}"
        exit 0
    fi
    
    log "INFO" "Found ${#found_files[@]} XorLang files/directories to remove"
    log "SUCCESS" "XorLang installation detected"
}

# Show what will be removed
show_removal_preview() {
    echo ""
    echo -e "${BOLD}${YELLOW}⚠️  REMOVAL PREVIEW${NC}"
    echo -e "${YELLOW}===================${NC}"
    echo ""
    echo -e "${BOLD}The following files and directories will be removed:${NC}"
    
    local count=0
    for file in "${SYSTEM_FILES[@]}"; do
        if [[ -e "$file" ]]; then
            ((count++))
            if [[ -d "$file" ]]; then
                echo -e "  ${RED}📁${NC} $file/ (directory)"
            elif [[ -L "$file" ]]; then
                echo -e "  ${CYAN}🔗${NC} $file (symlink)"
            else
                echo -e "  ${RED}📄${NC} $file"
            fi
        fi
    done
    
    echo ""
    echo -e "${BOLD}Total items to remove: ${RED}$count${NC}"
    echo ""
}

# Get user confirmation
get_confirmation() {
    if [[ "$FORCE_REMOVE" == true || "$DRY_RUN" == true ]]; then
        return 0
    fi
    
    echo -e "${BOLD}${RED}⚠️  WARNING: This will completely remove XorLang from your system!${NC}"
    echo ""
    read -p "Are you sure you want to continue? (yes/no): " -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        log "INFO" "Uninstallation cancelled by user"
        echo -e "${YELLOW}Uninstallation cancelled.${NC}"
        exit 0
    fi
    
    log "INFO" "User confirmed uninstallation"
}

# Create backup of files before removal
create_backup() {
    if [[ "$CREATE_BACKUP" == false || "$DRY_RUN" == true ]]; then
        log "INFO" "Skipping backup as requested"
        return 0
    fi
    
    log "INFO" "Creating backup of XorLang files..."
    mkdir -p "$BACKUP_DIR"
    
    local backup_count=0
    for file in "${SYSTEM_FILES[@]}"; do
        if [[ -e "$file" ]]; then
            local backup_path="$BACKUP_DIR$(dirname "$file")"
            mkdir -p "$backup_path"
            
            if cp -r "$file" "$backup_path/" 2>/dev/null; then
                ((backup_count++))
                log "DEBUG" "Backed up: $file"
            else
                log "WARN" "Failed to backup: $file"
            fi
        fi
    done
    
    if [[ $backup_count -gt 0 ]]; then
        log "SUCCESS" "Backup created with $backup_count items at $BACKUP_DIR"
    else
        log "WARN" "No files were backed up"
    fi
}

# Remove XorLang files
remove_xorlang() {
    if [[ "$DRY_RUN" == true ]]; then
        log "INFO" "DRY RUN: Would remove XorLang files (no actual removal performed)"
        return 0
    fi
    
    log "INFO" "Removing XorLang files and directories..."
    
    local removed_count=0
    local failed_count=0
    
    for file in "${SYSTEM_FILES[@]}"; do
        if [[ -e "$file" ]]; then
            log "INFO" "Removing: $file"
            
            if rm -rf "$file" 2>/dev/null; then
                ((removed_count++))
                log "SUCCESS" "Removed: $file"
            else
                ((failed_count++))
                log "ERROR" "Failed to remove: $file"
            fi
        fi
    done
    
    log "INFO" "Removal completed: $removed_count removed, $failed_count failed"
    
    if [[ $failed_count -gt 0 ]]; then
        log "WARN" "Some files could not be removed. Check permissions or manual removal may be required."
    fi
}

# Update system databases
update_system_databases() {
    if [[ "$DRY_RUN" == true ]]; then
        log "INFO" "DRY RUN: Would update system databases"
        return 0
    fi
    
    log "INFO" "Updating system databases..."
    
    # Update MIME database
    if command -v update-mime-database &> /dev/null; then
        log "INFO" "Updating MIME database..."
        if update-mime-database /usr/share/mime 2>/dev/null; then
            log "SUCCESS" "MIME database updated"
        else
            log "WARN" "Failed to update MIME database"
        fi
    fi
    
    # Update desktop database
    if command -v update-desktop-database &> /dev/null; then
        log "INFO" "Updating desktop database..."
        if update-desktop-database /usr/share/applications 2>/dev/null; then
            log "SUCCESS" "Desktop database updated"
        else
            log "WARN" "Failed to update desktop database"
        fi
    fi
    
    # Update manual page database
    if command -v mandb &> /dev/null; then
        log "INFO" "Updating manual page database..."
        if mandb -q 2>/dev/null; then
            log "SUCCESS" "Manual page database updated"
        else
            log "WARN" "Failed to update manual page database"
        fi
    fi
}

# Verify removal
verify_removal() {
    log "INFO" "Verifying removal..."
    
    local remaining_files=()
    for file in "${SYSTEM_FILES[@]}"; do
        if [[ -e "$file" ]]; then
            remaining_files+=("$file")
        fi
    done
    
    if [[ ${#remaining_files[@]} -eq 0 ]]; then
        log "SUCCESS" "All XorLang files successfully removed"
        return 0
    else
        log "WARN" "Some files still remain:"
        for file in "${remaining_files[@]}"; do
            log "WARN" "  - $file"
        done
        return 1
    fi
}

# Show uninstallation summary
show_summary() {
    echo ""
    if [[ "$DRY_RUN" == true ]]; then
        echo -e "${CYAN}${BOLD}📋 XorLang Uninstallation Preview Completed${NC}"
        echo -e "${CYAN}=========================================${NC}"
        echo ""
        echo -e "${BOLD}This was a dry run - no files were actually removed.${NC}"
        echo "Run without --dry-run to perform the actual uninstallation."
    else
        echo -e "${GREEN}${BOLD}✓ XorLang Uninstallation Completed Successfully!${NC}"
        echo -e "${BLUE}============================================${NC}"
    fi
    echo ""
    echo -e "${BOLD}Uninstallation Details:${NC}"
    echo "  • Log File: $LOG_FILE"
    [[ -d "$BACKUP_DIR" && "$CREATE_BACKUP" == true && "$DRY_RUN" == false ]] && echo "  • Backup Directory: $BACKUP_DIR"
    echo ""
    echo -e "${BOLD}Removed Components:${NC}"
    echo "  • XorLang CLI interpreter"
    echo "  • XorLang IDE application"
    echo "  • Desktop entries and file associations"
    echo "  • System icons and documentation"
    echo "  • Manual pages"
    echo ""
    if [[ "$DRY_RUN" == false ]]; then
        echo -e "${BOLD}Verification:${NC}"
        echo "  • Run 'xorlang --version' - should show 'command not found'"
        echo "  • Run 'xorlang-ide' - should show 'command not found'"
        echo "  • Check Applications menu - XorLang IDE should be gone"
    fi
    echo ""
}

# Main uninstallation function
main() {
    # Initialize logging
    echo "XorLang Enhanced Uninstaller v$VERSION - $(date)" > "$LOG_FILE"
    
    # Show header
    echo -e "${BLUE}${BOLD}XorLang Enhanced Uninstaller v$VERSION${NC}"
    echo -e "${BLUE}======================================${NC}"
    echo ""
    
    # Parse arguments
    parse_args "$@"
    
    # Run uninstallation steps
    check_requirements
    check_installation
    show_removal_preview
    get_confirmation
    create_backup
    remove_xorlang
    update_system_databases
    verify_removal
    show_summary
    
    if [[ "$DRY_RUN" == false ]]; then
        log "SUCCESS" "Uninstallation completed successfully"
    else
        log "INFO" "Dry run completed successfully"
    fi
}

# Run main function with all arguments
main "$@"
