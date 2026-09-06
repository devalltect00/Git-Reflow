# Reflow commands executed from the project virtual environment.

LOCAL_INIT_COMMANDS_LIST := \
	l-init l-init-dryrun l-init-force l-init-ask l-init-all l-init-config

LOCAL_REFLOW_COMMANDS_LIST := \
	l-reflow-releases-recover l-reflow-releases-recover-dryrun \
	l-reflow-tags-replay l-reflow-tags-replay-dryrun \
	l-reflow-tags-convert l-reflow-tags-convert-dryrun \
	l-reflow-tags-convert-local l-reflow-tags-convert-local-dryrun \
	l-reflow-tags-convert-remote l-reflow-tags-convert-remote-dryrun \
	l-reflow-dockerize l-reflow-dockerize-dryrun

$(foreach cmd,$(LOCAL_INIT_COMMANDS_LIST),$(eval $(call REGISTER_COMMAND,LOCAL_INIT,$(cmd),LOCAL)))
$(foreach cmd,$(LOCAL_REFLOW_COMMANDS_LIST),$(eval $(call REGISTER_COMMAND,LOCAL_REFLOW,$(cmd),LOCAL)))

.PHONY: l-init
l-init: check-venv
	$(LOCAL_RUN) \
		$(LOCAL_REFLOW_GLOBAL_ARGS) \
		init \
		$(LOCAL_REFLOW_INIT_ARGS) \
		$(LOCAL_REFLOW_EXTRA_ARGS)

.PHONY: l-init-dryrun l-init-force l-init-ask l-init-all l-init-config
l-init-dryrun: override LOCAL_REFLOW_GLOBAL_ARGS += --dry-run
l-init-dryrun: l-init

l-init-force: override LOCAL_REFLOW_INIT_ARGS += --force
l-init-force: l-init

l-init-ask: override LOCAL_REFLOW_INIT_ARGS += --ask
l-init-ask: l-init

l-init-all: override LOCAL_REFLOW_INIT_ARGS += --mode all
l-init-all: l-init

l-init-config: override LOCAL_REFLOW_INIT_ARGS += --mode config
l-init-config: l-init

.PHONY: l-reflow-releases-recover
l-reflow-releases-recover: check-venv
	$(LOCAL_RUN) \
		$(LOCAL_REFLOW_GLOBAL_ARGS) \
		releases recover \
		$(LOCAL_REFLOW_RELEASES_RECOVER_ARGS) \
		$(LOCAL_REFLOW_EXTRA_ARGS)

.PHONY: l-reflow-releases-recover-dryrun
l-reflow-releases-recover-dryrun: override LOCAL_REFLOW_GLOBAL_ARGS += --dry-run
l-reflow-releases-recover-dryrun: l-reflow-releases-recover

.PHONY: l-reflow-tags-replay l-reflow-tags-replay-dryrun
l-reflow-tags-replay:
	@echo WARNING: l-reflow-tags-replay is deprecated - use l-reflow-releases-recover.
	@$(MAKE) --no-print-directory l-reflow-releases-recover \
		LOCAL_REFLOW_GLOBAL_ARGS="$(LOCAL_REFLOW_GLOBAL_ARGS)" \
		LOCAL_REFLOW_RELEASES_RECOVER_ARGS="$(LOCAL_REFLOW_RELEASES_RECOVER_ARGS)" \
		LOCAL_REFLOW_EXTRA_ARGS="$(LOCAL_REFLOW_EXTRA_ARGS)"

l-reflow-tags-replay-dryrun:
	@echo WARNING: l-reflow-tags-replay-dryrun is deprecated - use l-reflow-releases-recover-dryrun.
	@$(MAKE) --no-print-directory l-reflow-releases-recover-dryrun \
		LOCAL_REFLOW_GLOBAL_ARGS="$(LOCAL_REFLOW_GLOBAL_ARGS)" \
		LOCAL_REFLOW_RELEASES_RECOVER_ARGS="$(LOCAL_REFLOW_RELEASES_RECOVER_ARGS)" \
		LOCAL_REFLOW_EXTRA_ARGS="$(LOCAL_REFLOW_EXTRA_ARGS)"

.PHONY: l-reflow-tags-convert-local
l-reflow-tags-convert-local: check-venv
	$(LOCAL_RUN) \
		$(LOCAL_REFLOW_GLOBAL_ARGS) \
		tags convert local \
		$(LOCAL_REFLOW_TAGS_CONVERT_ARGS) \
		$(LOCAL_REFLOW_EXTRA_ARGS)

.PHONY: l-reflow-tags-convert-local-dryrun
l-reflow-tags-convert-local-dryrun: override LOCAL_REFLOW_GLOBAL_ARGS += --dry-run
l-reflow-tags-convert-local-dryrun: l-reflow-tags-convert-local

.PHONY: l-reflow-tags-convert-remote
l-reflow-tags-convert-remote: check-venv
	$(LOCAL_RUN) \
		$(LOCAL_REFLOW_GLOBAL_ARGS) \
		tags convert remote \
		$(LOCAL_REFLOW_TAGS_CONVERT_ARGS) \
		$(LOCAL_REFLOW_EXTRA_ARGS)

.PHONY: l-reflow-tags-convert-remote-dryrun
l-reflow-tags-convert-remote-dryrun: override LOCAL_REFLOW_GLOBAL_ARGS += --dry-run
l-reflow-tags-convert-remote-dryrun: l-reflow-tags-convert-remote

# Compatibility aliases default to the non-remote local scope.
.PHONY: l-reflow-tags-convert l-reflow-tags-convert-dryrun
l-reflow-tags-convert: l-reflow-tags-convert-local
l-reflow-tags-convert-dryrun: l-reflow-tags-convert-local-dryrun

.PHONY: l-reflow-dockerize
l-reflow-dockerize: check-venv
	$(LOCAL_RUN) \
		$(LOCAL_REFLOW_GLOBAL_ARGS) \
		dockerize \
		$(LOCAL_REFLOW_DOCKERIZE_ARGS) \
		$(LOCAL_REFLOW_EXTRA_ARGS)

.PHONY: l-reflow-dockerize-dryrun
l-reflow-dockerize-dryrun: override LOCAL_REFLOW_GLOBAL_ARGS += --dry-run
l-reflow-dockerize-dryrun: l-reflow-dockerize
