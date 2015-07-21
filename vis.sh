#!/bin/bash

gource --output-custom-log log1.txt ${PWD}
gource log1.txt
rm -rf log1.txt
