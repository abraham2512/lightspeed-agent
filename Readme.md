# Pipeline log analysis using Openshift Lightspeed Service
### This project is a work in progress, feel free to contribute
Log Analyzer using Openshift Lightspeed Service with Jira integration

## Prerequisites:
* OpenShift lightspeed-service with jira mcp server - https://github.com/abraham2512/lightspeed-service
* Ollama server - https://ollama.com/download/linux
* Logjuicer - https://github.com/logjuicer/logjuicer
* Jira access (for Jira integration features)

## Directory Structure:

* `agent.py` - Python interface with Jira integration
* `logjuicer.yaml` - Configuration file for logjuicer
* `baselines/` - Directory for individual test baselines

## Features:

### Core Functionality:
* **ASK** - Ask product questions about OpenShift
* **ANALYZE** - Analyze logfiles using baselines
* **ANALYZE-WITH-JIRA** - Analyze logfiles and find related Jira issues

### Jira Integration:
* Search for related Jira issues in OCPBUGS and CNF projects
* Get detailed issue information including status, assignee, and descriptions
* Formatted output for easy reading
* Automatic issue correlation with log analysis

## How to run:

### Basic Usage:
```bash
# Ask a product question about OpenShift
python agent.py ask "what is ACM?"

# Analyze a logfile using baseline comparison
python agent.py analyze logfile.log

# Analyze a logfile and find related Jira issues
python agent.py analyze-with-jira logfile.log OCPBUGS
```

### Jira Integration Examples:
```bash
# Search for Jira issues related to performance profiles
python agent.py ask "search for Jira issues related to performance profile in OCPBUGS"

# Analyze a specific failure and find related issues
python agent.py analyze-with-jira oslat_failure_cnfdg15.txt OCPBUGS
```

### Log Analysis Enhancements:
* Better triage summaries with failure details
* Relevant must-gather log file identification
* Integration with Jira for issue correlation

## Configuration:

The system automatically detects Jira configuration from the lightspeed-service setup. No additional configuration is required for basic usage.

## Output Format:

The system now provides:
1. **Main Analysis**: Triage summary and log analysis
2. **Tool Results**: Formatted Jira search results with issue details
3. **Debug Information**: Response structure and tool status (when needed)

Example output structure:
```
------------------------------------------->
### Triage Summary:
[Analysis of the log failure]

### Relevant Must-Gather Log Files:
[Identified log file paths]

### Jira Search Results:
[Summary of found issues]
