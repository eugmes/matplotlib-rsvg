#! /usr/bin/python
import rsvgartist
import matplotlib
matplotlib.use('cairo.pdf')
import matplotlib.pyplot as plt
import rsvg
import matplotlib.transforms as mtrans

p = plt.subplot(111)

x = [-1, 0, 1]
y = [1, 0, -1]
p.scatter(x, y)
p.grid()

svg = rsvg.Handle('tiger.svg')

scale = 1.0 / svg.props.width

p.add_artist(rsvgartist.RsvgArtist(svg, -0.5, 0.5, scale, scale))

plt.savefig('fig.pdf')
