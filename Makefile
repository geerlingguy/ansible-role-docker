ANSIBLE_KEY:=~/.ssh/ansible
# FIXME: This image is currently private
IMAGE:=molecule-test
SCENARIO:=docker-version
ROLE_NAME:=ansible-role-docker
WORK_DIR:=/workspace/$(ROLE_NAME)

DOCKER_VERSIONS:=18.09.1 18.09.4 18.09.5 18.09.6 19.03.1 19.03.2 19.03.3

RUN_CMD=docker run --rm \
	--env ANSIBLE_TRANSFORM_INVALID_GROUP_CHARS=ignore \
	--env HCLOUD_TOKEN=${HCLOUD_TOKEN} \
	--env MOLECULE_NO_LOG=yes \
	--env DOCKER_VERSION_CI=${DOCKER_VERSION_CI} \
	-v /tmp:/tmp \
	-v $(CURDIR):$(WORK_DIR) \
	-w $(WORK_DIR) \
	-v $(ANSIBLE_KEY):/root/.ssh/ansible $(IMAGE)

.PHONY: help
help: ## Show help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: all
all: $(DOCKER_VERSIONS) ## Run tests against all versions

$(DOCKER_VERSIONS): ## internal: version loop
	@echo version is $@
	$(MAKE) test DOCKER_VERSION_CI=$@

.PHONY: test
test: guard-HCLOUD_TOKEN guard-DOCKER_VERSION_CI ## Run molecule test
	$(RUN_CMD) molecule test --scenario-name $(SCENARIO)

guard-%: ## Check required variables
	@ if [ "${${*}}" = "" ]; then \
        echo "Environment variable $* not set"; \
        exit 1; \
    fi
