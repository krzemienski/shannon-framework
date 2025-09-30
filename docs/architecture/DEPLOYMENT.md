# Shannon Framework v2.1 - Deployment Guide

## System Requirements

### Minimum Requirements
- **Python**: 3.9+
- **CPU**: 2 cores
- **RAM**: 4GB
- **Storage**: 500MB for framework + 1GB for operation
- **OS**: Linux, macOS, Windows (WSL recommended)

### Recommended Requirements
- **Python**: 3.11+
- **CPU**: 4+ cores (for parallel execution)
- **RAM**: 8GB+
- **Storage**: 2GB+ for framework + 10GB for operation
- **OS**: Linux (Ubuntu 22.04+, Debian 11+) or macOS 12+

### Production Requirements
- **Python**: 3.11+
- **CPU**: 8+ cores
- **RAM**: 16GB+
- **Storage**: 10GB+ SSD
- **OS**: Linux (Ubuntu 22.04 LTS recommended)
- **Network**: Stable connection for MCP servers

## Dependencies

### Core Dependencies
```
numpy>=1.24.0           # Core numerical operations, FFT, complex numbers
```

### Testing Dependencies
```
pytest>=7.4.0           # Test framework
pytest-asyncio>=0.21.0  # Async test support
```

### Optional Dependencies
```
psutil>=5.9.0           # System resource monitoring
```

### MCP Server Requirements

Shannon v2.1 integrates with multiple MCP servers:

**Serena MCP** (Required for reflection and memory):
- **Purpose**: 5-stage reflection, memory persistence, pattern learning
- **Installation**: Follow Serena MCP setup guide
- **Configuration**: Set SERENA_API_KEY environment variable

**Tavily MCP** (Optional for research):
- **Purpose**: Web search and real-time information
- **Installation**: `pip install tavily-python`
- **Configuration**: Set TAVILY_API_KEY environment variable

**Context7 MCP** (Optional for documentation):
- **Purpose**: Official library documentation lookup
- **Installation**: Follow Context7 MCP setup guide
- **Configuration**: No API key required

**Sequential MCP** (Optional for complex analysis):
- **Purpose**: Multi-step reasoning and systematic analysis
- **Installation**: Follow Sequential MCP setup guide
- **Configuration**: No API key required

**Magic MCP** (Optional for UI components):
- **Purpose**: Modern UI component generation
- **Installation**: Follow Magic MCP setup guide
- **Configuration**: No API key required

**Playwright MCP** (Optional for browser automation):
- **Purpose**: E2E testing and browser interaction
- **Installation**: Follow Playwright MCP setup guide
- **Configuration**: Playwright browser installation required

## Installation

### Quick Install (Development)

```bash
# Clone repository
git clone https://github.com/your-org/shannon.git
cd shannon

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Verify installation
python -c "import shannon; print(shannon.__version__)"  # Should print: 2.1.0
```

### Standard Install (Production)

```bash
# Install from PyPI (when published)
pip install shannon-framework

# Or install from source
git clone https://github.com/your-org/shannon.git
cd shannon
pip install .

# Verify installation
python -c "import shannon; print(shannon.__version__)"
```

### Docker Install (Containerized)

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy Shannon framework
COPY . .

# Install Shannon
RUN pip install --no-cache-dir -e .

# Run tests (optional)
RUN pytest tests/

# Set entrypoint
ENTRYPOINT ["python"]
CMD ["-m", "shannon"]
```

**Build and run**:
```bash
docker build -t shannon:2.1.0 .
docker run -it --rm shannon:2.1.0
```

## Configuration

### Basic Configuration

Create `shannon_config.yaml` in your project root:

```yaml
# Shannon Framework Configuration v2.1

# Orchestration Settings
orchestration:
  complexity_threshold: 0.7        # Trigger wave when complexity ≥ 0.7
  max_agents: 10                   # Maximum concurrent agents
  timeout: 300.0                   # Wave timeout (seconds)
  default_strategy: "adaptive"     # Wave strategy
  validation_level: "standard"     # Validation level

# Memory Settings
memory:
  hot_tier_ttl: 300                # Hot tier retention (seconds)
  warm_tier_ttl: 900               # Warm tier retention (seconds)
  cool_tier_ttl: 3600              # Cool tier retention (seconds)
  cold_tier_ttl: 21600             # Cold tier retention (seconds)
  max_hot_size: 104857600          # 100MB
  max_warm_size: 52428800          # 50MB
  compression_enabled: true

