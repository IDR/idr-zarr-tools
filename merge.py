#!/usr/bin/env python
import os
import glob
import json
import argparse


def update_zattrs(zarr_dir, rendering_json=None, dry_run=False):
    rv = dict()
    if os.path.exists(f"{zarr_dir}/.zattrs"):
        with open(f"{zarr_dir}/.zattrs") as o:
            rv.update(json.load(o))
    else:
        multiscale = {"datasets":[],"version":"0.1"}
        for path in sorted(glob.glob(f"{zarr_dir}/[0-9]*")):
            path = path.split("/")[-1]
            multiscale["datasets"].append({"path": path})
        rv["multiscales"] = [multiscale]

    if not rendering_json:
        with open(f"{zarr_dir}/omero.json", "r") as o:
            rendering_json = json.load(o)

    rv["omero"] = {}
    if "version" not in omero:
        omero["version" ] = "0.1"
    for x in ("version", "channels", "rdefs"):
        rv["omero"][x] = omero[x]

    rv["omero"]["id"] = omero["id"]
    rv["omero"]["name"] = omero["meta"]["imageName"]
    for ch in rv["omero"]["channels"]:
        for x in ("reverseIntensity", "emissionWave"):
            ch.pop(x, None)
    rv["omero"]["rdefs"].pop("invertAxis", None)
    rv["omero"]["rdefs"].pop("projection", None)

    if args.dry_run:
        print(f"Updating {zarr_dir}/.zattrs")
    with open(f"{zarr_dir}/.zattrs", "w") as o:
        o.write(json.dumps(rv, indent=4, sort_keys=True))


def get_zarr_directories(top_dirs, recursive):
    if not recursive:
       return top_dirs

    if len(top_dirs) > 1:
        raise Exception("Recursive option can only be used with one directory")

    paths = []
    for root, dirs, files in os.walk(top_dirs[0]):
        for f in files:
            if f.lower() == '.zattrs':
                paths.append(root)
    return(paths)


def get_rendering_json(json_file):
    if json_file:
        with open(f"{json_file}", "r") as o:
            return json.load(o)
    else:
        return None


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("dir", nargs="+", help="the Zarr directory")
    p.add_argument('--file',
                   help="a JSON file containing the rendering settings")
    p.add_argument("--dry-run", "-n", action='store_true',
                   help="dry-run")
    p.add_argument("--recursive", "-r", action='store_true',
                   help="apply recursively to all Zarr sub-directories")
    args = p.parse_args()

    zarr_dirs = get_zarr_directories(args.dir, args.recursive)
    rendering_json = get_rendering_json(args.file)
    for zarr_dir in zarr_dirs:
        update_zattrs(zarr_dir, rendering_json=rendering_json, dry_run=False)
