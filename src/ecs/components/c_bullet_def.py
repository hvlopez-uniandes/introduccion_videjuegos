# Definición de la bala cargada desde bullet.json (va en la misma entidad que el spawner).


class CBulletDef:
    def __init__(self, w, h, r, g, b, velocity):
        self.w = float(w)
        self.h = float(h)
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)
        self.velocity = float(velocity)
