#!/bin/bash

# add permissions
sudo mkdir -p /blender/4.0/{scripts/addons,python/lib/python3.10/site-packages}
sudo chmod 777 /blender/4.0/{scripts/addons,python/lib/python3.10/site-packages}

# install add-on
ln -s $(pwd)/src /blender/4.0/scripts/addons/myaddon

# add symbolic link to python
mkdir -p /config/.local/bin
ln -s /blender/4.0/python/bin/python3.10 /config/.local/bin/python

# install dev dependencies
python -m pip install fake-bpy-module-4.0