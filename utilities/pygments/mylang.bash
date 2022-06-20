#!/usr/bin/env bash
set -eu

#declare -r target="${1:-listings/cl-existence-oriented/optional-arguments}"
declare -r target="$1"

#pygmentize -x -l utilities/pygments/mylang.py:MylangLexer -f html -Ofull,debug_token_types listings/cl-existence-oriented/${target}.mylang >${target}.html
pygmentize -x -l utilities/pygments/mylang.py:MylangLexer -O style=one-dark "${target}"
