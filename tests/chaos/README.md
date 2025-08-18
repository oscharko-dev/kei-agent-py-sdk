# Chaos Engineering Test Suite

## 🔥 Overview

This comprehensive chaos engineering test suite validates the resilience and fault tolerance of the KEI-Agent Python SDK under various failure conditions. The suite includes automated chaos injection, metrics collection, and detailed reporting to ensure the system maintains core functionality during adverse conditions.

## 🎯 Key Features

- **Comprehensive Coverage**: Tests network, service dependency, resource exhaustion, configuration, and security failure scenarios
- **Automated Chaos Injection**: Programmatic injection of various failure types with controlled intensity
- **Real-time Metrics Collection**: Continuous monitoring of system behavior during chaos tests
- **Resilience Scoring**: Automated calculation of resilience scores for different system components
- **CI/CD Integration**: GitHub Actions workflow for automated chaos testing
- **Safety Mechanisms**: Built-in safety checks and automatic cleanup to prevent system damage
- **Detailed Reporting**: Comprehensive reports with recommendations for system improvements

## 📁 Test Categories

### 🌐 Network Chaos (`test_network_chaos.py`)
- Network latency and packet loss simulation
- Connection failure and retry mechanism testing
- Protocol failover validation (RPC, Stream, Bus, MCP)
- Circuit breaker pattern testing
- Intermittent connectivity scenarios

### 🔗 Service Dependency Chaos (`test_service_dependency_chaos.py`)
- Authentication service failure simulation
- Metrics collection service outages
- Configuration service unavailability
- Multiple simultaneous service failures
- Graceful degradation testing

### 💾 Resource Exhaustion Chaos (`test_resource_exhaustion_chaos.py`)
- Memory pressure simulation
- CPU throttling scenarios
- Connection pool exhaustion
- Rate limiting and backpressure testing
- Disk space constraint simulation

### ⚙️ Configuration Chaos (`test_configuration_chaos.py`)
- Invalid configuration injection
- Configuration file corruption
- Rollback mechanism testing
- Concurrent configuration updates
- Hot-reload failure scenarios

### 🔒 Security Chaos (`test_security_chaos.py`)
- Authentication token expiration
- SSL certificate validation failures
- Security attack pattern detection
- Rate limiting bypass attempts
- Comprehensive security resilience testing

## 🚀 Quick Start

### Running Basic Tests

```bash
# Install dependencies
pip install -e ".[dev,test]"
pip install pytest-asyncio pytest-timeout psutil watchdog

# Run basic chaos framework test
python -m pytest tests/test_chaos_basic.py -v

# Run specific chaos category
python -m pytest tests/chaos/test_network_chaos.py -v

# Run with timeout protection
python -m pytest tests/chaos/test_network_chaos.py --timeout=300 -v
```

### Running Complete Test Suite

```bash
# Run all chaos tests with integration framework
python tests/chaos/chaos_integration.py

# Run specific categories
python tests/chaos/chaos_integration.py --categories network,security

# Generate detailed report
python tests/chaos/chaos_integration.py --output chaos-report.json --verbose

# Run in safe mode (recommended)
python tests/chaos/chaos_integration.py --safe-mode
```

### Demo Execution

```bash
# Run the chaos engineering demo
python -c "
import asyncio
from tests.chaos.chaos_framework import chaos_test_context

async def demo():
    async with chaos_test_context('demo') as test:
        test.record_operation(True)
        print('✅ Chaos framework working!')

asyncio.run(demo())
"
```

## 📊 Metrics and Reporting

### Resilience Scores

The framework calculates resilience scores based on:

- **Availability Score** (0-100%): Success rate during chaos injection
- **Recovery Score** (0-100%): Speed of recovery after failures
- **Error Handling Score** (0-100%): Quality of error handling during chaos
- **Overall Score**: Weighted average of component scores

### Sample Report Structure

```json
{
  "summary": {
    "total_tests": 25,
    "overall_resilience_score": 85.2,
    "components_tested": ["network", "security", "configuration"]
  },
  "resilience_scores": {
    "network": {
      "overall_score": 88.5,
      "availability_score": 85.0,
      "recovery_score": 92.0,
      "error_handling_score": 88.5
    }
  },
  "recommendations": [
    "Improve network recovery time with faster health checks",
    "Enhance security error handling mechanisms"
  ]
}
```

## 🔧 Framework Components

### Core Framework (`chaos_framework.py`)

- **ChaosTest**: Base class for chaos engineering tests
- **ChaosInjector**: Abstract base for chaos injection mechanisms
- **ChaosMetrics**: Comprehensive metrics collection
- **chaos_test_context**: Context manager for safe test execution

### Chaos Injectors

