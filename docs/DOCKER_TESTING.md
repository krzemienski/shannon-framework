# Shannon V3 Docker Testing Guide

Complete guide for building and testing Shannon Framework V3 in Docker containers.

## Overview

Shannon V3 provides a production-ready Docker environment for:
- Clean installation testing
- Behavioral pattern verification
- Continuous integration workflows
- Isolated development environments

## Quick Start

```bash
# Build and run tests
docker-compose up --build

# Interactive shell
docker-compose run --rm shannon /bin/bash

# Verify installation
docker-compose run --rm shannon python3 setup/install.py verify
```

## Architecture

### Multi-Stage Build
The Dockerfile uses a 5-stage build process:

1. **Base** (ubuntu:22.04) - System dependencies
2. **Claude Install** - Claude Code CLI installation
3. **Shannon Setup** - Framework files and Python deps
4. **Shannon Install** - Run installer to ~/.claude/
5. **Testing** - Final test-ready environment

### Directory Structure
```
/app/shannon/
├── Shannon/          # Framework source files
├── setup/            # Installation scripts
├── tests/            # Test suite
├── docs/             # Documentation
└── test-results/     # Test output (mounted)
```

## Building the Image

### Standard Build
```bash
# Using Docker Compose (recommended)
docker-compose build

# Using Docker directly
docker build -t shannon:v3-testing .
```

### Target-Specific Builds
```bash
# Build up to specific stage
docker build --target base -t shannon:base .
docker build --target claude-install -t shannon:claude .
docker build --target shannon-setup -t shannon:setup .
```

### Build Arguments
```bash
# Specify Python version
docker build --build-arg PYTHON_VERSION=3.10 .

# Specify Shannon version
docker build --build-arg SHANNON_VERSION=3.0.0 .
```

## Running Tests

### Basic Test Execution
```bash
# Run all tests
docker-compose run --rm shannon python3 -m pytest tests/ -v

# Run specific test file
docker-compose run --rm shannon python3 -m pytest tests/test_shannon.py -v

# Run specific test function
docker-compose run --rm shannon python3 -m pytest tests/test_shannon.py::test_installation -v
```

### Advanced Testing
```bash
# Tests with coverage
docker-compose run --rm shannon python3 -m pytest tests/ --cov=Shannon --cov-report=html

# Tests with detailed output
docker-compose run --rm shannon python3 -m pytest tests/ -vv --tb=long

# Tests in parallel (if pytest-xdist installed)
docker-compose run --rm shannon python3 -m pytest tests/ -n auto

# Stop on first failure
docker-compose run --rm shannon python3 -m pytest tests/ -x
```

### Test Filtering
```bash
# Run tests by marker
docker-compose run --rm shannon python3 -m pytest tests/ -m "not slow"

# Run tests by keyword
docker-compose run --rm shannon python3 -m pytest tests/ -k "installation"

# Skip specific tests
docker-compose run --rm shannon python3 -m pytest tests/ --ignore=tests/integration/
```

## Installation Verification

### Shannon Status Checks
```bash
# Full verification
docker-compose run --rm shannon python3 setup/install.py verify

# Status report
docker-compose run --rm shannon python3 setup/install.py status

# Check specific components
docker-compose run --rm shannon /bin/bash -c "
  ls -la ~/.claude/core/ && \
  ls -la ~/.claude/agents/ && \
  ls -la ~/.claude/commands/
"
```

### Health Checks
```bash
# Container health status
docker ps --filter name=shannon-test

# Manual health check
docker-compose run --rm shannon python3 setup/install.py verify
```

## Interactive Development

### Shell Access
```bash
# Interactive bash shell
docker-compose run --rm shannon /bin/bash

# Python REPL with Shannon loaded
docker-compose run --rm shannon python3

# IPython (if installed)
docker-compose run --rm shannon ipython
```

### File Inspection
```bash
# View Shannon installation
docker-compose run --rm shannon ls -la ~/.claude/

# Check markdown files
docker-compose run --rm shannon cat ~/.claude/core/TESTING_PHILOSOPHY.md

# Verify hooks
docker-compose run --rm shannon cat ~/.claude/hooks/precompact.py
```

## Test Results

### Accessing Results
```bash
# Test results are mounted to ./test-results/
ls -la test-results/

# View coverage report (after running coverage tests)
open test-results/htmlcov/index.html
```

### Collecting Artifacts
```bash
# Copy results from container
docker cp shannon-test:/app/shannon/test-results ./local-results/

# Export logs
docker-compose logs shannon > shannon-test.log
```

## Troubleshooting

### Build Failures

