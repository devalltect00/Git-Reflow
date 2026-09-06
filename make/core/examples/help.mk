# Practical examples for common Reflow Make workflows.

.PHONY: help-examples
help-examples:
	@echo [Examples]
	@echo $(HELP_SEPARATOR)
	@$(ECHO_BLANK)
	@echo [Local Reflow Workflow]
	@echo   make setup
	@echo   make l-reflow-tags-convert-dryrun REFLOW_GLOBAL_ARGS="--repository D:/project/testing_lab/testing_reflow"
	@echo   make l-reflow-tags-convert REFLOW_GLOBAL_ARGS="--repository D:/project/testing_lab/testing_reflow" REFLOW_TAGS_CONVERT_ARGS="--to semver --yes"
	@echo   make l-reflow-releases-recover-dryrun REFLOW_GLOBAL_ARGS="--repository-url https://github.com/owner/repository.git"
	@$(ECHO_BLANK)
	@echo [Docker and Compose Workflow]
	@echo   make d-build-all
	@echo   make c-check
	@$(ECHO_BLANK)
	@echo [Published Image Registry Workflow]
	@echo   make r-phs-pull REMOTE_TAG=latest
	@echo   make r-doc-gen-pull REMOTE_TAG=latest
	@echo   make r-custy-pull REMOTE_TAG=latest
	@echo   make r-reflow-pull REMOTE_TAG=latest
	@$(ECHO_BLANK)
	@echo [Published Utility Runtime Workflow]
	@echo   make r-phs-scan TARGET=app REMOTE_WORKSPACE="D:/project/target"
	@echo   make r-doc-generate-smart REMOTE_WORKSPACE="D:/project/target"
	@echo   make r-custy-run-validate REMOTE_WORKSPACE="D:/project/target"
	@echo   make r-reflow-tags-convert-dryrun REMOTE_WORKSPACE="D:/project/target" REFLOW_TAGS_CONVERT_ARGS="--to pep440"
	@echo $(HELP_SEPARATOR)
	@$(ECHO_BLANK)
