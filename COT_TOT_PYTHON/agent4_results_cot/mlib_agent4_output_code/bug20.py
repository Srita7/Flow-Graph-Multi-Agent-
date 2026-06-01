"""
Buggy NON-MODULAR snippet from matplotlib, bug ID 20.
"""
def buggy_function(rs, data, freq=None):
    ax.set_frame_on(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor((1, 0, 0, 0))
    # Check if a point is in an axes.
    # axes: topmost axes containing the point, or None if no axes.
    # if a.patch.contains_point(xy)]
    return rs