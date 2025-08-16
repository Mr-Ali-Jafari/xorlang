#!/bin/bash

# XorLang Enhanced Uninstaller
# Version: 2.1.0
# Author: XorLang Development Team
# Description: Uninstalls XorLang, aligning with the enhanced installer's parameters.

set -euo pipefail # Exit on any error, undefined variables, and pipe failures

# --- Configuration ---
readonly VERSION="2.1.0"
readonly INSTALL_DIR="/opt/xorlang"
readonly LOG_FILE="/tmp/xorlang-uninstall-$(date +%Y%m%d-%H%M%S).log"
readonly BACKUP_DIR="/tmp/xorlang-backup-$(date +%Y%m%d-%H%M%S)" # Aligned with installer

# --- Colors ---
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly CYAN='\033[0;36m'
readonly BOLD='\033[1m'
readonly NC='\033[0m' # No Color

# --- Global Variables ---
FORCE=false
SKIP_BACKUP=false
VERBOSE=false
DRY_RUN=false

# --- Files to Remove ---
# This list should accurately reflect files created by install_to_opt.sh
readonly SYSTEM_FILES=(
    "${INSTALL_DIR}"
    "/usr/local/bin/xorlang"
    "/usr/local/bin/xorlang-ide"
    "/usr/share/pixmaps/xorlang.ico"
    "/usr/share/applications/xorlang.desktop"
    "/usr/share/applications/xorlang-ide.desktop"
    "/usr/share/mime/packages/xorlang.xml"
)

# --- Logging and Error Handling ---
log() {
    local level="$1" message="$2"
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" >>"$LOG_FILE"

    # Only print to stdout if VERBOSE is true or it's not a DEBUG message
    case "$level" in
        INFO) echo -e "${BLUE}[INFO]${NC} $message" ;; 
        WARN) echo -e "${YELLOW}[WARN]${NC} $message" ;; 
        ERROR) echo -e "${RED}[ERROR]${NC} $message" ;; 
        SUCCESS) echo -e "${GREEN}[SUCCESS]${NC} $message" ;; 
        DEBUG) [[ "$VERBOSE" == true ]] && echo -e "${CYAN}[DEBUG]${NC} $message" ;; 
    esac
}

error_exit() {
    log "ERROR" "$1"
    echo -e "${RED}Uninstallation failed. See log for details: $LOG_FILE${NC}"
    exit 1
}

cleanup() {
    # This function is called on script exit
    if [[ "$SKIP_BACKUP" == false && -d "$BACKUP_DIR" && "$(ls -A "$BACKUP_DIR")" ]]; then
        log "INFO" "Backup retained at: $BACKUP_DIR"
        echo -e "${CYAN}Backup available at: $BACKUP_DIR${NC}"
    elif [[ -d "$BACKUP_DIR" ]]; then
        # Cleanup empty backup dir if backup was skipped or failed
        rmdir "$BACKUP_DIR" 2>/dev/null || true
    fi
}

trap cleanup EXIT
trap 'error_exit "Uninstallation interrupted by user."' INT TERM

# --- Core Functions ---
show_help() {
    cat <<EOF
${BOLD}XorLang Enhanced Uninstaller v$VERSION${NC}

Uninstalls the XorLang IDE and command-line tools from the system.

${BOLD}USAGE:${NC}
    sudo $0 [OPTIONS]

${BOLD}OPTIONS:${NC}
    -f, --force         Force removal without confirmation.
    -s, --skip-backup   Do not create a backup of the installation directory.
    -d, --dry-run       Simulate removal without making any changes.
    -v, --verbose       Enable detailed logging output.
    -h, --help          Display this help message and exit.

${BOLD}DESCRIPTION:${NC}
    This script safely removes all components of the XorLang installation,
    including executables, symlinks, desktop entries, and MIME types.
    It requires root privileges to run.
EOF
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -f | --force) FORCE=true; shift ;; 
            -s | --skip-backup) SKIP_BACKUP=true; shift ;; 
            -d | --dry-run) DRY_RUN=true; shift ;; 
            -v | --verbose) VERBOSE=true; shift ;; 
            -h | --help) show_help; exit 0 ;; 
            *) error_exit "Unknown option: '$1'. Use --help for guidance." ;; 
        esac
    done
}

check_requirements() {
    log "INFO" "Checking system requirements..."
    if [[ "$EUID" -ne 0 ]]; then
        error_exit "This script requires root privileges. Please run with sudo."
    fi
    log "SUCCESS" "System requirements met."
}

