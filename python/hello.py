#!/usr/bin/env python3

# Straightforward translation of hello.c example to python

from evg import LibShapes

evg = LibShapes()

w, h = evg.c_int(), evg.c_int()
evg.init(w, h)
evg.begin()

evg.background(0, 0, 0)

evg.fill(44, 77, 232, 1)
evg.circle(w.value / 2, 0, w.value)

evg.fill(255, 255, 255, 1)
evg.text_mid(
	w.value / 2, h.value * 0.7,
	b'hello world', None, w.value / 15 )

evg.end()

input()
evg.finish()
