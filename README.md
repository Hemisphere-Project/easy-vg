[header-image]: https://raw.githubusercontent.com/mk-fg/easy-vg/develop/.github/assets/raspi-spiral.png
[git-repository-url]: https://github.com/mk-fg/openvg
[license-shield-url]: https://img.shields.io/github/license/mk-fg/easy-vg.svg?style=flat-square
[license-url]: https://github.com/mk-fg/easy-vg/blob/master/LICENSE

# EasyVG [mk-fg fork]

[![One][header-image]][git-repository-url]
[![LICENSE][license-shield-url]][license-url]

EasyVG provides an abstraction layer on top of native
[OpenVG graphics API](https://www.khronos.org/files/openvg-quick-reference-card.pdf),
for easy creation of OpenVG contexts and drawing shapes, images, and text,
without requiring anything other than the most minimal system setup.

EasyVG follows standard C and EGL API naming conventions.

EasyVG is fully compatible with Raspberry Pi boards.

This mk-fg/easy-vg repository is a fork of (in a recent-first order):

- [EasyVG by George Thomas <mgthomas99>](https://github.com/mgthomas99/easy-vg)
- [OpenVG by Anthony Starks <ajstarks>](https://github.com/ajstarks/openvg)

Difference from upstream EasyVG (mgthomas99/easy-vg):

- Has API frozen at a state of ~2018-08-01 master branch, with simple "draw
  things via single call" API, same as ajstarks/openvg has, before introducing paths
  (which are still in mgthomas99/easy-vg#develop branch at the time of writing).

- Intended to be built and used as a shared libshapes.so library,
  including from python via ctypes wrapper.

- Updated with fixes and minor additional API features where necessary,
  without changing its current methods and logic if possible.

### Text & Fonts

EasyVG is capable of rendering text.

One default font (DejaVuSans.ttf) is converted and built-into libshapes.so via Makefile.

To use custom TrueType fonts, developers should convert the font into C code use
the font2openvg binary (use `make lib/font2openvg` or just `make` to build it),
and then include and init it using `loadfont()` in C API.

Loading custom fonts at runtime (incl. via python wrapper) is not supported.

#### Using font2openvg

The [font2openvg](https://github.com/mgthomas99/font2openvg) repository contains
more information on font2openvg tool included in this repo.

Once the lib/font2openvg is built, compile a TrueType font file.

For the below demonstrations, it will be assumed that you are using a source
font file named `DejaVuSans.ttf` and a compiled output named `DejaVuSans.inc`.

Once a font is compiled, it can be included in your code like this:

```c
    #include "DejaVuSans.inc"
    Fontinfo DejaFont

    loadfont(DejaVuSans_glyphPoints,
            DejaVuSans_glyphPointIndices,
            DejaVuSans_glyphInstructions,
            DejaVuSans_glyphInstructionIndices,
            DejaVuSans_glyphInstructionCounts,
            DejaVuSans_glyphAdvances,
            DejaVuSans_characterMap,
            DejaVuSans_glyphCount);

    // Unload the font when done
    unloadfont(DejaFont.Glyphs, DejaFont.Count);
```



## Build and Run Examples

*Note that you will need at least 64 MB of GPU RAM*
(when using a single DispmanX layer, 128+ for more)

For building libshapes.so and/or including the code, requirements are:
- DejaVu fonts, jpeg and freetype libraries with headers.
- For building and easy packaging on raspbian/debian: build-essentials checkinstall

```shell
# apt install libfreetype6-dev libjpeg8-dev ttf-dejavu-core
# apt install build-essentials checkinstall
```

Runtime requirements for libshapes.so and python wrapper:
- libbrcmEGL / libbrcmGLESv2 - RPi's VC4 GL libs.
- libjpeg - for createImageFromJpeg, can be omitted when including code from C.
- python3 - when/if using python wrapper.

```shell
# apt install libjpeg8 python3
```

Basic build process:

```shell
% curl https://github.com/mk-fg/easy-vg/archive/master.tar.gz | tar -xz
% cd easy-vg-master
% make
```

Build and run C example(s):

```shell
% pushd example
% make hello
% ./hello
% popd
```

Package/install on raspbian/debian (including libshapes.so and python module):

```shell
% sudo checkinstall -Dy --pkgname=easy-vg --pkgversion=1 --backup=no -- make install-checkinstall
% dpkg -L easy-vg
% dpkg-deb -I easy-vg_1-1_armhf.deb
```

Install / uninstall to current rootfs (not recommended outside of packaging scripts and such):

```shell
% make install
% make install-python
% make uninstall
```

Run python example:

```shell
% python3 python/hello.py
```

Build self-contained C binary (e.g. example.c, see also example/hello.c) based
on the library code:

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <jpeglib.h>
#include "VG/openvg.h"
#include "VG/vgu.h"
#include "./src/fontinfo.h"
#include "./src/libshapes.h"

// Load image from specified jpg file and display it stretched to full screen.

int main(int argc, char *argv[]) {
  int w, h;
  evgInit(&w, &h, -1);
  evgBegin();
  evgImage(0, 0, w, h, argv[1]);
  evgEnd();
  while (1) sleep(3600);
  evgFinish();
  return 0;
}
```

```shell
% gcc -Wall \
  -I/opt/vc/include -I/opt/vc/include/interface/vmcs_host/linux -I/opt/vc/include/interface/vcos/pthreads \
  -I. ./example.c -o ./example \
  ./build/libshapes.o ./build/oglinit.o -L/opt/vc/lib -lbrcmEGL -lbrcmGLESv2 -lbcm_host -lpthread -ljpeg
% curl -OL https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg
% ./example Example.jpg
```

Build C binary linked against installed libshapes.so:

```c
#include <shapes.h>
#include <fontinfo.h>

// ... code using libshapes.so
```

```shell
% gcc -Wall \
  -I/opt/vc/include -I/opt/vc/include/interface/vmcs_host/linux -I/opt/vc/include/interface/vcos/pthreads \
  example.c -o example -lshapes
% ./example
```

Have fun!



## License

See the `LICENSE` file for license information.
