#! /usr/bin/python
import rsvgartist
import matplotlib
matplotlib.use('cairo.pdf')
import matplotlib.pyplot as plt
import rsvg
import matplotlib.transforms as mtrans

p = plt.subplot(221, aspect='equal')
p.set_title('A small tiger')

x = [-1, 0, 1]
y = [1, 0, -1]
p.scatter(x, y)
p.grid()

svg = rsvg.Handle('tiger.svg')

scale = 1.0 / svg.props.width

p.add_artist(rsvgartist.RsvgArtist(svg, -0.5, 0.5, scale, scale))

p = plt.subplot(224, aspect='equal')
p.set_title('A larger tiger over the grid')

p.scatter(x, y, zorder=10)
p.grid(zorder=5)

svg = rsvg.Handle('tiger.svg')
scale = 4.0 / svg.props.width

p.add_artist(rsvgartist.RsvgArtist(svg, -1.5, 1.5, scale, scale, zorder=7))

plt.savefig('fig.pdf')
