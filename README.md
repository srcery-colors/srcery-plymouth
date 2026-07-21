<p align="center">
  <img src="https://raw.githubusercontent.com/srcery-colors/srcery-assets/master/src/logo_border.svg">
</p>

<p align="center">
  <a href="https://srcery.sh">
    <img src="https://img.shields.io/static/v1?label=&message=Website&style=flat&color=5B5B5B&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAA7MAAAOzAGxoQZ+AAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAdJJREFUOI1jDAgIYMAFTp8+EcrIyMRqYmK2DJcaJlwS548fV2RjYJnNxsg87fzx44okGbBhwwaWvyyMSzM4dfgrlGz5/7IwLt2wYQML0QZIS0s2mLFIWIZxqDKkyJowuAirWkpLSzYQZcDZsyfthJnYK2p4TBkYGRgYGBkYGXo0PBjE2XgqT58+7oTXgHPnzgky/GNYXMFlwizEyAEXF2bjYujX9GJiYmBedPr0aWGcBvz793teOIeanBWrJIZT7YQUGFJkTaQZGf4v3LBhAyOGAWdPn8hUZxYIyODUweZVBgYGBoYqZXsGQz5Jb1lpiQycYUAqgBtgbGox/ebfDxtmfL+CU3Hb3YMM5z893/r46YsZWF3AxMSatPLHrUfHfj/H0Hzo3QOGOY/PPP3PwBgfEBDwH6sBRkZG7xmYGGI7vp35++7/D7j421/fGAqvb/v3j+FvnKmp6VusXoB7xdj80Nt/Pztavpxm+M/AwPCf4T9DyY0dDC9/fWk3NbXchzMMkMHTp88bTv15cXzVj9sMcx6fYdjz9vbxp0+fN2BTy4grN54/flyRiYX1PCMTI8PfX78MDS0t72NThzMaDS0t7//5/y/z99+/mbg0MzAwMAAAVbWgDHTwVjUAAAAASUVORK5CYII=">
  </a>
  <a href="https://discord.gg/G6vBMmZ">
    <img src="https://img.shields.io/discord/714101903377694741?color=%232C78BF&label=Discord&logo=discord">
  </a>
  <a href="https://www.npmjs.com/package/@srcery-colors/srcery-palette">
    <img src="https://img.shields.io/npm/v/@srcery-colors/srcery-palette?color=%23FBB829&label=Palette%20version&logo=npm">
  </a>
</p>

<h2 align="center">Plymouth</h2>

<p align="center">
Theme for <a href="https://en.wikipedia.org/wiki/Plymouth_(software)">Plymouth</a>.
</p>





## Requirements

- Plymouth
- [plymouth-plugin-script](https://packages.fedoraproject.org/pkgs/plymouth/plymouth-plugin-script/)

## Installation

Via COPR (Fedora/RHEL/CentOS and derivatives):

```bash
sudo dnf copr enable mindtooth/srcery
sudo dnf install plymouth-theme-srcery
```

Installing the package does **not** switch your boot splash automatically —
see [What the scriptlets do](#what-the-scriptlets-do) for why. To activate it:

```bash
sudo plymouth-set-default-theme -R srcery
```

`-R` rebuilds the initramfs, which is required for the new theme to actually
appear on the next boot.

## What the scriptlets do

This package intentionally has **no `%post` scriptlet** — installing it never
changes your active theme, matching how Fedora's own bundled Plymouth themes
behave (`plymouth-theme-solar`, `plymouth-theme-spinfinity`, etc. don't
self-activate either).

Its `%postun` scriptlet runs only on a genuine uninstall (RPM's `$1 == 0`
case, never on upgrade), and only touches your configuration if `srcery` is
still the *currently active* theme — in that case it clears the `Theme=`
line from `plymouthd.conf` (`plymouth-set-default-theme --reset`) so you
aren't left pointing at a theme whose files no longer exist. It never
rebuilds your initramfs on removal.

## Standalone vs. paired with the GRUB theme

This Plymouth theme works on its own. It's also designed to pair with the
sibling [srcery GRUB2 theme](https://github.com/srcery-colors) so the
boot sequence reads as one continuous animation: GRUB draws the same eye
glyph near the left edge of the boot menu, and this Plymouth theme spawns
the glyph at that same relative position before easing it to center. If you
only install this package, you still get the full boot splash — you just
won't get the GRUB-to-Plymouth handoff animation (Plymouth already detects
this: it skips the slide-in for the `shutdown`/`reboot` modes, since there's
no preceding GRUB screen then either).

## Tunables

- `EYE_START_X_FRAC` / `EYE_START_Y_FRAC` (top of `srcery/srcery.script`):
  the fractional screen position the glyph starts its intro animation from.
  These must match the image block's position in the GRUB theme's
  `theme.txt` for the slide-in to look continuous — if you move one, move
  the other.

## Screenshots

_TODO: add screenshots once available._
