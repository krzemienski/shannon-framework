#!/bin/bash
# ============================================================================
# Shannon V3 Docker Testing Helper Script
# ============================================================================
# Convenience wrapper for common Docker testing operations
# ============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo -e "\n${BLUE}===${NC} $1 ${BLUE}===${NC}"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Show usage
usage() {
    cat << EOF
Shannon V3 Docker Testing Helper

Usage: ./docker-test.sh <command> [options]

Commands:
    build               Build the Docker image
    test                Run all tests
    test-specific       Run specific test (provide test name)
    verify              Verify Shannon installation
    status              Show Shannon status
    shell               Open interactive shell
    coverage            Run tests with coverage report
    clean               Clean up containers and images
    rebuild             Clean build from scratch
    help                Show this help message

Examples:
    ./docker-test.sh build
    ./docker-test.sh test
    ./docker-test.sh test-specific test_installation
    ./docker-test.sh verify
    ./docker-test.sh shell
    ./docker-test.sh coverage
    ./docker-test.sh clean
    ./docker-test.sh rebuild

EOF
}

# Build image
cmd_build() {
    print_header "Building Shannon Docker Image"
    docker-compose build
    print_success "Build complete"
}

# Run all tests
cmd_test() {
    print_header "Running Shannon Tests"
    docker-compose run --rm shannon python3 -m pytest tests/ -v --tb=short
}

# Run specific test
cmd_test_specific() {
    if [ -z "$1" ]; then
        print_error "Please provide test name"
        echo "Usage: ./docker-test.sh test-specific <test_name>"
        exit 1
    fi
    print_header "Running Test: $1"
    docker-compose run --rm shannon python3 -m pytest tests/ -k "$1" -v
}

# Verify installation
cmd_verify() {
    print_header "Verifying Shannon Installation"
    docker-compose run --rm shannon python3 setup/install.py verify
}

# Show status
cmd_status() {
    print_header "Shannon Installation Status"
    docker-compose run --rm shannon python3 setup/install.py status
}

# Interactive shell
cmd_shell() {
    print_header "Opening Interactive Shell"
    print_warning "Type 'exit' to close shell"
    docker-compose run --rm shannon /bin/bash
}

# Coverage report
cmd_coverage() {
    print_header "Running Tests with Coverage"
    docker-compose run --rm shannon python3 -m pytest tests/ \
        --cov=Shannon \
        --cov-report=term-missing \
        --cov-report=html \
        --cov-report=xml

    print_success "Coverage report generated in test-results/htmlcov/"

    # Try to open coverage report
    if [ -f "test-results/htmlcov/index.html" ]; then
        if command -v open &> /dev/null; then
            print_success "Opening coverage report in browser..."
            open test-results/htmlcov/index.html
        else
            print_warning "Coverage report: test-results/htmlcov/index.html"
        fi
    fi
}

# Clean up
cmd_clean() {
    print_header "Cleaning Up Docker Resources"

    print_warning "Stopping containers..."
    docker-compose down

    print_warning "Removing Shannon image..."
    docker rmi shannon:v3-testing 2>/dev/null || true

    print_warning "Removing dangling images..."
    docker image prune -f

    print_success "Cleanup complete"
}

# Rebuild from scratch
cmd_rebuild() {
    print_header "Rebuilding Shannon from Scratch"

    cmd_clean

    print_warning "Building with no cache..."
    docker-compose build --no-cache

    print_success "Rebuild complete"
}

# Main command dispatcher
case "${1:-help}" in
    build)
        cmd_build
        ;;
    test)
        cmd_test
        ;;
    test-specific)
        cmd_test_specific "$2"
        ;;
    verify)
        cmd_verify
        ;;
    status)
        cmd_status
        ;;
    shell)
        cmd_shell
        ;;
    coverage)
        cmd_coverage
        ;;
    clean)
        cmd_clean
        ;;
    rebuild)
        cmd_rebuild
        ;;
    help|--help|-h)
        usage
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        usage
        exit 1
        ;;
esac

exit 0