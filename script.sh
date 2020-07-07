#!/usr/bin/env bash


EXE=/opt/bioformats2raw/bin/bioformats2raw

set -e
set -u
set -x

IMAGE_OR_FILE=$1; shift
INPUT=$1; shift
OUTPUT=$1; shift

EXTRA_ARGS=
echo "Converting $INPUT to /$OUTPUT..."
if [ -e "${IMAGE_OR_FILE}" ];
then
   echo Found file: $IMAGE_OR_FILE
   # Use the first column of the CSV (%3) as the group and omit use of the series ID (%1)
   EXTRA_ARGS="--scale-format-string=%3\$s/%2\$s --additional-scale-format-string-args=${IMAGE_OR_FILE}"
fi

time $EXE "$INPUT" "/$OUTPUT" --file_type=zarr --dimension-order=XYZCT ${EXTRA_ARGS}
ls "/$OUTPUT"

if [ -e "${IMAGE_OR_FILE}" ];
then
    for IMAGE in $(cut -f1 -d, "${IMAGE_OR_FILE}");
    do
        echo Image:${IMAGE}
        mv /$OUTPUT/data.zarr/${IMAGE} /v0.1/${IMAGE}.zarr
    done
else
    # Move first (and only) of series to the image name
    mv /$OUTPUT/data.zarr/0 /v0.1/${IMAGE_OR_FILE}.zarr
fi

# Cleanup
rm /$OUTPUT/data.zarr/.zattrs
rm /$OUTPUT/data.zarr/.zgroup
rmdir /$OUTPUT/data.zarr
rm /$OUTPUT/METADATA.ome.xml
rmdir /$OUTPUT/
