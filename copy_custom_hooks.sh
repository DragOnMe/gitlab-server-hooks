#!/bin/bash
#
# * Copies custom_hooks directory to target repo path
# * $GITREPO path is defined in .bash_profile
#
# Caution: one item per one line for clarity
declare -a target_path_list=(
 "CloudLabTest/project-3.git"
 "CloudMesh/web.git"
 "CloudMesh/cloudmesh_original_root.git"
 "CloudMesh/ngf.git"
 "CloudMesh/public-cloud-adapter.git"
 "CloudMesh/public-cloud-web.git"
)

for path in "${target_path_list[@]}"; do
  echo "Copying to: $path"
  cp -arf /root/custom_hooks/ $GITREPO/"$path"/
done