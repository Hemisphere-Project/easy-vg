#!/usr/bin/env python3

# Straightforward translation of hello.c example to python

from evg import LibShapes

evg = LibShapes()

w, h = evg.c_int(), evg.c_int()
evg.init(w, h, 0)

# evg.WindowOpacity(200)

evg.begin()

evg.background_rgb(0, 0, 0, 0)

evg.fill(255, 0, 0, 1)
evg.circle(w.value/2, h.value/2, w.value/2)


# evg.fill(44, 77, 232, 1)
# evg.circle(w.value / 2, 0, w.value)

# evg.text_mid(
# 	w.value / 2, h.value * 0.7,
# 	b'hello world', None, w.value / 15 )

evg.end()

input()
evg.finish()
