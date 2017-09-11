.PHONY: build run default

IMAGE_NAME := modularitycontainers/tools
# HELP_MD := ./help/help.md

default: run

# FIXME: current go-md2man can't convert tables :<
# doc:
# 	go-md2man -in=${HELP_MD} -out=./root/help.1

build:
	docker build --tag=$(IMAGE_NAME) .

run:
	atomic run --update $(IMAGE_NAME)

enumerate-tools:
	@docker run -v ${PWD}:/src --rm $(IMAGE_NAME) /src/enumerate-tools.py
