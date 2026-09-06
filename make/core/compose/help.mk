# Help for Docker Compose workflows.

.PHONY: help-compose-infrastructure help-compose-init help-compose-reflow help-compose-utilities
help-compose-infrastructure:
	@echo [Compose Infrastructure] $(call HELP_TOTAL,COMPOSE_INFRASTRUCTURE)
	@echo $(HELP_SEPARATOR)
	@$(ECHO_BLANK)
	@echo   make c-build-base                   $(HELP_COLUMN_SEPARATOR)    Build the base service image
	@echo   make c-build-dev                    $(HELP_COLUMN_SEPARATOR)    Build the development app image
	@echo   make c-build-prod                   $(HELP_COLUMN_SEPARATOR)    Build the production app image
	@echo   make c-build-all                    $(HELP_COLUMN_SEPARATOR)    Build all Reflow Compose images
	@echo   make c-up                           $(HELP_COLUMN_SEPARATOR)    Start the development stack
	@echo   make c-up-build                     $(HELP_COLUMN_SEPARATOR)    Rebuild and start the stack
	@echo   make c-up-detached                  $(HELP_COLUMN_SEPARATOR)    Start in the background
	@echo   make c-down                         $(HELP_COLUMN_SEPARATOR)    Stop the stack
	@echo   make c-down-clean                   $(HELP_COLUMN_SEPARATOR)    Stop and remove project volumes
	@echo   make c-logs                         $(HELP_COLUMN_SEPARATOR)    Follow stack logs
	@echo $(HELP_SEPARATOR)
	@$(ECHO_BLANK)

help-compose-init:
	@echo [Compose Initialization] $(call HELP_TOTAL,COMPOSE_INIT)
	@echo $(HELP_SEPARATOR)
	@$(ECHO_BLANK)
	@echo   make c-init                         $(HELP_COLUMN_SEPARATOR)    Run reflow init through Compose
	@echo   make c-init-dryrun                  $(HELP_COLUMN_SEPARATOR)    Preview initialization
	@echo   make c-init-force                   $(HELP_COLUMN_SEPARATOR)    Force initialization
	@echo   make c-init-ask                     $(HELP_COLUMN_SEPARATOR)    Prompt before overwriting
	@echo   make c-init-all                     $(HELP_COLUMN_SEPARATOR)    Initialize all resources
	@echo   make c-init-config                  $(HELP_COLUMN_SEPARATOR)    Initialize configuration only
	@echo $(HELP_SEPARATOR)
	@$(ECHO_BLANK)

help-compose-reflow:
	@echo [Compose Reflow Workflows] $(call HELP_TOTAL,COMPOSE_REFLOW)
	@echo $(HELP_SEPARATOR)
	@$(ECHO_BLANK)
	@echo   make c-reflow-releases-recover     $(HELP_COLUMN_SEPARATOR)    Run release recovery
	@echo   make c-reflow-releases-recover-dryrun $(HELP_COLUMN_SEPARATOR)  Preview release recovery
	@echo   make c-reflow-tags-convert-local   $(HELP_COLUMN_SEPARATOR)    Replace local version tags
	@echo   make c-reflow-tags-convert-local-dryrun $(HELP_COLUMN_SEPARATOR) Preview local replacement
	@echo   make c-reflow-tags-convert-remote  $(HELP_COLUMN_SEPARATOR)    Replace remote version tags
	@echo   make c-reflow-tags-convert-remote-dryrun $(HELP_COLUMN_SEPARATOR) Preview remote replacement
	@echo   make c-reflow-dockerize            $(HELP_COLUMN_SEPARATOR)    Run Docker release automation
	@echo   make c-reflow-dockerize-dryrun     $(HELP_COLUMN_SEPARATOR)    Preview Docker release automation
	@$(ECHO_BLANK)
	@echo   make c-reflow-tags-replay          $(HELP_COLUMN_SEPARATOR)    Deprecated recovery alias
	@echo   make c-reflow-tags-replay-dryrun   $(HELP_COLUMN_SEPARATOR)    Deprecated dry-run alias
	@echo   make c-reflow-tags-convert         $(HELP_COLUMN_SEPARATOR)    Compatibility alias for local conversion
	@echo   make c-reflow-tags-convert-dryrun  $(HELP_COLUMN_SEPARATOR)    Compatibility alias for local dry-run
	@echo $(HELP_SEPARATOR)
	@$(ECHO_BLANK)

help-compose-utilities:
	@echo [Compose Developer Utilities] $(call HELP_TOTAL,COMPOSE_UTILITIES)
	@echo $(HELP_SEPARATOR)
	@$(ECHO_BLANK)
	@echo   make c-test                         $(HELP_COLUMN_SEPARATOR)    Build the app image and run tests
	@echo   make c-lint                         $(HELP_COLUMN_SEPARATOR)    Build the app image and run Ruff
	@echo   make c-lint-fix                     $(HELP_COLUMN_SEPARATOR)    Build the app image and apply Ruff fixes
	@echo   make c-format                       $(HELP_COLUMN_SEPARATOR)    Build the app image and run Black
	@echo   make c-format-check                 $(HELP_COLUMN_SEPARATOR)    Build the app image and check Black
	@echo   make c-docs                         $(HELP_COLUMN_SEPARATOR)    Start MkDocs
	@echo   make c-shell                        $(HELP_COLUMN_SEPARATOR)    Open a one-off shell
	@echo   make c-exec-shell                   $(HELP_COLUMN_SEPARATOR)    Open a shell in the running app service
	@echo   make c-build-package                $(HELP_COLUMN_SEPARATOR)    Build Python package artifacts
	@echo   make c-fix                          $(HELP_COLUMN_SEPARATOR)    Apply Compose formatting and lint fixes
	@echo   make c-check                        $(HELP_COLUMN_SEPARATOR)    Run Compose validation
	@echo   make c-qa                           $(HELP_COLUMN_SEPARATOR)    Run the full Compose QA workflow
	@echo   make c-ci                           $(HELP_COLUMN_SEPARATOR)    Build and validate the development stack
	@echo $(HELP_SEPARATOR)
	@$(ECHO_BLANK)
