# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 11:34:07 2025

@author: vhdl
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
import skychart_enspima as sch
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Fonction pour afficher la vue du ciel
def page_vue(focale, lentille, barlow):
    try:
        # Conversion des entrées utilisateur
        
        focale = float(focale)
        lentille = float(lentille)
        barlow = float(barlow)

        # Calculs nécessaires
        t = datetime.now()
        obs_loc = (2.3522, 48.8566)  # Coordonnées de Paris
        taille_capteur = lentille * barlow
        AFOV = 2 * np.arctan(taille_capteur / (2 * focale))
        AngleVue = 45

        # Génération de la figure Matplotlib
        fig, ax, df = sch.draw(
            obs_loc, t, mag_max=15,
            figsize=(10, 10), alpha=0.3,
            zoom_az=(0, 360), zoom_alt=(AngleVue + AFOV, AngleVue - AFOV)
        )

        # Création d'une nouvelle fenêtre pour la visualisation
        VueCiel = tk.Toplevel()
        VueCiel.title("Visualisation des étoiles")
        VueCiel.geometry("800x800")

        # Intégration de la figure dans Tkinter
        canvas = FigureCanvasTkAgg(fig, master=VueCiel)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Bouton pour fermer la fenêtre
        quit_button = tk.Button(VueCiel, text="Fermer", command=VueCiel.destroy)
        quit_button.pack()

    except ValueError:
        # Gérer les erreurs de conversion
        error_popup("Veuillez entrer des valeurs numériques valides.")


# Fonction pour afficher une boîte d'erreur
def error_popup(message):
    popup = tk.Toplevel()
    popup.title("Erreur")
    tk.Label(popup, text=message, fg="red").pack(pady=10, padx=10)
    tk.Button(popup, text="OK", command=popup.destroy).pack(pady=5)


# Fenêtre principale
root = tk.Tk()
root.title("Accueil")
root.geometry("400x300")

# Création du notebook pour les onglets
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Création des deux onglets
onglet1 = ttk.Frame(notebook)
onglet2 = ttk.Frame(notebook)
notebook.add(onglet1, text="Onglet 1")
notebook.add(onglet2, text="Onglet 2")

# Contenu de l'onglet 1 : plusieurs champs de texte
label1 = ttk.Label(onglet1, text="Saisissez des informations :")
label1.pack(pady=10)

# Champs de texte
fields = [("Distance focale du télescope :", "entry1"),
          ("Diamètre de la lentille :", "entry2"),
          ("Zoom lentille Barlow :", "entry3")]
entries = {}

for label_text, entry_var in fields:
    label = ttk.Label(onglet1, text=label_text)
    label.pack(anchor="w", padx=10)
    entry = ttk.Entry(onglet1)
    entry.pack(padx=10, pady=5, fill="x")
    entries[entry_var] = entry

# Bouton pour lancer le calcul
button = tk.Button(
    root,
    text="Lancez le calcul",
    bg="lightblue",
    fg="black",
    padx=20,
    pady=10,
    command=lambda: page_vue(
        entries["entry1"].get(),
        entries["entry2"].get(),
        entries["entry3"].get()
    )
)
button.pack(pady=30)

# Contenu de l'onglet 2 : simple message
label2 = ttk.Label(onglet2, text="Bienvenue dans l'Onglet 2")
label2.pack(pady=20)

# Lancement de la boucle principale
root.mainloop()
