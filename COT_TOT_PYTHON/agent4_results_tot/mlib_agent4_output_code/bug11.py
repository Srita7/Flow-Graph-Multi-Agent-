"""
Buggy NON-MODULAR snippet from matplotlib, bug ID 11.
"""
def buggy_function(rs, data, freq=None):
        if dpi is not None:
                dpi_orig = self.figure.dpi
                self.figure.dpi = dpi
                tx, ty = self._get_xy_display()
                return Bbox.from_bounds(tx, ty, 0, 0)
            bbox, info, descent = self._get_layout(self._renderer)
            x, y = self.get_unitless_position()
            x, y = self.get_transform().transform((x, y))
            bbox = bbox.translated(x, y)
            if dpi is not None:
                self.figure.dpi = dpi_orig
            return bbox
    return rs