check_existing_installation() {
    log "INFO" "Checking for existing XorLang installation..."
    for file in "${SYSTEM_FILES[@]}"; do
        if [[ -e "$file" ]]; then
            log "SUCCESS" "XorLang installation detected."
            return 0
        fi
    done
    log "INFO" "No XorLang components found."
    echo -e "${YELLOW}XorLang does not appear to be installed.${NC}"
    exit 0
}

show_removal_preview() {
    echo -e "\n${BOLD}${YELLOW}The following XorLang components will be removed:${NC}"
    for file in "${SYSTEM_FILES[@]}"; do
        if [[ -e "$file" ]]; then
            if [[ -d "$file" ]]; then
                echo -e "  ${RED}📁 Directory: $file/${NC}"
            elif [[ -L "$file" ]]; then
                echo -e "  ${CYAN}🔗 Symlink:   $file${NC}"
            else
                echo -e "  ${BLUE}📄 File:      $file${NC}"
            fi
        fi
    done
    echo
}

get_confirmation() {
    if [[ "$FORCE" == true || "$DRY_RUN" == true ]]; then
        return
    fi
    read -p "Are you sure you want to proceed with uninstallation? (yes/no): " -r REPLY
    echo
    if [[ ! "$REPLY" =~ ^[Yy][Ee][Ss]$ ]]; then
        log "INFO" "Uninstallation cancelled by user."
        echo -e "${YELLOW}Uninstallation cancelled.${NC}"
        exit 0
    fi
}

create_backup() {
    if [[ "$SKIP_BACKUP" == true || ! -d "$INSTALL_DIR" ]]; then
        log "INFO" "Backup skipped."
        return
    fi
    log "INFO" "Creating backup of ${INSTALL_DIR}..."
    mkdir -p "$BACKUP_DIR"
    if cp -a "$INSTALL_DIR" "$BACKUP_DIR/"; then
        log "SUCCESS" "Backup created successfully at $BACKUP_DIR"
    else
        log "WARN" "Failed to create backup. Continuing without one."
        # Clean up partial backup
        rm -rf "$BACKUP_DIR"
    fi
}

remove_xorlang_components() {
    log "INFO" "Starting removal of XorLang components..."
    local failed=false
    for file in "${SYSTEM_FILES[@]}"; do
        if [[ -e "$file" ]]; then
            log "DEBUG" "Removing '$file'..."
            if rm -rf "$file"; then
                log "SUCCESS" "Removed '$file'."
            else
                log "ERROR" "Failed to remove '$file'."
                failed=true
            fi
        fi
    done
    [[ "$failed" == true ]] && error_exit "One or more components could not be removed."
    log "SUCCESS" "All XorLang components removed."
}

update_system_databases() {
    log "INFO" "Updating system databases..."
    if command -v update-mime-database &>/dev/null; then
        update-mime-database /usr/share/mime && log "SUCCESS" "MIME database updated." || log "WARN" "Failed to update MIME database."
    fi
    if command -v update-desktop-database &>/dev/null; then
        update-desktop-database -q /usr/share/applications && log "SUCCESS" "Desktop database updated." || log "WARN" "Failed to update desktop database."
    fi
}

verify_removal() {
    log "INFO" "Verifying removal..."
    local remaining_files=()
    for file in "${SYSTEM_FILES[@]}"; do
        [[ -e "$file" ]] && remaining_files+=("$file")
    done

    if [[ ${#remaining_files[@]} -eq 0 ]]; then
        log "SUCCESS" "Verification complete. No XorLang files found."
        return 0
    else
        log "ERROR" "Verification failed. The following files remain:"
        for file in "${remaining_files[@]}"; do
            log "ERROR" "  - $file"
        done
        return 1
    fi
}

# --- Main Execution ---
main() {
    # Setup and Checks
    echo "XorLang Uninstaller v$VERSION - Log: $LOG_FILE" >"$LOG_FILE"
    parse_args "$@"
    
    echo -e "${BLUE}${BOLD}--- XorLang Uninstaller v$VERSION ---${NC}"
    [[ "$DRY_RUN" == true ]] && echo -e "${YELLOW}${BOLD}*** DRY RUN MODE ***${NC}"

    check_requirements
    check_existing_installation

    # Preview and Confirm
    show_removal_preview
    get_confirmation

    if [[ "$DRY_RUN" == true ]]; then
        log "INFO" "Dry run complete. No changes were made."
        echo -e "${CYAN}Dry run finished. No files were removed.${NC}"
        exit 0
    fi

    # Execution
    create_backup
    remove_xorlang_components
    update_system_databases

    # Final Verification and Summary
    if verify_removal; then
        echo -e "\n${GREEN}${BOLD}✓ XorLang has been successfully uninstalled.${NC}"
    else
        error_exit "Uninstallation finished, but some files could not be removed."
    fi
}

main "$@"
