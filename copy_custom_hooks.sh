#!/bin/bash
#
# * Copies custom_hooks directory to target repo path
# * $GITREPO path is defined in .bash_profile
#
# Caution: one item per one line for clarity
declare -a target_path_list=(
 "CloudLabTest/project-3.git"
 "ExampleGroup/web.git"
 "ExampleGroup/prj_original_root.git"
 "ExampleGroup/prj-new.git"
 "ExampleGroup/prj3.git"
 "ExampleGroup/prj-web.git"
)

for path in "${target_path_list[@]}"; do
  echo "Copying to: $path"
  cp -arf /root/custom_hooks/ $GITREPO/"$path"/
done
