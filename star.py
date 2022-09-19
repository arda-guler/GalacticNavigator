class star:
    def __init__(self, hyg, hip, hd, hr, gl, bf, proper, ra, dec, dist,
                 pmra, pmdec, rv, mag, absmag, spect, ci, x, y, z, vx, vy, vz,
                 rarad, decrad, pmrarad, prdecrad, bayer, flam, con, comp,
                 comp_primary, base, lum, var, var_min, var_max):

        self.hyg = hyg
        self.hip = hip
        self.hd = hd
        self.hr = hr
        self.gl = gl
        self.bf = bf
        self.ra = ra
        self.dec = dec
        self.proper = proper
        self.dist = float(dist)
        self.pmra = pmra
        self.pmdec = pmdec
        self.rv = rv
        self.mag = float(mag)
        self.absmag = float(absmag)
        self.spect = spect
        self.ci = ci
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.pos = [float(x), float(y), float(z)]
        self.vx = float(vx)
        self.vy = float(vy)
        self.vz = float(vz)
        self.vel = [float(vx), float(vy), float(vz)]
        self.rarad = float(rarad)
        self.decrad = float(decrad)
        self.skypos = [float(rarad), float(decrad)]
        self.pmrarad = float(pmrarad)
        self.prdecrad = float(prdecrad)
        self.skyvel = [float(pmrarad), float(prdecrad)]
        self.bayer = bayer
        self.flam = flam
        self.con = con
        self.comp = comp
        self.comp_primary = comp_primary
        self.base = base
        self.lum = lum
        self.var = var
        self.var_min = var_min
        self.var_max = var_max
        self.var_range = [var_min, var_max]

