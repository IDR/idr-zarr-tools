#!/usr/bin/env bash


EXE=/opt/bioformats2raw/bin/bioformats2raw

set -e
set -u
set -x

IMAGE=$1; shift
INPUT=$1; shift
OUTPUT=$1; shift

echo "Converting $INPUT to /$OUTPUT..."
time $EXE "$INPUT" "/$OUTPUT" --file_type=zarr --dimension-order=XYZCT
ls "/$OUTPUT"

# TBD Move first series to the image name
mv /$OUTPUT/data.zarr/0 /v0.1/${IMAGE}.zarr
rm /$OUTPUT/data.zarr/.zattrs
rm /$OUTPUT/data.zarr/.zgroup
rmdir /$OUTPUT/data.zarr
rm /$OUTPUT/METADATA.ome.xml
rmdir /$OUTPUT/
