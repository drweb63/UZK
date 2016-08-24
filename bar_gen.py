from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics.shapes import Drawing
from reportlab.lib.units import mm

#----------------------------------------------------------------------


class Code128(Drawing):
    def __init__(self, text_value, *args, **kw):
        barcode = createBarcodeDrawing(
            'Code128',
            value=text_value,
            barHeight=6*mm,
            humanReadable=True,
            width=220,
            height=150
        )
        Drawing.__init__(
            self,
            barcode.width,
            barcode.height,
            *args,
            **kw
        )
        self.add(barcode, name='barcode')
