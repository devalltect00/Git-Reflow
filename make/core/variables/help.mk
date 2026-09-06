# Help text for commonly overridden Make variables.

.PHONY: help-variables
help-variables:
	@echo [Common Variables]
	@echo $(HELP_SEPARATOR)
	@$(ECHO_BLANK)
	@echo   REFLOW_GLOBAL_ARGS="args"           $(HELP_COLUMN_SEPARATOR)    Global Reflow options, including repository and dry-run
	@echo   REFLOW_INIT_ARGS="args"             $(HELP_COLUMN_SEPARATOR)    Options passed to reflow init
	@echo   REFLOW_RELEASES_RECOVER_ARGS="args" $(HELP_COLUMN_SEPARATOR)    Options passed to releases recover
	@echo   REFLOW_TAGS_CONVERT_ARGS="args"     $(HELP_COLUMN_SEPARATOR)    Options passed after tags convert local/remote
	@echo   REFLOW_DOCKERIZE_ARGS="args"        $(HELP_COLUMN_SEPARATOR)    Options passed to dockerize
	@$(ECHO_BLANK)
	@echo   VENV_NAME=name                      $(HELP_COLUMN_SEPARATOR)    Virtual environment directory, default: venv
	@echo   TARGET=path                         $(HELP_COLUMN_SEPARATOR)    Target used by remote utility commands
	@echo   PHS_SCAN_TARGETS="paths"            $(HELP_COLUMN_SEPARATOR)    Path Header Scanner apply-all targets
	@$(ECHO_BLANK)
	@echo   DOCKER_TAG=tag                      $(HELP_COLUMN_SEPARATOR)    Local Docker image tag, default: latest
	@echo   DOCKER_TTY=                         $(HELP_COLUMN_SEPARATOR)    Disable interactive Docker flags for automation
	@echo   DOCKER_WORKSPACE_HOST=path          $(HELP_COLUMN_SEPARATOR)    Host repository mounted by direct Docker commands
	@echo   DOCKER_RUNTIME_ARGS="args"          $(HELP_COLUMN_SEPARATOR)    Extra docker run options
	@echo   CUSTY_CREDENTIALS_MOUNT=true/false  $(HELP_COLUMN_SEPARATOR)    Opt in to the read-only Custy credential mount
	@echo   CUSTY_CREDENTIALS_HOST_DIR=path     $(HELP_COLUMN_SEPARATOR)    External host credential directory
	@echo   CUSTY_CREDENTIALS_CONTAINER_DIR=path $(HELP_COLUMN_SEPARATOR)   Container credential directory
	@echo   CUSTY_CREDENTIALS_REMOTE=name       $(HELP_COLUMN_SEPARATOR)    Remote tested by credential helper targets
	@$(ECHO_BLANK)
	@echo   GHCR_REGISTRY=host                  $(HELP_COLUMN_SEPARATOR)    Published container registry host
	@echo   GHCR_OWNER=owner                    $(HELP_COLUMN_SEPARATOR)    Published container registry owner
	@echo   REMOTE_TAG=tag                      $(HELP_COLUMN_SEPARATOR)    Published image tag, default: latest
	@echo   REMOTE_WORKSPACE=path               $(HELP_COLUMN_SEPARATOR)    Host workspace mounted into a remote container
	@echo   REMOTE_IMAGE_PHS=name               $(HELP_COLUMN_SEPARATOR)    Path Header Scanner image repository
	@echo   REMOTE_IMAGE_DOC_GEN=name           $(HELP_COLUMN_SEPARATOR)    Doc Gen image repository
	@echo   REMOTE_IMAGE_CUSTY=name             $(HELP_COLUMN_SEPARATOR)    Custy image repository
	@echo   REMOTE_IMAGE_REFLOW=name            $(HELP_COLUMN_SEPARATOR)    Reflow image repository
	@echo $(HELP_SEPARATOR)
	@$(ECHO_BLANK)
