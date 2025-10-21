# tuxedo-yt6801-kmod

This configuration builds the driver for the Motorcomm YT6801 Gigabit Ethernet Controller provided by tuxedo as kmod, which is compatible with ostree based atomic distributions.
It has been successfully tested on Fedora Kinoite with secure boot enabled.


## Installation

### With distrobox

```bash
### Skip the first two commands if you have setup akmods already, don't need secure boot support or want to generate the keys inside of distrobox ###
sudo rpm-ostree install akmods rpmdevtools
sudo kmodgenca

# Create a distrobox with all requirements. We use --root because we need to access the host akmods signing key. Skip, if you don't require secure boot support
distrobox create --image fedora:42 --name kmod-builder --root \
  --volume /etc/pki/akmods:/etc/pki/akmods-host:ro \
  --additional-packages "kernel-devel rpmrebuild spectool kmodtool git rpmdevtools akmods nvim tree" \
  --init-hooks 'dnf -y group install c-development development-tools && mkdir -p "/lib/modules/$(uname -r)" && ln -s "/usr/src/kernels/$(uname -r)" "/lib/modules/$(uname -r)/build && rm -r /etc/pki/akmods && mv /etc/pki/akmods-host /etc/pki/akmods"'
distrobox enter --root kmod-builder

# Setup repository
git clone https://github.com/theCalcaholic/tuxedo-yt6801-kmod
cd tuxedo-yt6801-kmod

# Build kmod
./build.sh

# The rpm is saved at $HOME/rpmbuild/RPMs/<your-architecture>/kmod-tuxedo-yt6801-*
# For some reason I don't understand yet, there's a bogus dependency to "kmod-tuxedo-yt6801-common", which doesn't exist. A workaround is to rebuild the rpm pacakge without it:
rpmrebuild --edit-spec --package "$HOME/rpmbuild/RPMs/<your-architecture>/kmod-tuxedo-yt6801-"*.rpm # Then remove the line that says `Requires: kmod-tuxedo-yt6801-common`, save and confirm.

# Exit distrobox
exit

# Install the driver
sudo rpm-ostree install "$HOME/rpmbuild/RPMs/<your-architecture>/kmod-tuxedo-yt6801-"*.rpm

# Finally, reboot
systemctl reboot
```

### With podman

```bash
### Skip the first two commands if you have setup akmods already, don't need secure boot support or want to generate the keys inside of distrobox ###
sudo rpm-ostree install akmods rpmdevtools
sudo kmodgenca

# Setup repository
git clone https://github.com/theCalcaholic/tuxedo-yt6801-kmod
cd tuxedo-yt6801-kmod

# Build kmod in podman
./tools/build_in_container.sh

# The rpm is saved at $HOME/rpmbuild/RPMs/<your-architecture>/kmod-tuxedo-yt6801-*
# For some reason I don't understand yet, there's a bogus dependency to "kmod-tuxedo-yt6801-common", which doesn't exist. A workaround is to rebuild the rpm pacakge without it:
rpmrebuild --edit-spec --package "$HOME/rpmbuild/RPMs/<your-architecture>/kmod-tuxedo-yt6801-"*.rpm # Then remove the line that says `Requires: kmod-tuxedo-yt6801-common`, save and confirm.

# Install the driver
sudo rpm-ostree install "$HOME/rpmbuild/RPMs/<your-architecture>/kmod-tuxedo-yt6801-"*.rpm

# Finally, reboot
systemctl reboot
```

## Credits

I wouldn't have been able to make this work without the examples given in [https://github.com/gladion136/tuxedo-drivers-kmod/](https://github.com/gladion136/tuxedo-drivers-kmod/), so thank you @gladion136. :)
