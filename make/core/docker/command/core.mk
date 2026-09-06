# Reflow and test commands executed in local Docker images.

DOCKER_TESTING_COMMANDS_LIST := d-test
DOCKER_INIT_COMMANDS_LIST := d-init d-init-dryrun d-init-force d-init-ask d-init-all d-init-config
DOCKER_REFLOW_COMMANDS_LIST := \
	d-reflow-releases-recover d-reflow-releases-recover-dryrun \
	d-reflow-tags-replay d-reflow-tags-replay-dryrun \
	d-reflow-tags-convert d-reflow-tags-convert-dryrun \
	d-reflow-tags-convert-local d-reflow-tags-convert-local-dryrun \
	d-reflow-tags-convert-remote d-reflow-tags-convert-remote-dryrun \
	d-reflow-dockerize d-reflow-dockerize-dryrun

$(foreach cmd,$(DOCKER_TESTING_COMMANDS_LIST),$(eval $(call REGISTER_COMMAND,DOCKER_TESTING,$(cmd),DOCKER)))
$(foreach cmd,$(DOCKER_INIT_COMMANDS_LIST),$(eval $(call REGISTER_COMMAND,DOCKER_INIT,$(cmd),DOCKER)))
$(foreach cmd,$(DOCKER_REFLOW_COMMANDS_LIST),$(eval $(call REGISTER_COMMAND,DOCKER_REFLOW,$(cmd),DOCKER)))

.PHONY: d-test
d-test: d-build-dev
	$(DOCKER_RUN_NO_ENTRYPOINT) $(DOCKER_WORKSPACE) $(DOCKER_IMAGE_DEV) python -m pytest -v

.PHONY: d-init
d-init: docker-check
	$(DOCKER_RUN_INTERACTIVE) \
		$(DOCKER_WORKSPACE) \
		$(DOCKER_IMAGE_PROD) \
		$(DOCKER_REFLOW_GLOBAL_ARGS) \
		init \
		$(DOCKER_REFLOW_INIT_ARGS) \
		$(DOCKER_REFLOW_EXTRA_ARGS)

.PHONY: d-init-dryrun d-init-force d-init-ask d-init-all d-init-config
d-init-dryrun: override DOCKER_REFLOW_GLOBAL_ARGS += --dry-run
d-init-dryrun: d-init

d-init-force: override DOCKER_REFLOW_INIT_ARGS += --force
d-init-force: d-init

d-init-ask: override DOCKER_REFLOW_INIT_ARGS += --ask
d-init-ask: d-init

d-init-all: override DOCKER_REFLOW_INIT_ARGS += --mode all
d-init-all: d-init

d-init-config: override DOCKER_REFLOW_INIT_ARGS += --mode config
d-init-config: d-init

.PHONY: d-reflow-releases-recover
d-reflow-releases-recover: docker-check
	$(DOCKER_RUN_INTERACTIVE) \
		$(DOCKER_WORKSPACE) \
		$(DOCKER_IMAGE_PROD) \
		$(DOCKER_REFLOW_GLOBAL_ARGS) \
		releases recover \
		$(DOCKER_REFLOW_RELEASES_RECOVER_ARGS) \
		$(DOCKER_REFLOW_EXTRA_ARGS)

.PHONY: d-reflow-releases-recover-dryrun
d-reflow-releases-recover-dryrun: override DOCKER_REFLOW_GLOBAL_ARGS += --dry-run
d-reflow-releases-recover-dryrun: d-reflow-releases-recover

.PHONY: d-reflow-tags-replay d-reflow-tags-replay-dryrun
d-reflow-tags-replay:
	@echo WARNING: d-reflow-tags-replay is deprecated - use d-reflow-releases-recover.
	@$(MAKE) --no-print-directory d-reflow-releases-recover \
		DOCKER_REFLOW_GLOBAL_ARGS="$(DOCKER_REFLOW_GLOBAL_ARGS)" \
		DOCKER_REFLOW_RELEASES_RECOVER_ARGS="$(DOCKER_REFLOW_RELEASES_RECOVER_ARGS)" \
		DOCKER_REFLOW_EXTRA_ARGS="$(DOCKER_REFLOW_EXTRA_ARGS)"

d-reflow-tags-replay-dryrun:
	@echo WARNING: d-reflow-tags-replay-dryrun is deprecated - use d-reflow-releases-recover-dryrun.
	@$(MAKE) --no-print-directory d-reflow-releases-recover-dryrun \
		DOCKER_REFLOW_GLOBAL_ARGS="$(DOCKER_REFLOW_GLOBAL_ARGS)" \
		DOCKER_REFLOW_RELEASES_RECOVER_ARGS="$(DOCKER_REFLOW_RELEASES_RECOVER_ARGS)" \
		DOCKER_REFLOW_EXTRA_ARGS="$(DOCKER_REFLOW_EXTRA_ARGS)"

.PHONY: d-reflow-tags-convert-local
d-reflow-tags-convert-local: docker-check
	$(DOCKER_RUN_INTERACTIVE) \
		$(DOCKER_WORKSPACE) \
		$(DOCKER_IMAGE_PROD) \
		$(DOCKER_REFLOW_GLOBAL_ARGS) \
		tags convert local \
		$(DOCKER_REFLOW_TAGS_CONVERT_ARGS) \
		$(DOCKER_REFLOW_EXTRA_ARGS)

.PHONY: d-reflow-tags-convert-local-dryrun
d-reflow-tags-convert-local-dryrun: override DOCKER_REFLOW_GLOBAL_ARGS += --dry-run
d-reflow-tags-convert-local-dryrun: d-reflow-tags-convert-local

.PHONY: d-reflow-tags-convert-remote
d-reflow-tags-convert-remote: docker-check
	$(DOCKER_RUN_INTERACTIVE) \
		$(DOCKER_WORKSPACE) \
		$(DOCKER_IMAGE_PROD) \
		$(DOCKER_REFLOW_GLOBAL_ARGS) \
		tags convert remote \
		$(DOCKER_REFLOW_TAGS_CONVERT_ARGS) \
		$(DOCKER_REFLOW_EXTRA_ARGS)

.PHONY: d-reflow-tags-convert-remote-dryrun
d-reflow-tags-convert-remote-dryrun: override DOCKER_REFLOW_GLOBAL_ARGS += --dry-run
d-reflow-tags-convert-remote-dryrun: d-reflow-tags-convert-remote

.PHONY: d-reflow-tags-convert d-reflow-tags-convert-dryrun
d-reflow-tags-convert: d-reflow-tags-convert-local
d-reflow-tags-convert-dryrun: d-reflow-tags-convert-local-dryrun

.PHONY: d-reflow-dockerize
d-reflow-dockerize: docker-check
	$(DOCKER_RUN_INTERACTIVE) \
		$(DOCKER_WORKSPACE) \
		$(DOCKER_SOCKET_MOUNT) \
		$(DOCKER_IMAGE_PROD) \
		$(DOCKER_REFLOW_GLOBAL_ARGS) \
		dockerize \
		$(DOCKER_REFLOW_DOCKERIZE_ARGS) \
		$(DOCKER_REFLOW_EXTRA_ARGS)

.PHONY: d-reflow-dockerize-dryrun
d-reflow-dockerize-dryrun: override DOCKER_REFLOW_GLOBAL_ARGS += --dry-run
d-reflow-dockerize-dryrun: d-reflow-dockerize
