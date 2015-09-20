#!/bin/bash

DIRECTORY_TO_OBSERVE="crypto_chaotic"      #// might want to change this
function block_for_change {
  inotifywait -r \
    -e modify,move,create,delete \
    $DIRECTORY_TO_OBSERVE
}
BUILD_SCRIPT=install.sh          #// might want to change this too
function build {
  bash $BUILD_SCRIPT
}
build
while block_for_change; do
  build
done
