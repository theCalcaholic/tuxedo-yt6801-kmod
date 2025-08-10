#!/bin/sh
# Build script for Tuxedo yt6801 driver
# Builds: tuxedo-yt6801-kmod (for your kernel)
set -ex

# Check if the kernels parameter is provided, if not, default to uname -r
if [ -z "$1" ]; then
  kernels=$(uname -r)
else
  kernels=$1
fi

echo "--> Copying spec files to ~/rpmbuild/SPECS/"
mkdir -p ~/rpmbuild/SPECS/
cp ./tuxedo-yt6801-kmod.spec ~/rpmbuild/SPECS/

cd ~/rpmbuild/SPECS/

echo "--> Installing dependencies"
spectool -g -R tuxedo-yt6801-kmod.spec

#rm ~/rpmbuild/RPMS/* -rf

echo "--> Building RPMs"
rpmbuild -ba tuxedo-yt6801-kmod.spec --define "kernels ${kernels}"

echo "--> Listing RPMs"
tree ~/rpmbuild/RPMS/
