"""
Buggy NON-MODULAR snippet from matplotlib, bug ID 12.
"""
def buggy_function(rs, data, freq=None):
    y, xmin, xmax = cbook.delete_masked_points(y, xmin, xmax)
    xmin = np.resize(xmin, y.shape)
    xmax = np.resize(xmax, y.shape)
    verts = [((thisxmin, thisy), (thisxmax, thisy))
               for thisxmin, thisxmax, thisy in zip(xmin, xmax, y)]
    lines = mcoll.LineCollection(verts, colors=colors,
    x, ymin, ymax = cbook.delete_masked_points(x, ymin, ymax)
    ymin = np.resize(ymin, x.shape)
    ymax = np.resize(ymax, x.shape)
    verts = [((thisx, thisymin), (thisx, thisymax))
               for thisx, thisymin, thisymax in zip(x, ymin, ymax)]
    lines = mcoll.LineCollection(verts, colors=colors,
    return rs