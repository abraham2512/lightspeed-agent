test:
	python agent.py analyze oslat_failure_cnfdg15.log
test-ols: ## Run the service locally
	python agent.py ask what is OLS?
test-logjuicer:
	python logjuicer.py
