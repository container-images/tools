.PHONY: build run default

IMAGE_NAME := modularitycontainers/tools

default: run

build:
	docker build --tag=$(IMAGE_NAME) .

run:
	atomic run $(IMAGE_NAME)
