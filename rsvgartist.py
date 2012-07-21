from matplotlib.artist import Artist
from matplotlib.transforms import Affine2D
import cairo

class RsvgArtist(Artist):
    """
    Artist that renders an rsvg handle.
    """
    def __init__(self, svg, x=0, y=0, xscale=1, yscale=1, **kwargs):
        """
        Creates an object instance.

        svg should be an instance of :class:`rsvg.Handle`.
        """
        Artist.__init__(self)
        self._svg = svg
        self.set_x(x)
        self.set_y(y)
        self.set_xscale(xscale)
        self.set_yscale(yscale)
        self.update(kwargs)

    def set_svg(self, svg):
        """Sets the image to display

        ACCEPTS: an :class:`rsvg.Handle` instance
        """
        self._svg = svg

    def set_x(self, x):
        """Sets the x coordinate of the image

        ACCEPTS: any number
        """
        self._x = x

    def set_y(self, y):
        """Sets the y coordinate of the image

        ACCEPTS: any number
        """
        self._y = y

    def set_xscale(self, xscale):
        """Sets the scale of the x coordinate

        ACCEPTS: any number
        """
        self._xscale = xscale

    def set_yscale(self, yscale):
        """Sets the scale of the y coordinate

        ACCEPTS: any number
        """
        self._yscale = yscale

    def get_svg(self): return self._svg
    def get_x(self): return self._x
    def get_y(self): return self._y
    def get_xscale(self): return self._xscale
    def get_yscale(self): return self._yscale

    def draw(self, renderer):
        if not self.get_visible(): return

        from matplotlib.backends.backend_cairo import RendererCairo
        if not isinstance(renderer, RendererCairo):
            raise TypeError('Rendering of SVG is supported only with Cairo backend.')

        renderer.open_group('svg', self.get_gid())

        trans = self.get_transform()

        gc = renderer.new_gc()
        self._set_gc_clip(gc)

        ctx = gc.ctx
        ctx.save()

        affine = trans.get_affine() + Affine2D().scale(1.0, -1.0).translate(0, renderer.height)
        mtx = affine.get_matrix()

        matrix = cairo.Matrix(mtx[0, 0], mtx[0, 1], mtx[1, 0], mtx[1, 1], mtx[0, 2], mtx[1, 2])
        posx = float(self.convert_xunits(self._x))
        posy = float(self.convert_yunits(self._y))
        matrix.translate(posx, posy)

        matrix.scale(self._xscale, -self._yscale)

        ctx.transform(matrix)

        self._svg.render_cairo(ctx)

        ctx.restore()
        gc.restore()

        renderer.close_group('svg')
