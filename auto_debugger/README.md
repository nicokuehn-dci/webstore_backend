# Auto Debugger Service

Automated debugging and code analysis service for the WebStore application.

## Features

- **Real-time Code Analysis**: Continuous monitoring of code changes
- **Error Detection**: Syntax errors, runtime errors, and potential issues
- **Code Quality Checks**: PEP 8 compliance, complexity analysis, naming conventions
- **Performance Analysis**: Loop optimization, import efficiency, string operations
- **Comprehensive Reporting**: HTML and JSON reports with actionable insights
- **Configurable**: Customizable rules and thresholds

## Quick Start

### CLI Usage

```bash
# Run a one-time analysis
python auto_debugger/debug_cli.py scan

# Start continuous monitoring
python auto_debugger/debug_cli.py monitor --interval 30

# Generate detailed report
python auto_debugger/debug_cli.py report

# Check debugger status
python auto_debugger/debug_cli.py status
```

### Programmatic Usage

```python
from auto_debugger.src.debugger import AutoDebugger

# Initialize debugger
debugger = AutoDebugger(project_root="/path/to/webstore")

# Run analysis
results = debugger.run_full_analysis()

# Start monitoring
debugger.start_monitoring(interval=30)

# Get statistics
stats = debugger.get_statistics()
health = debugger.get_health_status()
```

## Integration with WebStore

The debugger can be integrated into the main webstore application:

```python
# In webstore.py, add debug option
elif sys.argv[1] == '--debug':
    from auto_debugger.src.debugger import AutoDebugger
    debugger = AutoDebugger()
    debugger.start_monitoring()
```

## Configuration

Edit `auto_debugger/config/debug_config.json` to customize:

- **Analysis Rules**: Line length, complexity thresholds
- **Monitoring**: Scan intervals, auto-fix options
- **Reporting**: Output formats, retention policies
- **Exclusions**: Files and directories to skip

## Output

### Console Output
- Real-time error and warning messages
- Summary statistics
- Health status indicators

### Reports
- **JSON Reports**: Machine-readable analysis results
- **HTML Reports**: Human-friendly visual reports
- **Logs**: Detailed debugging information

## Error Types Detected

- **Syntax Errors**: Parse failures, invalid syntax
- **Code Quality**: PEP 8 violations, naming issues
- **Performance**: Inefficient loops, string operations
- **Potential Runtime Errors**: Undefined variables, attribute errors

## File Structure

```
auto_debugger/
├── src/
│   ├── debugger.py          # Main debugger service
│   ├── analyzers/           # Code analysis modules
│   │   ├── code_analyzer.py
│   │   ├── error_detector.py
│   │   └── performance_analyzer.py
│   ├── handlers/            # Output handlers
│   │   ├── log_handler.py
│   │   └── report_handler.py
│   └── utils/               # Utility modules
│       ├── config.py
│       └── file_scanner.py
├── config/
│   └── debug_config.json    # Configuration file
├── logs/                    # Log files
├── reports/                 # Generated reports
└── debug_cli.py             # Command-line interface
```

## Requirements

- Python 3.7+
- Standard library only (no external dependencies)

## License

MIT License - Same as WebStore application
