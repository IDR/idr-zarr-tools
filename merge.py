#!/usr/bin/env python
import os
import sys
import glob
import json
import argparse
p = argparse.ArgumentParser()
p.add_argument("dir")
a = p.parse_args()
rv = dict()

if os.path.exists(f"{a.dir}/.zattrs"):
    with open(f"{a.dir}/.zattrs") as o:
        rv.update(json.load(o))
else:
    multiscale = {"datasets":[],"version":"0.1"}
    for path in sorted(glob.glob(f"{a.dir}/[0-9]*")):
        path = path.split("/")[-1]
        multiscale["datasets"].append({"path": path})
    rv["multiscales"] = [multiscale]

with open(f"{a.dir}/omero.json", "r") as o:
    omero = json.load(o)

#print(list(omero.keys()))
rv["omero"] = {}
for x in ("version", "channels", "rdefs"):
    rv["omero"][x] = omero[x]

rv["omero"]["id"] = omero["id"]
rv["omero"]["name"] = omero["meta"]["imageName"]
for ch in rv["omero"]["channels"]:
    for x in ("reverseIntensity", "emissionWave"):
        ch.pop(x, None)
rv["omero"]["rdefs"].pop("invertAxis", None)
rv["omero"]["rdefs"].pop("projection", None)

with open(f"{a.dir}/.zattrs", "w") as o:
    o.write(json.dumps(rv, indent=4, sort_keys=True))
