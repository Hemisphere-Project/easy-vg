#include <VG/openvg.h>
#include <VG/vgu.h>
#include "fontinfo.h"

#if defined(__cplusplus)
extern "C" {
#endif
	extern VGfloat TextHeight(Fontinfo *, int);
	extern VGfloat TextDepth(Fontinfo *, int);
	extern VGfloat TextWidth(const char *, Fontinfo *, int);
	extern void RGBA(unsigned int, unsigned int, unsigned int, VGfloat, VGfloat[4]);
	extern void RGB(unsigned int, unsigned int, unsigned int, VGfloat[4]);

	extern void evgTranslate(VGfloat, VGfloat);
	extern void evgRotate(VGfloat);
	extern void evgShear(VGfloat, VGfloat);
	extern void evgScale(VGfloat, VGfloat);
	extern void evgText(VGfloat, VGfloat, const char *, Fontinfo *, int);
	extern void evgTextMid(VGfloat, VGfloat, const char *, Fontinfo *, int);
	extern void evgTextEnd(VGfloat, VGfloat, const char *, Fontinfo *, int);
	extern void evgCbezier(VGfloat, VGfloat, VGfloat, VGfloat, VGfloat, VGfloat, VGfloat, VGfloat);
	extern void evgQbezier(VGfloat, VGfloat, VGfloat, VGfloat, VGfloat, VGfloat);
	extern void evgPolygon(VGfloat *, VGfloat *, VGint);
	extern void evgPolyline(VGfloat *, VGfloat *, VGint);
	extern void evgRect(VGfloat, VGfloat, VGfloat, VGfloat);
	extern void evgLine(VGfloat, VGfloat, VGfloat, VGfloat);
	extern void evgRoundRect(VGfloat, VGfloat, VGfloat, VGfloat, VGfloat, VGfloat);
	extern void evgEllipse(VGfloat, VGfloat, VGfloat, VGfloat);
	extern void evgCircle(VGfloat, VGfloat, VGfloat);
	extern void evgArc(VGfloat, VGfloat, VGfloat, VGfloat, VGfloat, VGfloat);
	extern void evgImage(VGfloat, VGfloat, int, int, const char *);
	extern void evgBegin();
	extern void evgClear();
	extern void evgEnd();
	extern void evgSaveEnd(const char *);
	extern void evgBackground(unsigned int, unsigned int, unsigned int);
	extern void evgBackgroundRGB(unsigned int, unsigned int, unsigned int, VGfloat);
	extern void evgInit(int *, int *);
	extern void evgFinish();
	extern void evgSetFill(VGfloat[4]);
	extern void evgSetStroke(VGfloat[4]);
	extern void evgStrokeWidth(VGfloat);
	extern void evgStroke(unsigned int, unsigned int, unsigned int, VGfloat);
	extern void evgFill(unsigned int, unsigned int, unsigned int, VGfloat);
	extern void evgFillLinearGradient(VGfloat, VGfloat, VGfloat, VGfloat, VGfloat *, int);
	extern void evgFillRadialGradient(VGfloat, VGfloat, VGfloat, VGfloat, VGfloat, VGfloat *, int);
	extern void evgClipRect(VGint x, VGint y, VGint w, VGint h);
	extern void evgClipEnd();
	extern void evgCbezierOutline(VGfloat, VGfloat, VGfloat, VGfloat, VGfloat, VGfloat, VGfloat, VGfloat);
	extern void evgQbezierOutline(VGfloat, VGfloat, VGfloat, VGfloat, VGfloat, VGfloat);
	extern void evgRectOutline(VGfloat, VGfloat, VGfloat, VGfloat);
	extern void evgRoundrectOutline(VGfloat, VGfloat, VGfloat, VGfloat, VGfloat, VGfloat);
	extern void evgEllipseOutline(VGfloat, VGfloat, VGfloat, VGfloat);
	extern void evgCircleOutline(VGfloat, VGfloat, VGfloat);
	extern void evgArcOutline(VGfloat, VGfloat, VGfloat, VGfloat, VGfloat, VGfloat);
	extern void evgClearRect(unsigned int x, unsigned int y, unsigned int w, unsigned int h);

	extern Fontinfo loadfont(const int *, const int *, const unsigned char *, const int *, const int *, const int *,
				 const short *, int);
	extern void unloadfont(VGPath *, int);
	extern VGImage createImageFromJpeg(const char *);
	extern void makeimage(VGfloat, VGfloat, int, int, VGubyte *);
	extern void saveterm();
	extern void restoreterm();
	extern void rawterm();

	// Added by Paeryn
	extern void evgInitWindowSize(int x, int y, unsigned int w, unsigned int h);
	extern void evgWindowOpacity(unsigned int alpha);
	extern void evgWindowPosition(int x, int y);
#if defined(__cplusplus)
}
#endif
