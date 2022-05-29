#!/usr/bin/env bash
set -eu
build_path="$(dirname $0)/openjdk"
docker build --tag openjdk-languages --file "${build_path}/Dockerfile" "${build_path}"
docker run --volume $HOME:/home/me --workdir /home/me/src/mysite --rm --interactive --tty --name openjdk openjdk-languages bash -i
#docker run --volume $HOME:/home/me --workdir /home/me/src/mysite --rm --interactive --tty --name openjdk openjdk:jdk-bullseye bash -i
