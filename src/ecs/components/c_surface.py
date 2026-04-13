class CSurface:
    """Textura y área de colisión/dibujo (un fotograma = tira horizontal / number_frames)."""

    def __init__(self, surface, number_frames=1):
        self.surface = surface
        self.num_frames = max(1, int(number_frames))
        w = surface.get_width()
        h = surface.get_height()
        self.frame_w = max(1, w // self.num_frames)
        self.frame_h = h
        self.area_w = float(self.frame_w)
        self.area_h = float(self.frame_h)
