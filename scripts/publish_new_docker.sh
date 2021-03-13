#!/usr/bin/env bash

cat .ghcr-access-token | docker login https://docker.pkg.github.com -u sandrochuber --password-stdin
TAG=docker.pkg.github.com/sandrochuber/pylic/pylic:latest
docker build -t ${TAG} .
docker push ${TAG}
