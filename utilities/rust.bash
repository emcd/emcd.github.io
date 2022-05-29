#!/usr/bin/env bash
docker run --volume $HOME:/home/me --workdir /home/me/src/mysite --rm --interactive --tty --name rust rust
