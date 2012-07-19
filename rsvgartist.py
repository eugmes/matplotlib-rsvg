from matplotlib.artist import Artist
from matplotlib.transforms import Affine2D
import cairo

class RsvgArtist(Artist):
    """
    Artist that renders an rsvg handle.
    """
    def __init__(self, svg, x=0, y=0, xscale=1, yscale=1):
        """
        Creates an object instance.

        svg should be an object of class rsvg.Handle.
        """
        Artist.__init__(self)
        self._svg = svg
        self._x = x
        self._y = y
        self._xscale = xscale
        self._yscale = yscale

    def draw(self, renderer, *args, **kwargs):
        if not self.get_visible(): return

        from matplotlib.backends.backend_cairo import RendererCairo
        if not isinstance(renderer, RendererCairo):
            raise TypeError('Rendering of SVG is supported only with Cairo backend.')

        renderer.open_group('svg', self.get_gid())

        trans = self.get_transform()

        ctx = renderer.gc.ctx
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

        renderer.close_group('svg')