- **NetworkChaosInjector**: Network latency, packet loss, connection failures
- **ServiceDependencyChaosInjector**: Service failure simulation
- **ResourceExhaustionInjector**: Memory, CPU, and disk pressure
- **ConfigurationChaosInjector**: Configuration corruption and validation failures
- **SecurityChaosInjector**: Authentication and security attack simulation

### Metrics Collection (`chaos_metrics.py`)

- **ChaosMetricsCollector**: Aggregates and analyzes test results
- **ResilienceScore**: Calculated resilience metrics
- Trend analysis and performance impact assessment
- Automated recommendation generation

## 🛡️ Safety Mechanisms

### Pre-Test Safety Checks
- System resource validation (memory < 90%, CPU < 90%, disk < 95%)
- Environment verification
- Service health checks

### During Test Execution
- Real-time resource monitoring
- Automatic test termination on resource exhaustion
- Controlled chaos intensity with gradual escalation
- Continuous system health monitoring

### Post-Test Cleanup
- Automatic resource cleanup and restoration
- System stabilization verification
- Resource leak detection and cleanup
- Process cleanup and verification

## 🔄 CI/CD Integration

### GitHub Actions Workflow

The chaos tests are integrated into CI/CD pipelines with:

- **Scheduled Execution**: Daily chaos testing at 2 AM UTC
- **Manual Triggers**: On-demand execution with configurable parameters
- **Pull Request Integration**: Chaos testing on code changes
- **Automated Reporting**: Results posted as PR comments
- **Failure Notifications**: Automatic issue creation on test failures

### Environment Configuration

```yaml
env:
  CHAOS_ENV: staging
  CHAOS_SAFE_MODE: true
  CHAOS_CATEGORIES: network,service_dependency,resource_exhaustion
```

## 📈 Best Practices

### Test Development
1. **Start Simple**: Begin with basic chaos scenarios
2. **Gradual Intensity**: Increase chaos intensity progressively
3. **Comprehensive Coverage**: Test all critical system paths
4. **Real-World Modeling**: Base scenarios on actual failure patterns
5. **Automated Validation**: Include clear success/failure criteria

### Production Readiness
1. **Staging First**: Always validate in staging environments
2. **Gradual Rollout**: Start with limited scope in production
3. **Comprehensive Monitoring**: Ensure full observability during tests
4. **Immediate Rollback**: Have instant rollback capabilities
5. **Team Coordination**: Coordinate with operations and on-call teams

### Continuous Improvement
1. **Regular Execution**: Run chaos tests on a regular schedule
2. **Metric Tracking**: Monitor resilience trends over time
3. **Failure Analysis**: Learn from each failure scenario
4. **System Hardening**: Implement improvements based on results
5. **Knowledge Sharing**: Document learnings and share with team

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
   ```bash
   pip install -e ".[dev,test]"
   pip install pytest-asyncio psutil watchdog
   ```

2. **Resource Constraints**: Check system resources before testing
   ```bash
   python -c "import psutil; print(f'Memory: {psutil.virtual_memory().percent}%')"
   ```

3. **Permission Issues**: Ensure proper file system permissions
4. **Network Connectivity**: Verify network access for service tests
5. **Timeout Errors**: Adjust timeout values for slower systems

### Debug Mode

```bash
# Run with verbose logging
python tests/chaos/chaos_integration.py --verbose

# Run single test with detailed output
python -m pytest tests/chaos/test_network_chaos.py -v -s --tb=long

# Check framework functionality
python -c "from tests.chaos.chaos_framework import chaos_test_context; print('✅ Framework OK')"
```

## 🤝 Contributing

### Adding New Chaos Tests

1. Create test class inheriting from appropriate base
2. Implement chaos injection mechanisms with proper cleanup
3. Add comprehensive assertions and metrics collection
4. Include safety mechanisms and resource monitoring
5. Update documentation and integration framework

### Extending Framework

1. Follow existing patterns and conventions
2. Add comprehensive error handling and logging
3. Include safety mechanisms and resource limits
4. Add metrics collection and reporting
5. Update integration framework and CI/CD workflows

## 📚 Additional Resources

- [Chaos Engineering Documentation](../../docs/chaos-engineering.md)
- [Framework API Reference](chaos_framework.py)
- [Metrics Collection Guide](chaos_metrics.py)
- [CI/CD Integration](../../.github/workflows/chaos-testing.yml)

## 🎉 Success Metrics

A successful chaos engineering implementation should achieve:

- **Resilience Score > 80%**: Overall system resilience above 80%
- **Recovery Time < 30s**: System recovery within 30 seconds
- **Zero Critical Failures**: No complete system failures during chaos
- **Graceful Degradation**: Maintained core functionality during failures
- **Automated Recovery**: Self-healing capabilities demonstrated

---

**🔥 Ready to test your system's resilience? Start with the basic tests and gradually increase the chaos intensity!**
