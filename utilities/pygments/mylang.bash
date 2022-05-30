#!/usr/bin/env bash

declare -r target="${1:-optional-arguments}"

pygmentize -x -l utilities/pygments/mylang.py:MylangLexer -f html -Ofull,debug_token_types listings/cl-existence-oriented/${target}.mylang >${target}.html