# Context Management
context:
  green_threshold: 0.60            # Normal operation
  yellow_threshold: 0.75           # Warning
  orange_threshold: 0.85           # Alert
  red_threshold: 0.95              # Critical
  checkpoint_frequency: 5          # Checkpoints per wave

# Reflection Settings
reflection:
  enabled: true
  pre_wave: true                   # Stage 1
  mid_wave: true                   # Stage 2
  post_wave: true                  # Stage 3
  pattern_learning: true           # Stage 4
  memory_persistence: true         # Stage 5

# Evolution Settings
evolution:
  enabled: true
  population_size: 100
  mutation_rate: 0.10
  crossover_rate: 0.70
  tournament_k: 3
  elitism_rate: 0.10

# Performance Settings
performance:
  max_parallel: 5                  # Concurrent task limit
  enable_monitoring: true
  anomaly_detection: true
  auto_recommendations: true

# Error Recovery Settings
error_recovery:
  max_retries: 3
  retry_backoff: 2.0               # Exponential backoff multiplier
  circuit_breaker_threshold: 5     # Failures before opening circuit
  circuit_breaker_timeout: 60.0    # Seconds before retry attempt

# MCP Server Settings
mcp:
  serena:
    enabled: true
    timeout: 30.0
  tavily:
    enabled: false                 # Optional
    timeout: 15.0
  context7:
    enabled: false                 # Optional
    timeout: 20.0
  sequential:
    enabled: false                 # Optional
    timeout: 60.0

# Logging Settings
logging:
  level: "INFO"                    # DEBUG, INFO, WARNING, ERROR, CRITICAL
  format: "json"                   # json or text
  file: "shannon.log"
  max_size: 10485760               # 10MB
  backup_count: 5
```

### Environment Variables

Create `.env` file:

```bash
# Shannon Framework Environment Variables

# Required
SERENA_API_KEY=your_serena_api_key_here

# Optional MCP Servers
TAVILY_API_KEY=your_tavily_api_key_here
CONTEXT7_API_KEY=your_context7_api_key_here

# Configuration
SHANNON_CONFIG_PATH=/path/to/shannon_config.yaml
SHANNON_LOG_LEVEL=INFO
SHANNON_ENV=production              # development, staging, production

# Performance
SHANNON_MAX_WORKERS=8
SHANNON_MEMORY_LIMIT=8589934592     # 8GB in bytes

# Feature Flags
SHANNON_ENABLE_EVOLUTION=true
SHANNON_ENABLE_REFLECTION=true
SHANNON_ENABLE_MONITORING=true
```

### Advanced Configuration

#### Custom Orchestration Rules

```python
from shannon.core import AutomaticOrchestrator, WaveConfig

# Create custom orchestrator
orchestrator = AutomaticOrchestrator()

# Override complexity weights
orchestrator.complexity_weights = {
    'file_count': 0.20,              # Increased from 0.15
    'directory_depth': 0.05,         # Decreased from 0.10
    'operation_diversity': 0.15,
    'domain_complexity': 0.15,
    'dependency_depth': 0.15,
    'risk_level': 0.15,              # Increased from 0.10
    'token_estimation': 0.10,
    'parallelization_opportunity': 0.05  # Decreased from 0.10
}

# Override threshold
orchestrator.complexity_threshold = 0.6  # Lower threshold for more orchestration
```

#### Custom Memory Tiers

```python
from shannon.memory import MultiTierMemory, MemoryTier

# Create custom memory configuration
memory = MultiTierMemory()

# Adjust transition times
memory.transition_config = {
    'hot_to_warm': 10 * 60,      # 10 minutes (increased from 5)
    'warm_to_cool': 30 * 60,     # 30 minutes (increased from 15)
    'cool_to_cold': 2 * 60 * 60, # 2 hours (increased from 1)
    'cold_to_archive': 24 * 60 * 60  # 24 hours (increased from 6)
}

# Adjust compression ratios
memory.compression_config = {
    'semantic': 3.0,    # Less aggressive (was 5.0)
    'ast': 7.0,         # Less aggressive (was 10.0)
    'holographic': 30.0, # Less aggressive (was 50.0)
    'archive': 70.0     # Less aggressive (was 100.0)
}
```

#### Custom Reflection Pipeline

```python
from shannon.reflection import SerenaReflectionEngine

