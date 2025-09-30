# Shannon V3 Docker Quick Start

Get Shannon V3 running in Docker in under 5 minutes.

## Prerequisites

- Docker 20.10+
- Docker Compose 1.29+
- 2GB free disk space

## Installation

```bash
# Clone repository
git clone <shannon-repo-url>
cd shannon

# Build and test
./docker-test.sh build
./docker-test.sh test
```

That's it! Shannon is now running in Docker.

## Quick Commands

### Testing
```bash
# Run all tests
./docker-test.sh test

# Run specific test
./docker-test.sh test-specific test_installation

# Test with coverage
./docker-test.sh coverage
```

### Verification
```bash
# Verify installation
./docker-test.sh verify

# Check status
./docker-test.sh status
```

### Development
```bash
# Interactive shell
./docker-test.sh shell

# Inside shell:
python3 setup/install.py verify
ls -la ~/.claude/
pytest tests/ -v
```

### Cleanup
```bash
# Remove containers and images
./docker-test.sh clean

# Rebuild from scratch
./docker-test.sh rebuild
```

## Common Operations

### Run Specific Test File
```bash
docker-compose run --rm shannon python3 -m pytest tests/test_shannon.py -v
```

### Run Tests with Output
```bash
docker-compose run --rm shannon python3 -m pytest tests/ -vv --tb=long
```

### Check Shannon Files
```bash
docker-compose run --rm shannon ls -la ~/.claude/core/
docker-compose run --rm shannon ls -la ~/.claude/agents/
docker-compose run --rm shannon ls -la ~/.claude/commands/
```

### View Installed Hook
```bash
docker-compose run --rm shannon cat ~/.claude/hooks/precompact.py
```

## Troubleshooting

### Build fails
```bash
# Clear cache and rebuild
./docker-test.sh rebuild
```

### Tests fail
```bash
# Verify installation first
./docker-test.sh verify

# Run tests with more detail
docker-compose run --rm shannon python3 -m pytest tests/ -vv --tb=long
```

### Can't access results
```bash
# Create test-results directory
mkdir -p test-results
chmod 777 test-results

# Run tests again
./docker-test.sh test
```

## Next Steps

- Read full guide: [DOCKER_TESTING.md](DOCKER_TESTING.md)
- Explore Shannon: [README.md](../README.md)
- View specification: [SHANNON_V3_SPECIFICATION.md](../SHANNON_V3_SPECIFICATION.md)

## Support

For issues:
1. Check [DOCKER_TESTING.md](DOCKER_TESTING.md) troubleshooting section
2. Run `./docker-test.sh verify` to check installation
3. Open issue with logs and error messages