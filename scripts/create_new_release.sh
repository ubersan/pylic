#!/usr/bin/env bash

VERSION=$1
git tag ${VERSION}
gh release create --notes "" ${VERSION}
