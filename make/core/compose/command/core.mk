# Reflow and developer utility commands executed through Docker Compose.

COMPOSE_INIT_COMMANDS_LIST := c-init c-init-dryrun c-init-force c-init-ask c-init-all c-init-config
COMPOSE_REFLOW_COMMANDS_LIST := \
	c-reflow-releases-recover c-reflow-releases-recover-dryrun \
	c-reflow-tags-replay c-reflow-tags-replay-dryrun \
	c-reflow-tags-convert c-reflow-tags-convert-dryrun \
	c-reflow-tags-convert-local c-reflow-tags-convert-local-dryrun \
	c-reflow-tags-convert-remote c-reflow-tags-convert-remote-dryrun \
	c-reflow-dockerize c-reflow-dockerize-dryrun
COMPOSE_UTILITIES_COMMANDS_LIST := \
	c-test c-lint c-lint-fix c-format c-format-check c-docs c-shell \
	c-build-package c-exec-shell c-fix c-check c-qa c-ci

$(foreach cmd,$(COMPOSE_INIT_COMMANDS_LIST),$(eval $(call REGISTER_COMMAND,COMPOSE_INIT,$(cmd),COMPOSE)))
$(foreach cmd,$(COMPOSE_REFLOW_COMMANDS_LIST),$(eval $(call REGISTER_COMMAND,COMPOSE_REFLOW,$(cmd),COMPOSE)))
$(foreach cmd,$(COMPOSE_UTILITIES_COMMANDS_LIST),$(eval $(call REGISTER_COMMAND,COMPOSE_UTILITIES,$(cmd),COMPOSE)))

.PHONY: c-init
c-init: docker-check
	$(COMPOSE_PROD_RUN_APP) \
		$(COMPOSE_REFLOW_GLOBAL_ARGS) \
		init \
		$(COMPOSE_REFLOW_INIT_ARGS) \
		$(COMPOSE_REFLOW_EXTRA_ARGS)

.PHONY: c-init-dryrun c-init-force c-init-ask c-init-all c-init-config
c-init-dryrun: override COMPOSE_REFLOW_GLOBAL_ARGS += --dry-run
c-init-dryrun: c-init

c-init-force: override COMPOSE_REFLOW_INIT_ARGS += --force
c-init-force: c-init

c-init-ask: override COMPOSE_REFLOW_INIT_ARGS += --ask
c-init-ask: c-init

c-init-all: override COMPOSE_REFLOW_INIT_ARGS += --mode all
c-init-all: c-init

c-init-config: override COMPOSE_REFLOW_INIT_ARGS += --mode config
c-init-config: c-init

.PHONY: c-reflow-releases-recover
c-reflow-releases-recover: docker-check
	$(COMPOSE_PROD_RUN_APP) \
		$(COMPOSE_REFLOW_GLOBAL_ARGS) \
		releases recover \
		$(COMPOSE_REFLOW_RELEASES_RECOVER_ARGS) \
		$(COMPOSE_REFLOW_EXTRA_ARGS)

.PHONY: c-reflow-releases-recover-dryrun
c-reflow-releases-recover-dryrun: override COMPOSE_REFLOW_GLOBAL_ARGS += --dry-run
c-reflow-releases-recover-dryrun: c-reflow-releases-recover

.PHONY: c-reflow-tags-replay c-reflow-tags-replay-dryrun
c-reflow-tags-replay:
	@echo WARNING: c-reflow-tags-replay is deprecated - use c-reflow-releases-recover.
	@$(MAKE) --no-print-directory c-reflow-releases-recover \
		COMPOSE_REFLOW_GLOBAL_ARGS="$(COMPOSE_REFLOW_GLOBAL_ARGS)" \
		COMPOSE_REFLOW_RELEASES_RECOVER_ARGS="$(COMPOSE_REFLOW_RELEASES_RECOVER_ARGS)" \
		COMPOSE_REFLOW_EXTRA_ARGS="$(COMPOSE_REFLOW_EXTRA_ARGS)"

