#!/bin/sh

OPT=$1
sc examples/twofile/counter.v examples/twofile/top.v \
   -target "freepdk45" \
   -constraint "examples/twofile/constraint.sdc" \
   -asic_diesize "0 0 100.13 100.8" \
   -asic_coresize "10.07 11.2 90.25 91" \
   -loglevel "INFO" \
   -quiet \
   -relax \
   -stop "syn" \
   -design top