**Issue**: Package installation fails
```bash
# Clear Docker cache and rebuild
docker-compose build --no-cache

# Check specific stage
docker build --target base -t shannon:debug .
docker run -it shannon:debug /bin/bash
```

**Issue**: Shannon source files not found
```bash
# Verify .dockerignore isn't excluding needed files
cat .dockerignore

# Check build context
docker-compose build --progress=plain
```

### Runtime Failures

**Issue**: Tests fail with import errors
```bash
# Verify Python path
docker-compose run --rm shannon python3 -c "import sys; print(sys.path)"

# Check Shannon module
docker-compose run --rm shannon python3 -c "import Shannon; print(Shannon.__file__)"
```

**Issue**: Claude CLI not working
```bash
# Check Claude installation
docker-compose run --rm shannon which claude
docker-compose run --rm shannon claude --version

# Verify npm global packages
docker-compose run --rm shannon npm list -g --depth=0
```

**Issue**: Installation verification fails
```bash
# Check Claude directory structure
docker-compose run --rm shannon ls -laR ~/.claude/

# Verify settings.json
docker-compose run --rm shannon cat ~/.claude/settings.json

# Re-run installer
docker-compose run --rm shannon python3 setup/install.py install
```

### Permission Issues

**Issue**: Cannot write test results
```bash
# Check volume permissions
docker-compose run --rm shannon ls -la /app/shannon/test-results

# Create directory with proper permissions
mkdir -p test-results
chmod 777 test-results
```

## CI/CD Integration

### GitHub Actions
```yaml
name: Shannon Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build Docker image
        run: docker-compose build

      - name: Run tests
        run: docker-compose run --rm shannon python3 -m pytest tests/ -v

      - name: Verify installation
        run: docker-compose run --rm shannon python3 setup/install.py verify
```

### GitLab CI
```yaml
test:
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker-compose build
    - docker-compose run --rm shannon python3 -m pytest tests/ -v
    - docker-compose run --rm shannon python3 setup/install.py verify
  artifacts:
    paths:
      - test-results/
    expire_in: 1 week
```

## Performance Optimization

### Build Cache
```bash
# Use BuildKit for better caching
DOCKER_BUILDKIT=1 docker build -t shannon:v3-testing .

# Layer caching with Docker Compose
docker-compose build --parallel
```

### Image Size
```bash
# Check image size
docker images shannon:v3-testing

# Analyze layers
docker history shannon:v3-testing

# Optimize by cleaning apt cache (already done in Dockerfile)
```

### Test Execution Speed
```bash
# Run tests in parallel
docker-compose run --rm shannon python3 -m pytest tests/ -n auto

# Skip slow tests during development
docker-compose run --rm shannon python3 -m pytest tests/ -m "not slow"
```

## Cleanup

### Remove Containers
```bash
# Stop and remove containers
docker-compose down

# Remove with volumes
docker-compose down -v
```

### Remove Images
```bash
# Remove Shannon image
docker rmi shannon:v3-testing

# Remove all dangling images
docker image prune -f

# Remove all unused images
docker image prune -a
```

### Clean Build Cache
```bash
# Remove build cache
docker builder prune

# Remove all cache
docker system prune -a --volumes
```

## Advanced Usage

### Custom Test Configuration
```bash
# Override pytest configuration
docker-compose run --rm shannon python3 -m pytest tests/ \
  --cov=Shannon \
  --cov-report=term-missing \
  --cov-report=html \
  --junit-xml=test-results/junit.xml
```

### Environment Variables
```bash
# Pass environment variables
docker-compose run --rm \
  -e TEST_DEBUG=1 \
  -e SHANNON_LOG_LEVEL=DEBUG \
  shannon python3 -m pytest tests/ -v
```

### Volume Mounting for Development
```bash
# Mount local Shannon directory for live testing
docker run -it --rm \
  -v $(pwd)/Shannon:/app/shannon/Shannon \
  -v $(pwd)/tests:/app/shannon/tests \
  shannon:v3-testing /bin/bash
```

## Best Practices

1. **Always use docker-compose** for consistent environments
2. **Run verify after builds** to ensure correct installation
3. **Use --rm flag** to automatically clean up containers
4. **Mount test-results** to preserve test output
5. **Tag images with versions** for reproducibility
6. **Clean up regularly** to free disk space
7. **Use multi-stage builds** to optimize image size
8. **Document custom configurations** in docker-compose.yml

## Additional Resources

- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Shannon V3 Specification](../SHANNON_V3_SPECIFICATION.md)
- [Testing Philosophy](../Shannon/Core/TESTING_PHILOSOPHY.md)