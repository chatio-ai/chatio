#!/bin/sh

set -ex

DIR="$(dirname "$(readlink -f "$0")")"

cd "$("$VIRTUAL_ENV/bin/python" -c 'import site; print(site.getsitepackages()[0])')"
echo "$DIR/src" | tee ./chatio.pth
cd -
