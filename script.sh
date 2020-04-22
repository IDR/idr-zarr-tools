#!/usr/bin/env bash


EXE=/opt/bioformats2raw/bin/bioformats2raw

set -e
set -u
set -x

INPUT=$1; shift
OUTPUT=$1; shift

echo "Converting $INPUT to /out/$OUTPUT..."
time $EXE $INPUT /out/$OUTPUT --file_type=zarr --dimension-order=XYZCT
ls /out/$OUTPUT
