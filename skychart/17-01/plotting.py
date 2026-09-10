from collections.abc import Iterable
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from .tools import radec_to_altaz, moveObserver
from .load_data import load_constellations, create_edges, load_hipparcos

def visible_hipparcos(delta_lat, delta_lon, obs_loc, t):
    lon, lat = moveObserver(delta_lat, delta_lon, obs_loc)
    df = load_hipparcos()
    df['alt'], df['az'] = radec_to_altaz(lon, lat, df['ra'], df['dec'], t)
    df1 = df[df['alt']>0]
    return df

def draw_chart(df, df_show, dc_const, alpha, figsize=None, rotation_angle=0):
    """
    df : visible hipparcos stars for the observer
    df_show : stars to be shown in the chart
    dc_const : dictionary of constellations
    """
    edges = create_edges(dc_const)
    edges = [i for i in edges if (i[0] in df.index) and (i[1] in df.index)]

    edge1 = [i[0] for i in edges]
    edge2 = [i[1] for i in edges]
    
    xy1 = df[['az', 'alt']].loc[edge1].values
    xy2 = df[['az', 'alt']].loc[edge2].values
    
    xy1[:,0] = xy1[:,0]*(np.pi/180)
    xy2[:,0] = xy2[:,0]*(np.pi/180)
    
    xy1[:,1] = xy1[:,1]
    xy2[:,1] = xy2[:,1]
    
    lines_xy = np.array([*zip(xy1,xy2)])

    mag_max = df_show['Vmag'].max()

    marker_size = (0.5 + mag_max - df['Vmag'].values) ** 2

    fig, ax = plot_altaz(df_show['az'], df_show['alt'], mag=df_show['Vmag'], figsize=figsize, rotation_angle=rotation_angle)
    ax.add_collection(LineCollection(lines_xy, alpha=alpha, color='aquamarine'))
    
    return fig, ax, df_show


def draw(obs_loc, delta_lat, delta_lon, t, mag_max=5, alpha=0.3, figsize=None, rotation_angle=0):
    df = visible_hipparcos(delta_lat, delta_lon, obs_loc, t)
    
    # Appliquer le décalage global
    df['az'] = (df['az']) % 360
    df['alt'] = df['alt']
    
    # Filtrer pour garder uniquement les étoiles visibles
    df = df[df['alt'] > 0]

    # Filtrer les étoiles selon leur magnitude apparente
    df_show = df[df['Vmag'] < mag_max]
    
    dc_const = load_constellations()
    return draw_chart(df, df_show, dc_const, alpha, figsize, rotation_angle)


# def plot_altaz(az, alt, mag=None, size=None, color='w', alpha=1, marker='o', ax=None, figsize=None, slide_az=0, slide_alt=0,zoom=2):
    # """
    # Plot positions of bodies based on altitude/azimuth coordinates
    # Arguments
    # ---------
        # az (iter of float): azimuth values
        # alt (iter of float): altitude values
        # mag (iter of float): apparent magnitudes; default None.
        # size (int): size; default None.
        # color (str): color; default 'k'.
        # alpha (float): alpha value (transparency), between 0 and 1; default 1.
        # marker (str): marker shape; default 'o'.
        # ax (axes): axes object; default None.
    # Returns
    # -------
        # matplotlib axes object
    # """

    # if isinstance(az, Iterable):
        # az = np.array(az)
        # alt = np.array(alt)
        # mag = np.array(mag) if mag is not None else None
    # else:
        # az = np.array([az])
        # alt = np.array([alt])
        # mag = None
        
    # az  = (az+slide_az)*(np.pi/180)
    # alt = (alt + slide_alt)

    # if size is None:
        # if mag is None:
            # size = [5] * len(az)
        # else:
            # size = (0.1 + max(mag)-mag)**1.8

    # plt.style.use('dark_background')
    # if ax is None:
        # if figsize is None:
            # fig = plt.figure()
        # else:
            # fig = plt.figure(figsize=figsize)
        # ax = fig.add_axes([0.1,0.1,0.8,0.8], polar=True)
        # ax.set_theta_zero_location('N')
        # ax.set_rlim(90, 0, 1)
        # ax.set_yticks(np.arange(0,91,30))
        # ax.set_xticks([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi, 5*np.pi/4, 6*np.pi/4, 7*np.pi/4])
        # ax.set_xticklabels(['N','NE','E','SE','S','SW','W','NW'])
        # for label in ax.get_xticklabels():
            # label.set_rotation(45)  # Rotation de 45 degrés
            # label.set_horizontalalignment('center') 
        # ax.tick_params(axis=u'both', which=u'both',length=0)
    # if matplotlib.__version__ < '3.0.0':
        # alt = [90-i for i in alt]
    # ax.scatter(az, alt, c=color, s=size, alpha=alpha, marker=marker)
    # ax.grid(True, alpha=0.1)
    # return fig, ax
def plot_altaz(az, alt, mag=None, size=None, color='w', alpha=1, marker='o', ax=None, figsize=None, slide_az=0, slide_alt=0, zoom=2, rotation_angle=0):
    """
    Plot positions of bodies based on altitude/azimuth coordinates
    Arguments
    ---------
        az (iter of float): azimuth values
        alt (iter of float): altitude values
        mag (iter of float): apparent magnitudes; default None.
        size (int): size; default None.
        color (str): color; default 'k'.
        alpha (float): alpha value (transparency), between 0 and 1; default 1.
        marker (str): marker shape; default 'o'.
        ax (axes): axes object; default None.
        rotation_angle (float): angle to rotate the entire circle (degrees).
    Returns
    -------
        matplotlib axes object
    """
    if isinstance(az, Iterable):
        az = np.array(az)
        alt = np.array(alt)
        mag = np.array(mag) if mag is not None else None
    else:
        az = np.array([az])
        alt = np.array([alt])
        mag = None
        
    az  = az * (np.pi / 180)
    alt = alt

    if size is None:
        if mag is None:
            size = [5] * len(az)
        else:
            size = (0.1 + max(mag) - mag) ** 1.8

    plt.style.use('dark_background')
    if ax is None:
        if figsize is None:
            fig = plt.figure()
        else:
            fig = plt.figure(figsize=figsize)
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
        
        # Rotation globale du cercle
        ax.set_theta_zero_location('N')  # Position initiale (Nord en haut)
        ax.set_theta_offset(np.radians(rotation_angle+90))  # Rotation du cercle
        ax.set_rlim(90 / zoom, 0, 1)
        ax.set_yticks(np.arange(0, 91, 30))
        ax.set_xticks([0, np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi, 5 * np.pi / 4, 6 * np.pi / 4, 7 * np.pi / 4])
        ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])

        ax.tick_params(axis=u'both', which=u'both', length=0)
    if matplotlib.__version__ < '3.0.0':
        alt = [90 - i for i in alt]
    ax.scatter(az, alt, c=color, s=size, alpha=alpha, marker=marker)
    ax.grid(True, alpha=0.1)
    return fig, ax


