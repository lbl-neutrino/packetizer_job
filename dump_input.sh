#!/usr/bin/env bash

basedir="/global/cfs/cdirs/dune/www/data/Module2"
subdir="packetized"

# https://stackoverflow.com/questions/4210042/how-do-i-exclude-a-directory-when-using-find
find "$basedir"                        `# in $basedir` \
    -path "$basedir/$subdir" -prune -o `# but not in $basedir/$subdir` \
    -name '*selftrig*.h5'              `# with a self-triggerish name` \
    -mmin +60 -print                   `# at least an hour since last modified` \