# Create custom reflection engine
reflection = SerenaReflectionEngine()

# Selective stage enabling
reflection.stages_enabled = {
    'pre_wave': True,
    'mid_wave': False,        # Disable for faster execution
    'post_wave': True,
    'pattern_learning': True,
    'memory_persistence': True
}

# Custom reflection frequency
reflection.mid_wave_frequency = 10  # Check every 10 operations (was 5)
```

## Production Deployment

### Deployment Architecture

```
┌─────────────────────────────────────────────────┐
│              Load Balancer (Optional)            │
└────────────────────┬────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│             Shannon Application Nodes            │
│  ┌──────────────┬──────────────┬──────────────┐ │
│  │   Node 1     │   Node 2     │   Node 3     │ │
│  │  Shannon     │  Shannon     │  Shannon     │ │
│  │  Framework   │  Framework   │  Framework   │ │
│  └──────────────┴──────────────┴──────────────┘ │
└────────────────────┬────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│              Shared Storage (Optional)           │
│  ┌──────────────────────────────────────────┐  │
│  │  Memory Persistence (Serena MCP)         │  │
│  │  Pattern Library (Serena MCP)            │  │
│  │  Snapshot Storage (S3 / NFS)             │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

### Deployment Steps

#### 1. Prepare Environment

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Python 3.11
sudo apt-get install -y python3.11 python3.11-venv python3.11-dev

# Install system dependencies
sudo apt-get install -y gcc g++ make git
```

#### 2. Create Application User

```bash
# Create dedicated user
sudo useradd -m -s /bin/bash shannon

# Create application directory
sudo mkdir -p /opt/shannon
sudo chown shannon:shannon /opt/shannon
```

#### 3. Install Shannon

```bash
# Switch to shannon user
sudo su - shannon

# Create virtual environment
cd /opt/shannon
python3.11 -m venv venv
source venv/bin/activate

# Install Shannon
pip install shannon-framework

# Or install from source
git clone https://github.com/your-org/shannon.git
cd shannon
pip install .
```

#### 4. Configure Application

```bash
# Create configuration directory
mkdir -p /opt/shannon/config

# Copy configuration files
cp shannon_config.yaml /opt/shannon/config/
cp .env /opt/shannon/config/

# Set permissions
chmod 600 /opt/shannon/config/.env
```

#### 5. Create Systemd Service

Create `/etc/systemd/system/shannon.service`:

```ini
[Unit]
Description=Shannon Framework Agent Orchestration
After=network.target

[Service]
Type=simple
User=shannon
Group=shannon
WorkingDirectory=/opt/shannon
Environment="PATH=/opt/shannon/venv/bin"
EnvironmentFile=/opt/shannon/config/.env
ExecStart=/opt/shannon/venv/bin/python -m shannon.server
Restart=on-failure
RestartSec=10s
StandardOutput=append:/var/log/shannon/shannon.log
StandardError=append:/var/log/shannon/shannon_error.log

# Resource limits
LimitNOFILE=65536
MemoryLimit=8G
CPUQuota=400%

[Install]
WantedBy=multi-user.target
```

**Enable and start service**:

```bash
# Create log directory
sudo mkdir -p /var/log/shannon
sudo chown shannon:shannon /var/log/shannon

# Enable service
sudo systemctl enable shannon

# Start service
sudo systemctl start shannon

# Check status
sudo systemctl status shannon
```

#### 6. Configure Logging

Create `/opt/shannon/config/logging.yaml`:

```yaml
version: 1
disable_existing_loggers: false

formatters:
  json:
    class: pythonjsonlogger.jsonlogger.JsonFormatter
    format: '%(asctime)s %(name)s %(levelname)s %(message)s'

  standard:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

handlers:
  console:
    class: logging.StreamHandler
    formatter: standard
    stream: ext://sys.stdout

  file:
    class: logging.handlers.RotatingFileHandler
    formatter: json
    filename: /var/log/shannon/shannon.log
    maxBytes: 10485760  # 10MB
    backupCount: 5

  error_file:
    class: logging.handlers.RotatingFileHandler
    formatter: json
    filename: /var/log/shannon/shannon_error.log
    maxBytes: 10485760
    backupCount: 5
    level: ERROR

loggers:
  shannon:
    level: INFO
    handlers: [console, file, error_file]
    propagate: false

root:
  level: INFO
  handlers: [console, file]
