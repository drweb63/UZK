from reportlab.graphics.barcode import qr, createBarcodeDrawing
from reportlab.graphics.shapes import Drawing
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF, renderPM

#----------------------------------------------------------------------


class Code128(Drawing):
    """
    Useage:
        Code128("1234567890").save(
            formats=['gif','pdf'],
            outDir='.',
            fnRoot='code128'
        )
    """
    def __init__(self, text_value, *args, **kw):
        barcode = createBarcodeDrawing(
            'Code128',
            value=text_value,
            barHeight=6*mm,
            humanReadable=True,
            width=450,
            height=250
        )
        Drawing.__init__(
            self,
            barcode.width,
            barcode.height,
            *args,
            **kw
        )
        self.add(barcode, name='barcode')


def createBarCodes(value):
    """
    Create barcode examples and embed in a PDF
    """

    pdf_file_name = "qr_barcode.pdf"
    png_file_name = "qr_barcode.png"
    width = 300
    height = 200

    # draw a QR code
    qr_code = qr.QrCodeWidget(
        value=value,
        barWidth=width,
        barHeight=height
    )

    # to PDF
    pdf_canvas = canvas.Canvas(
        pdf_file_name, pagesize=letter
    )
    pdf_draw = Drawing(45, 45)
    pdf_draw.add(qr_code)
    renderPDF.draw(pdf_draw, pdf_canvas, 15, 405)
    pdf_canvas.save()

    # to PNG
    png_draw = Drawing(width, height)
    png_draw.add(qr_code)
    png_canvas = renderPM.drawToPIL(png_draw)
    png_canvas.save(png_file_name, "png")


if __name__ == "__main__":
    value = "1234567890"
    createBarCodes(value)
    Code128(value).save(
        formats=['gif', 'pdf'],
        outDir='.',
        fnRoot='code128'
    )