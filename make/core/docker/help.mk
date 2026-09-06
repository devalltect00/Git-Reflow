# Help for direct Docker workflows.

.PHONY: help-docker-build help-docker-testing help-docker-init help-docker-reflow
help-docker-build:
	@echo [Docker Images] $(call HELP_TOTAL,DOCKER_INFRASTRUCTURE)
	@echo $(HELP_SEPARATOR)
	@$(ECHO_BLANK)
	@echo   make d-build-base                   $(HELP_COLUMN_SEPARATOR)    Build the base image
	@echo   make d-build-dev                    $(HELP_COLUMN_SEPARATOR)    Build the development image
	@echo   make d-build-prod                   $(HELP_COLUMN_SEPARATOR)    Build the production image
	@echo   make d-build-all                    $(HELP_COLUMN_SEPARATOR)    Build every local image
	@echo $(HELP_SEPARATOR)
	@$(ECHO_BLANK)

help-docker-testing:
	@echo [Docker Testing] $(call HELP_TOTAL,DOCKER_TESTING)
	@echo $(HELP_SEPARATOR)
	@$(ECHO_BLANK)
	@echo   make d-test                         $(HELP_COLUMN_SEPARATOR)    Build the development image and run pytest
	@echo $(HELP_SEPARATOR)
	@$(ECHO_BLANK)

help-docker-init:
	@echo [Docker Initialization] $(call HELP_TOTAL,DOCKER_INIT)
	@echo $(HELP_SEPARATOR)
	@$(ECHO_BLANK)
	@echo   make d-init                         $(HELP_COLUMN_SEPARATOR)    Run reflow init in the production image
	@echo   make d-init-dryrun                  $(HELP_COLUMN_SEPARATOR)    Preview initialization
	@echo   make d-init-force                   $(HELP_COLUMN_SEPARATOR)    Force initialization
	@echo   make d-init-ask                     $(HELP_COLUMN_SEPARATOR)    Prompt before overwriting
	@echo   make d-init-all                     $(HELP_COLUMN_SEPARATOR)    Initialize all resources
	@echo   make d-init-config                  $(HELP_COLUMN_SEPARATOR)    Initialize configuration only
	@echo $(HELP_SEPARATOR)
	@$(ECHO_BLANK)

help-docker-reflow:
	@echo [Docker Reflow Workflows] $(call HELP_TOTAL,DOCKER_REFLOW)
	@echo $(HELP_SEPARATOR)
	@$(ECHO_BLANK)
	@echo   make d-reflow-releases-recover     $(HELP_COLUMN_SEPARATOR)    Run release recovery in Docker
	@echo   make d-reflow-releases-recover-dryrun $(HELP_COLUMN_SEPARATOR)  Preview release recovery
	@echo   make d-reflow-tags-convert-local   $(HELP_COLUMN_SEPARATOR)    Replace local tags in Docker
	@echo   make d-reflow-tags-convert-local-dryrun $(HELP_COLUMN_SEPARATOR) Preview local replacement
	@echo   make d-reflow-tags-convert-remote  $(HELP_COLUMN_SEPARATOR)    Replace remote tags from Docker
	@echo   make d-reflow-tags-convert-remote-dryrun $(HELP_COLUMN_SEPARATOR) Preview remote replacement
	@echo   make d-reflow-dockerize            $(HELP_COLUMN_SEPARATOR)    Run Docker release automation
	@echo   make d-reflow-dockerize-dryrun     $(HELP_COLUMN_SEPARATOR)    Preview Docker release automation
	@$(ECHO_BLANK)
	@echo   make d-reflow-tags-replay          $(HELP_COLUMN_SEPARATOR)    Deprecated recovery alias
	@echo   make d-reflow-tags-replay-dryrun   $(HELP_COLUMN_SEPARATOR)    Deprecated dry-run alias
	@echo   make d-reflow-tags-convert         $(HELP_COLUMN_SEPARATOR)    Compatibility alias for local conversion
	@echo   make d-reflow-tags-convert-dryrun  $(HELP_COLUMN_SEPARATOR)    Compatibility alias for local dry-run
	@echo $(HELP_SEPARATOR)
	@$(ECHO_BLANK)
