# Pipeline log analysis using Openshift Lightspeed Service
### This project is a PoC and work is in progress
Log Analyzer using Openshift Lightspeed Service

Prerequisites:
* OpenShift lightspeed-service - https://github.com/openshift/lightspeed-service
* Ollama server - https://ollama.com/download/linux
* Logjuicer - https://github.com/logjuicer/logjuicer

Directory Structure:

* agent.py - python interface
* logjuicer.config - ignore patterns for logjuicer
* baselines/ - directory for individual test baselines

How to run:
* ASK - ask a product question about OpenShift

`python agent.py ask what is acm?`

* ANALYZE - analyze a logfile related to OpenShift using a baseline

`python agent.py analyze logfile.log`