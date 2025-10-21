#!/usr/bin/env bash

cd "$(dirname "$0")"

kernel="${1:-$(uname -r)}"
FEDORA_VERSION="$(. /etc/os-release; echo "${VERSION_ID?}")"

echo "1) Building container image ..."
podman build --build-arg kernel="$kernel" --build-arg FEDORA_VERSION="$FEDORA_VERSION" -t "tuxedo-drivers-builder:${kernel}" -f Dockerfile.build ..

echo "2) Building kmod"

podman run \
  --security-opt label=disable \
  -v /etc/pki:/etc/pki:ro \
  -v "$HOME/rpmbuild:/root/rpmbuild" \
  "tuxedo-drivers-builder:${kernel}" \
  "${kernel}" \
  | sed -e "s/^\\/root/${HOME//\//\\\/}/g"
