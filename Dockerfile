# ============================================================================
# Shannon V3 Testing Environment Dockerfile
# ============================================================================
# Multi-stage build for testing Shannon Framework V3 installation and behavior
#
# Purpose: Clean environment to verify Shannon installation and patterns
# Architecture: Ubuntu 22.04 base → System deps → Claude Code → Shannon
# ============================================================================

# ----------------------------------------------------------------------------
# Stage 1: Base Image with System Dependencies
# ----------------------------------------------------------------------------
FROM ubuntu:22.04 AS base

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Set timezone to avoid tzdata prompts
ENV TZ=America/New_York

# Install system dependencies
# - python3: Shannon installer and test runner
# - python3-pip: Python package manager
# - git: Version control (required by many tools)
# - curl: HTTP client for downloads
# - nodejs/npm: Required for Claude Code CLI
RUN apt-get update && apt-get install -y \
    python3=3.10.* \
    python3-pip=22.0.* \
    git=1:2.34.* \
    curl=7.81.* \
    nodejs=12.22.* \
    npm=8.5.* \
    && rm -rf /var/lib/apt/lists/*

# Verify installations
RUN python3 --version && \
    pip3 --version && \
    git --version && \
    node --version && \
    npm --version

# ----------------------------------------------------------------------------
# Stage 2: Claude Code CLI Installation
# ----------------------------------------------------------------------------
FROM base AS claude-install

# Install Claude Code CLI globally
# Using official Anthropic package from npm registry
RUN npm install -g @anthropic/claude-code@latest

# Verify Claude Code installation
RUN claude --version || echo "Claude CLI installed (version check may require auth)"

# Create Claude configuration directory
RUN mkdir -p /root/.claude

# ----------------------------------------------------------------------------
# Stage 3: Shannon Framework Setup
# ----------------------------------------------------------------------------
FROM claude-install AS shannon-setup

# Set working directory for Shannon project
WORKDIR /app/shannon

# Copy Shannon framework structure
# Core system files
COPY Shannon/ ./Shannon/
COPY setup/ ./setup/
COPY tests/ ./tests/
COPY docs/ ./docs/

# Copy project metadata
COPY README.md ./README.md

# Note: No CLAUDE.md in repository root - Shannon uses ~/.claude/ structure
# Shannon is installed via setup/install.py which copies files to ~/.claude/

# Install Python test dependencies
# pytest: Test runner
# pytest-cov: Coverage reporting
# pyyaml: YAML parsing (if needed by tests)
RUN pip3 install --no-cache-dir \
    pytest==7.4.* \
    pytest-cov==4.1.* \
    pyyaml==6.0.*

# Verify test dependencies
RUN pytest --version

# ----------------------------------------------------------------------------
# Stage 4: Shannon Installation
# ----------------------------------------------------------------------------
FROM shannon-setup AS shannon-install

# Run Shannon installer
# This copies markdown files to ~/.claude/ and registers PreCompact hook
RUN python3 setup/install.py install

# Verify Shannon installation
RUN python3 setup/install.py verify

# Display Shannon status for build-time verification
RUN python3 setup/install.py status

# ----------------------------------------------------------------------------
# Stage 5: Testing Environment (Final)
# ----------------------------------------------------------------------------
FROM shannon-install AS testing

# Set environment variables for testing
ENV PYTHONUNBUFFERED=1
ENV SHANNON_VERSION=3.0.0
ENV TEST_MODE=docker

# Create test output directory
RUN mkdir -p /app/shannon/test-results

# Health check: Verify Shannon installation
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 setup/install.py verify || exit 1

# Default command: Run Shannon tests with verbose output
CMD ["python3", "-m", "pytest", "tests/", "-v", "--tb=short"]

# ----------------------------------------------------------------------------
# Alternative Entrypoints (documented for users)
# ----------------------------------------------------------------------------
# Interactive shell: docker run -it shannon:latest /bin/bash
# Specific test: docker run shannon:latest python3 -m pytest tests/test_shannon.py::test_name -v
# Coverage report: docker run shannon:latest python3 -m pytest tests/ --cov=Shannon --cov-report=html
# Shannon status: docker run shannon:latest python3 setup/install.py status
# Shannon verify: docker run shannon:latest python3 setup/install.py verify
# ----------------------------------------------------------------------------

# Build metadata (labels)
LABEL org.opencontainers.image.title="Shannon V3 Testing Environment"
LABEL org.opencontainers.image.description="Clean Docker environment for Shannon Framework testing"
LABEL org.opencontainers.image.version="3.0.0"
LABEL org.opencontainers.image.authors="Shannon Framework Contributors"
LABEL org.opencontainers.image.documentation="https://github.com/your-repo/shannon"

# Expose no ports (testing environment, not a service)

# Set final working directory
WORKDIR /app/shannon