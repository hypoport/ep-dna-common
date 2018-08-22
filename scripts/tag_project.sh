#!/bin/bash

BASEDIR=$( dirname "${BASH_SOURCE[0]}" )
set -euo pipefail

if [ $# -eq 0 ]
  then
    echo "ERROR. You have to specify the tag comment like : tag_project.sh \"my comment\" "
    exit 1
fi

COMMENT=$1
VERSION="$(date +"%Y-%m-%d-%H-%M-%S")"

echo "Erstelle neue Package Version : $VERSION mit Kommentar : ${COMMENT}"
git tag -a ${VERSION} -m "${COMMENT}"
git push origin ${VERSION}