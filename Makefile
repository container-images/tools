.PHONY: build run default enumerate-tools upstream fedora-downstream source test check

DISTRO := fedora-27-x86_64
VARIANT := upstream
DG_BINARY ?= dg
DG_EXEC = $(DG_BINARY) --max-passes 25 --spec specs/common.yml --multispec specs/multispec.yaml --distro $(DISTRO).yaml --multispec-selector variant=$(VARIANT)
# set to 1 to enable debugging
DEBUG_MODE ?= 0
ifeq ($(DEBUG_MODE), 1)
	ANSIBLE_EXTRA_ARGS := -vv
endif

REPOSITORY = $(shell ${DG_EXEC} --template={{spec.repository}})

SOURCE_HELP_MD := ./help/help.md
# Fedora policy is to name the file README.md in the container image
RENDERED_HELP_MD := ./root/README.md
SOURCE_README_MD := ./README.md.template
RENDERED_README_MD := ./README.md
SOURCE_DOCKERFILE_MD := ./Dockerfile.template
RENDERED_DOCKERFILE_MD := ./Dockerfile

default: run

root/:
	mkdir -p ./root

$(RENDERED_DOCKERFILE_MD): $(SOURCE_DOCKERFILE_MD) specs/*
	$(DG_EXEC) --template $(SOURCE_DOCKERFILE_MD) --output $(RENDERED_DOCKERFILE_MD)

$(RENDERED_README_MD): $(SOURCE_README_MD) specs/*
	$(DG_EXEC) --template $(SOURCE_README_MD) --output $(RENDERED_README_MD)

$(RENDERED_HELP_MD): $(SOURCE_HELP_MD) specs/*
	@# FIXME: current go-md2man can't convert tables :<
	@# go-md2man -in=${SOURCE_HELP_MD} -out=./root/help.1
	$(shell TOOLS_CONTAINER_SKIP_ENUMERATION=false $(DG_EXEC) --template $(SOURCE_HELP_MD) --output $(RENDERED_HELP_MD))

source: root/ $(RENDERED_HELP_MD) $(RENDERED_README_MD) $(RENDERED_DOCKERFILE_MD)

fedora-downstream:
	make -e source VARIANT="fedora"

upstream:
	make -e source VARIANT="upstream"

build: source
	docker build --tag=$(REPOSITORY) .

run:
	atomic run --update $(REPOSITORY)

enumerate-tools:
	docker run -it -v ${PWD}:/src -e TOOLS_PACKAGES=$(shell $(DG_EXEC) --template="{{spec.packages|join(\",\")}}") --rm $(REPOSITORY) /src/enumerate-tools.py

check: test

test: build
	make -C tests/ check-local IMAGE_NAME=$(REPOSITORY) ANSIBLE_EXTRA_ARGS=$(ANSIBLE_EXTRA_ARGS)

check-in-vm: build
	make -C tests/ check-in-vm IMAGE_NAME=$(REPOSITORY) ANSIBLE_EXTRA_ARGS=$(ANSIBLE_EXTRA_ARGS)

clean:
	rm Dockerfile || :
	rm root/README.md || :
	rm README.md || :

render-in-centos:
	docker run --rm -ti -v ${PWD}:/src -w /src centos:7 ./hooks/pre_build_centos