```

#### 7. Configure Monitoring

**Prometheus metrics endpoint** (optional):

```python
# In shannon/server.py
from prometheus_client import Counter, Histogram, start_http_server

# Metrics
wave_executions = Counter('shannon_wave_executions_total', 'Total wave executions')
wave_duration = Histogram('shannon_wave_duration_seconds', 'Wave execution duration')
agent_count = Counter('shannon_agents_spawned_total', 'Total agents spawned')
memory_usage = Gauge('shannon_memory_bytes', 'Memory usage by tier', ['tier'])

# Start metrics server
start_http_server(9090)
```

**Grafana dashboard** (optional):
- Import Shannon dashboard JSON from `monitoring/grafana_dashboard.json`

### Health Checks

#### Basic Health Check

```python
# shannon/health.py
from shannon.core import AutomaticOrchestrator
from shannon.memory import MultiTierMemory

def health_check():
    """Basic health check"""
    try:
        orchestrator = AutomaticOrchestrator()
        memory = MultiTierMemory()

        # Check orchestrator
        assert orchestrator is not None

        # Check memory system
        stats = memory.get_statistics()
        assert stats is not None

        return {"status": "healthy", "version": "2.1.0"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

#### Readiness Check

```python
def readiness_check():
    """Check if system is ready to accept requests"""
    try:
        # Check MCP servers
        from shannon.integration import MCPCoordinator
        coordinator = MCPCoordinator()

        serena_healthy = coordinator.health_check('serena')

        if not serena_healthy:
            return {"ready": False, "reason": "Serena MCP unavailable"}

        return {"ready": True}
    except Exception as e:
        return {"ready": False, "error": str(e)}
```

#### Liveness Check

```python
def liveness_check():
    """Check if system is alive"""
    try:
        # Simple check: can we import core modules?
        import shannon
        return {"alive": True, "version": shannon.__version__}
    except Exception as e:
        return {"alive": False, "error": str(e)}
```

### Backup and Recovery

#### Backup Strategy

```bash
#!/bin/bash
# backup.sh - Backup Shannon state

BACKUP_DIR="/backup/shannon"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p "$BACKUP_DIR/$DATE"

# Backup configuration
cp -r /opt/shannon/config "$BACKUP_DIR/$DATE/"

# Backup logs
cp -r /var/log/shannon "$BACKUP_DIR/$DATE/"

# Backup memory state (if using local storage)
cp -r /opt/shannon/data "$BACKUP_DIR/$DATE/"

# Create tarball
tar -czf "$BACKUP_DIR/shannon_backup_$DATE.tar.gz" -C "$BACKUP_DIR" "$DATE"

# Remove temporary directory
rm -rf "$BACKUP_DIR/$DATE"

# Retention: keep last 7 days
find "$BACKUP_DIR" -name "shannon_backup_*.tar.gz" -mtime +7 -delete

echo "Backup completed: shannon_backup_$DATE.tar.gz"
```

**Schedule with cron**:

```bash
# Add to crontab
0 2 * * * /opt/shannon/scripts/backup.sh
```

#### Recovery Procedure

```bash
#!/bin/bash
# restore.sh - Restore Shannon state

BACKUP_FILE=$1

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file.tar.gz>"
    exit 1
fi

# Stop Shannon service
sudo systemctl stop shannon

# Extract backup
TEMP_DIR="/tmp/shannon_restore_$$"
mkdir -p "$TEMP_DIR"
tar -xzf "$BACKUP_FILE" -C "$TEMP_DIR"

# Restore configuration
cp -r "$TEMP_DIR"/*/config/* /opt/shannon/config/

# Restore data
cp -r "$TEMP_DIR"/*/data/* /opt/shannon/data/

# Cleanup
rm -rf "$TEMP_DIR"

# Start Shannon service
sudo systemctl start shannon

echo "Restoration complete from $BACKUP_FILE"
```

## Security Considerations

### API Key Management

```bash
# Use environment variables
export SERENA_API_KEY=$(cat /secure/path/serena_api_key)

# Or use secrets manager (e.g., AWS Secrets Manager)
aws secretsmanager get-secret-value --secret-id shannon/serena_api_key
```

### Network Security

```bash
# Firewall rules (UFW example)
sudo ufw allow from 10.0.0.0/8 to any port 8000  # Internal network only
sudo ufw enable
```

### File Permissions

```bash
# Restrict config file access
chmod 600 /opt/shannon/config/.env
chmod 600 /opt/shannon/config/shannon_config.yaml

# Restrict log directory
chmod 700 /var/log/shannon
```

### Resource Limits

```ini
# In systemd service file
MemoryLimit=8G
CPUQuota=400%  # 4 cores
LimitNOFILE=65536
```

## Performance Tuning

### CPU Optimization

```yaml
# In shannon_config.yaml
performance:
  max_parallel: 8              # Match CPU core count
  enable_cpu_affinity: true    # Pin agents to cores
```

### Memory Optimization

```yaml
memory:
  max_hot_size: 524288000      # 500MB (increased from 100MB)
  aggressive_compression: true  # Enable aggressive tier transitions
```

### Network Optimization

```yaml
mcp:
  connection_pooling: true
  max_connections: 50
  timeout: 10.0
```

## Troubleshooting

### Common Issues

#### Issue: High Memory Usage

**Symptoms**: Memory usage grows over time

**Diagnosis**:
```python
from shannon.memory import MultiTierMemory
memory = MultiTierMemory()
stats = memory.get_statistics()
print(stats)
```

**Solution**: Adjust tier transition times or enable aggressive compression

#### Issue: Slow Wave Execution

**Symptoms**: Waves take longer than expected

**Diagnosis**:
```python
from shannon.metrics import PerformanceTracker
tracker = PerformanceTracker()
bottlenecks = tracker.identify_bottlenecks()
print(bottlenecks)
```

**Solution**: Increase parallelism, optimize MCP calls, or adjust complexity threshold

#### Issue: Context Overflow

**Symptoms**: Red alert (>85% context usage)

**Diagnosis**: Check context monitor alerts

**Solution**: Create manual checkpoint, aggressive memory compression, or reduce scope

#### Issue: MCP Server Timeout

**Symptoms**: Serena MCP calls timing out

**Diagnosis**: Check MCP server health

**Solution**: Increase timeout, implement retry logic, or use fallback strategies

### Diagnostic Commands

```bash
# Check Shannon service status
sudo systemctl status shannon

# View logs
sudo journalctl -u shannon -f

# Check resource usage
htop -p $(pgrep -f shannon)

# Check memory tiers
python -c "from shannon.memory import MultiTierMemory; print(MultiTierMemory().get_statistics())"

# Check agent count
python -c "from shannon.core import AutomaticOrchestrator; print(len(AutomaticOrchestrator().active_agents))"
```

## Scaling Strategies

### Horizontal Scaling

**Load balancer configuration** (nginx example):

```nginx
upstream shannon_backends {
    least_conn;
    server shannon1.example.com:8000 max_fails=3 fail_timeout=30s;
    server shannon2.example.com:8000 max_fails=3 fail_timeout=30s;
    server shannon3.example.com:8000 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    server_name shannon.example.com;

    location / {
        proxy_pass http://shannon_backends;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Vertical Scaling

```bash
# Increase resource limits in systemd service
sudo systemctl edit shannon

# Add:
[Service]
MemoryLimit=16G
CPUQuota=800%  # 8 cores
```

## Migration Guide

### Upgrading from v2.0 to v2.1

**Breaking Changes**:
- Context management now manual (was automatic)
- Reflection stages increased from 3 to 5
- DNA genes expanded from 5 to 7

**Migration Steps**:

1. **Update configuration**:
```yaml
# Add new settings
context:
  checkpoint_frequency: 5  # NEW

reflection:
  pattern_learning: true    # NEW (Stage 4)
  memory_persistence: true  # NEW (Stage 5)
```

2. **Update code for manual checkpoints**:
```python
# OLD (automatic)
orchestrator.execute()

# NEW (manual checkpoints)
from shannon.memory import ContextMonitor
monitor = ContextMonitor()
checkpoint = monitor.create_checkpoint("before_risky_operation")
orchestrator.execute()
```

3. **Test thoroughly**:
```bash
pytest tests/ --verbose
```

## Related Documentation

- **OVERVIEW.md**: System architecture and components
- **MODULES.md**: Detailed module documentation
- **PATTERNS.md**: 96 design patterns
- **DATA_FLOW.md**: Component interactions and pipelines

## Support

- **Documentation**: https://shannon-framework.readthedocs.io
- **Issues**: https://github.com/your-org/shannon/issues
- **Discussions**: https://github.com/your-org/shannon/discussions
- **Email**: support@shannon-framework.com