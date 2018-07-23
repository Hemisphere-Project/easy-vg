import os, sys, re, enum, ctypes as ct, functools as ft

# Docs:
#   https://www.khronos.org/files/openvg-quick-reference-card.pdf
#   https://www.khronos.org/registry/OpenVG/specs/openvg_1_0_1.pdf
#   https://www.khronos.org/openvg/

class LibShapes(object):

	_headers = '''
		VGfloat TextHeight(Fontinfo *, VGfloat)
		VGfloat TextDepth(Fontinfo *, VGfloat)
		VGfloat TextWidth(char *, Fontinfo *, VGfloat)
		RGBA(unsigned int, unsigned int, unsigned int, VGfloat, VGfloat[4])
		RGB(unsigned int, unsigned int, unsigned int, VGfloat[4])

		evgTranslate(VGfloat, VGfloat)
		evgRotate(VGfloat)
		evgShear(VGfloat, VGfloat)
		evgScale(VGfloat, VGfloat)
		evgText(VGfloat, VGfloat, char *, Fontinfo *, VGfloat)
		evgTextMid(VGfloat, VGfloat, char *, Fontinfo *, VGfloat)
		evgTextEnd(VGfloat, VGfloat, char *, Fontinfo *, VGfloat)
		evgCbezier(VGfloat, VGfloat, VGfloat, VGfloat, VGfloat, VGfloat, VGfloat, VGfloat)
		evgQbezier(VGfloat, VGfloat, VGfloat, VGfloat, VGfloat, VGfloat)
		evgPolygon(VGfloat *, VGfloat *, VGint)
		evgPolyline(VGfloat *, VGfloat *, VGint)
		evgRect(VGfloat, VGfloat, VGfloat, VGfloat)
		evgLine(VGfloat, VGfloat, VGfloat, VGfloat)
		evgRoundRect(VGfloat, VGfloat, VGfloat, VGfloat, VGfloat, VGfloat)
		evgEllipse(VGfloat, VGfloat, VGfloat, VGfloat)
		evgCircle(VGfloat, VGfloat, VGfloat)
		evgArc(VGfloat, VGfloat, VGfloat, VGfloat, VGfloat, VGfloat)
		evgImage(VGfloat, VGfloat, int, int, char *)
		evgBegin()
		evgClear()
		evgEnd()
		evgSaveEnd(char *)
		evgBackground(unsigned int, unsigned int, unsigned int)
		evgBackgroundRGB(unsigned int, unsigned int, unsigned int, VGfloat)
		evgInit(int *, int *)
		evgFinish()
		evgSetFill(VGfloat[4])
		evgSetStroke(VGfloat[4])
		evgStrokeWidth(VGfloat)
		evgStrokeStyle(int, int)
		evgStroke(unsigned int, unsigned int, unsigned int, VGfloat)
		evgFill(unsigned int, unsigned int, unsigned int, VGfloat)
		evgFillLinearGradient(VGfloat, VGfloat, VGfloat, VGfloat, VGfloat *, int)
		evgFillRadialGradient(VGfloat, VGfloat, VGfloat, VGfloat, VGfloat, VGfloat *, int)
		evgClipRect(VGint x, VGint y, VGint w, VGint h)
		evgClipEnd()
		evgCbezierOutline(VGfloat, VGfloat, VGfloat, VGfloat, VGfloat, VGfloat, VGfloat, VGfloat)
		evgQbezierOutline(VGfloat, VGfloat, VGfloat, VGfloat, VGfloat, VGfloat)
		evgRectOutline(VGfloat, VGfloat, VGfloat, VGfloat)
		evgRoundrectOutline(VGfloat, VGfloat, VGfloat, VGfloat, VGfloat, VGfloat)
		evgEllipseOutline(VGfloat, VGfloat, VGfloat, VGfloat)
		evgCircleOutline(VGfloat, VGfloat, VGfloat)
		evgArcOutline(VGfloat, VGfloat, VGfloat, VGfloat, VGfloat, VGfloat)
		evgClearRect(unsigned int x, unsigned int y, unsigned int w, unsigned int h)

		evgInitWindowSize(int x, int y, unsigned int w, unsigned int h)
		evgWindowOpacity(unsigned int alpha)
		evgWindowPosition(int x, int y)'''

	@enum.unique
	class c(enum.IntEnum):
		none = 0
		cap_butt = 0x1700
		cap_round = 0x1701
		cap_square = 0x1702
		join_miter = 0x1800
		join_round = 0x1801
		join_bevel = 0x1802

	ptr = ct.POINTER
	ref = ct.byref

	c_int = ct.c_int
	c_int_p = ptr(ct.c_int)
	c_uint = ct.c_uint
	c_uint_p = ptr(c_uint)
	c_char_p = ct.c_char_p
	vg_int = ct.c_int32
	vg_float = ct.c_float
	class evg_font(ct.Structure): pass

	types_dict = dict(
		VGint=vg_int, VGfloat=vg_float, VGfloat_a4=vg_float*4,
		Fontinfo=evg_font, int=c_int, unsigned_int=c_uint, char_p=c_char_p )

	def __init__(self):
		self._lib = ct.CDLL('libshapes.so.1')
		self.parse_signatures(self._headers)

	def __getattr__(self, k):
		# Keys are auto-translated from following formats:
		#  evgFillLinearGradient, FillLinearGradient, fill_linear_gradient
		#  evgBackgroundRGB, BackgroundRGB, background_rgb
		if k.startswith('evg'): k = k[3:]
		if k[0].isupper(): k = '_'.join(map(str.lower, re.findall(r'[A-Z]*[a-z0-9]*', k)))
		if k.islower(): # nativ
			k = ''.join((k.title() if k not in ['rgb', 'rgba'] else k.upper()) for k in k.split('_'))
		func = getattr(self._lib, k, False)
		return func or getattr(self._lib, 'evg' + k)

	def parse_signatures(self, headers):
		replace_multi = lambda s,reps: ft.reduce(lambda a,kv: a.replace(*kv), reps.items(), s)
		type_key = lambda s: replace_multi('_'.join(s), {'*':'p','[':'_a',']':''})
		for line in filter(None, map(str.strip, headers.splitlines())):
			m = re.search(r'^(?:([\w\d]+)\s+)?([\w\d]+)\((.*)\)$', line)
			if not m: raise ValueError('Failed to parse signature: {!r}'.format(line))
			res, func, sig = m.groups()
			func = getattr(self, func)
			if res: func.restype = self.types_dict[res]
			args = list(map(str.strip, sig.split(','))) if sig else list()
			for n, arg_str in enumerate(args):
				arg = arg_str.split()
				ptr = t = None
				while arg:
					t = self.types_dict.get(type_key(arg))
					if t: break
					if arg[-1] == '*': ptr = True
					arg.pop()
				if not t: raise ValueError('Failed to parse type: {!r}'.format(arg_str))
				if ptr: t = self.ptr(t)
				args[n] = t
			func.argtypes = args