c-reflow-tags-replay-dryrun:
	@echo WARNING: c-reflow-tags-replay-dryrun is deprecated - use c-reflow-releases-recover-dryrun.
	@$(MAKE) --no-print-directory c-reflow-releases-recover-dryrun \
		COMPOSE_REFLOW_GLOBAL_ARGS="$(COMPOSE_REFLOW_GLOBAL_ARGS)" \
		COMPOSE_REFLOW_RELEASES_RECOVER_ARGS="$(COMPOSE_REFLOW_RELEASES_RECOVER_ARGS)" \
		COMPOSE_REFLOW_EXTRA_ARGS="$(COMPOSE_REFLOW_EXTRA_ARGS)"

.PHONY: c-reflow-tags-convert-local
c-reflow-tags-convert-local: docker-check
	$(COMPOSE_PROD_RUN_APP) \
		$(COMPOSE_REFLOW_GLOBAL_ARGS) \
		tags convert local \
		$(COMPOSE_REFLOW_TAGS_CONVERT_ARGS) \
		$(COMPOSE_REFLOW_EXTRA_ARGS)

.PHONY: c-reflow-tags-convert-local-dryrun
c-reflow-tags-convert-local-dryrun: override COMPOSE_REFLOW_GLOBAL_ARGS += --dry-run
c-reflow-tags-convert-local-dryrun: c-reflow-tags-convert-local

.PHONY: c-reflow-tags-convert-remote
c-reflow-tags-convert-remote: docker-check
	$(COMPOSE_PROD_RUN_APP) \
		$(COMPOSE_REFLOW_GLOBAL_ARGS) \
		tags convert remote \
		$(COMPOSE_REFLOW_TAGS_CONVERT_ARGS) \
		$(COMPOSE_REFLOW_EXTRA_ARGS)

.PHONY: c-reflow-tags-convert-remote-dryrun
c-reflow-tags-convert-remote-dryrun: override COMPOSE_REFLOW_GLOBAL_ARGS += --dry-run
c-reflow-tags-convert-remote-dryrun: c-reflow-tags-convert-remote

.PHONY: c-reflow-tags-convert c-reflow-tags-convert-dryrun
c-reflow-tags-convert: c-reflow-tags-convert-local
c-reflow-tags-convert-dryrun: c-reflow-tags-convert-local-dryrun

.PHONY: c-reflow-dockerize
c-reflow-dockerize: docker-check
	$(COMPOSE_PROD_RUN_APP) \
		$(COMPOSE_REFLOW_GLOBAL_ARGS) \
		dockerize \
		$(COMPOSE_REFLOW_DOCKERIZE_ARGS) \
		$(COMPOSE_REFLOW_EXTRA_ARGS)

.PHONY: c-reflow-dockerize-dryrun
c-reflow-dockerize-dryrun: override COMPOSE_REFLOW_GLOBAL_ARGS += --dry-run
c-reflow-dockerize-dryrun: c-reflow-dockerize

.PHONY: c-test c-lint c-lint-fix c-format c-format-check c-docs c-shell c-build-package c-exec-shell
c-test: c-build-dev
	$(COMPOSE_DEV_RUN_TEST)

c-lint: c-build-dev
	$(COMPOSE_DEV_RUN_LINT)

c-lint-fix: c-build-dev
	$(COMPOSE_DEV_RUN_LINT_FIX)

c-format: c-build-dev
	$(COMPOSE_DEV_RUN_FORMAT)

c-format-check: c-build-dev
	$(COMPOSE_DEV_RUN_FORMAT_CHECK)

c-docs: docker-check
	$(COMPOSE_DEV_UP_DOCS) -d

c-shell: c-build-dev
	$(COMPOSE_DEV_RUN_SHELL)

c-build-package: c-build-dev
	$(COMPOSE_DEV_RUN_BUILD)

c-exec-shell: docker-check
	$(COMPOSE_DEV_EXEC) $(SERVICE_APP) $(SHELL_BIN)

.PHONY: c-fix c-check c-qa c-ci
c-fix: docker-check
	@$(MAKE) --no-print-directory c-format
	@$(MAKE) --no-print-directory c-lint-fix

c-check: docker-check
	@$(MAKE) --no-print-directory c-format-check
	@$(MAKE) --no-print-directory c-lint
	@$(MAKE) --no-print-directory c-test

c-qa: docker-check
	@$(MAKE) --no-print-directory c-fix
	@$(MAKE) --no-print-directory c-check

c-ci: docker-check
	@$(MAKE) --no-print-directory c-build-dev
	@$(MAKE) --no-print-directory c-check
