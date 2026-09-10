# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import skychart_enspima as sch
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

t = datetime.now()
obs_loc = (2.3522, 48.8566)

#Calcul de l'angle de vue
taille_capteur = 200
focale = 1000
AFOV = 2*np.arctan(taille_capteur/(2*focale))
AngleVue = 45

fig, ax, df = sch.draw(obs_loc, t, mag_max=15, figsize =(10,10), alpha=0.3, zoom_az=(0, 360), zoom_alt=(AngleVue + AFOV, AngleVue - AFOV))

plt.show()
    # Sauvegarder la figure dans un fichier
fig.savefig('vue_du_ciel.png', dpi=300)  # Sauvegarde en PNG avec une résolution de 300 dpi
print("Figure sauvegardée dans 'vue_du_ciel.png'.")
print(type(fig))
print(type(ax))