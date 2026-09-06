# Help for Reflow commands executed from the local virtual environment.

.PHONY: help-local-init help-local-reflow
help-local-init:
	@echo [Local Initialization] $(call HELP_TOTAL,LOCAL_INIT)
	@echo $(HELP_SEPARATOR)
	@$(ECHO_BLANK)
	@echo   make l-init                         $(HELP_COLUMN_SEPARATOR)    Run reflow init with custom variables
	@echo   make l-init-dryrun                  $(HELP_COLUMN_SEPARATOR)    Preview initialization without writes
	@echo   make l-init-force                   $(HELP_COLUMN_SEPARATOR)    Overwrite existing initialization files
	@echo   make l-init-ask                     $(HELP_COLUMN_SEPARATOR)    Ask before overwriting files
	@echo   make l-init-all                     $(HELP_COLUMN_SEPARATOR)    Initialize all supported resources
	@echo   make l-init-config                  $(HELP_COLUMN_SEPARATOR)    Initialize configuration only
	@echo $(HELP_SEPARATOR)
	@$(ECHO_BLANK)

help-local-reflow:
	@echo [Local Reflow Workflows] $(call HELP_TOTAL,LOCAL_REFLOW)
	@echo $(HELP_SEPARATOR)
	@$(ECHO_BLANK)
	@echo   make l-reflow-releases-recover     $(HELP_COLUMN_SEPARATOR)    Retrigger missing release automation
	@echo   make l-reflow-releases-recover-dryrun $(HELP_COLUMN_SEPARATOR)  Preview release recovery
	@echo   make l-reflow-tags-convert-local   $(HELP_COLUMN_SEPARATOR)    Replace tags in a local checkout
	@echo   make l-reflow-tags-convert-local-dryrun $(HELP_COLUMN_SEPARATOR) Preview local replacement
	@echo   make l-reflow-tags-convert-remote  $(HELP_COLUMN_SEPARATOR)    Replace tags on the Git remote
	@echo   make l-reflow-tags-convert-remote-dryrun $(HELP_COLUMN_SEPARATOR) Preview remote replacement
	@echo   make l-reflow-dockerize            $(HELP_COLUMN_SEPARATOR)    Build and publish configured release images
	@echo   make l-reflow-dockerize-dryrun     $(HELP_COLUMN_SEPARATOR)    Preview Docker release automation
	@$(ECHO_BLANK)
	@echo   make l-reflow-tags-replay          $(HELP_COLUMN_SEPARATOR)    Deprecated alias for releases recover
	@echo   make l-reflow-tags-replay-dryrun   $(HELP_COLUMN_SEPARATOR)    Deprecated dry-run alias
	@echo   make l-reflow-tags-convert         $(HELP_COLUMN_SEPARATOR)    Compatibility alias for local conversion
	@echo   make l-reflow-tags-convert-dryrun  $(HELP_COLUMN_SEPARATOR)    Compatibility alias for local dry-run
	@echo $(HELP_SEPARATOR)
	@$(ECHO_BLANK)
