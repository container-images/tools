.PHONY: build run default enumerate-tools upstream fedora-downstream source

DISTRO := fedora-26-x86_64
VARIANT := upstream
DG_BINARY ?= dg
DG_EXEC = $(DG_BINARY) --max-passes 25 --spec specs/common.yml --multispec specs/multispec.yaml --distro $(DISTRO).yaml --multispec-selector variant=$(VARIANT)

REPOSITORY = $(shell ${DG_EXEC} --template={{spec.repository}})

SOURCE_HELP_MD := ./help/help.md
# Fedora policy is to name the file README.md in the container image
RENDERED_HELP_MD := ./root/README.md
SOURCE_README_MD := ./README.md.template
RENDERED_README_MD := ./README.md
SOURCE_DOCKERFILE_MD := ./Dockerfile.template
RENDERED_DOCKERFILE_MD := ./Dockerfile

default: run

$(RENDERED_DOCKERFILE_MD): $(SOURCE_DOCKERFILE_MD)
	$(DG_EXEC) --template $(SOURCE_DOCKERFILE_MD) --output $(RENDERED_DOCKERFILE_MD)

$(RENDERED_README_MD): $(SOURCE_README_MD)
	$(DG_EXEC) --template $(SOURCE_README_MD) --output $(RENDERED_README_MD)

$(RENDERED_HELP_MD): $(SOURCE_HELP_MD)
	@# FIXME: current go-md2man can't convert tables :<
	@# go-md2man -in=${SOURCE_HELP_MD} -out=./root/help.1
	$(shell TOOLS_CONTAINER_SKIP_ENUMERATION=false $(DG_EXEC) --template $(SOURCE_HELP_MD) --output $(RENDERED_HELP_MD))

source: $(RENDERED_HELP_MD) $(RENDERED_README_MD) $(RENDERED_DOCKERFILE_MD)

fedora-downstream:
	make -e source VARIANT="fedora-downstream"

upstream:
	make -e source VARIANT="upstream"

build: source
	docker build --tag=$(REPOSITORY) .

run:
	atomic run --update $(REPOSITORY)

enumerate-tools:
	docker run -it -v ${PWD}:/src -e TOOLS_PACKAGES=$(shell $(DG_EXEC) --template="{{spec.packages|join(\",\")}}") --rm $(REPOSITORY) /src/enumerate-tools.py

clean:
	rm Dockerfile || :
	rm root/README.md || :
	rm README.md || :
