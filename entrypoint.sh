#!/bin/sh

set -eu

if test "$#" = 0; then
	exec chatio
elif test "$1" = "--"; then
	shift
	exec chatio "$@"
else
	exec "$@"
fi
