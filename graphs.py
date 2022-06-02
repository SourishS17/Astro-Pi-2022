import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.express as px
from time import sleep
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib as mpl


df = pd.read_csv("results.csv",usecols=["latitude", "longitude", "SAVI", "NDWI", "RCI"])

# initialize an axis
fig, ax = plt.subplots(figsize=(8,6))

# plot map on axis
countries = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
countries.plot(color="lightgrey",ax=ax)



# plot points
df.plot(x="longitude", y="latitude", kind="scatter", c="SAVI", colormap="Greens", 
        title=f"SAVI Global Distribution", ax=ax, colorbar=False)

# define colorbar values
norm = mpl.colors.Normalize(vmin=df["SAVI"].min(), vmax=df["SAVI"].max())

# set colorbar on ax
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="2%", pad=0.15)
mpl.colorbar.ColorbarBase(cax, cmap=mpl.cm.Greens, norm=norm, label="SAVI")

# add grid
#ax.grid(b=True, alpha=0.5)

plt.show()


#sleep(10)

df = pd.read_csv("results.csv",usecols=["latitude", "longitude", "SAVI", "NDWI", "RCI"])

# initialize an axis
fig, ax = plt.subplots(figsize=(8,6))

# plot map on axis
countries = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
countries.plot(color="lightgrey",ax=ax)



# plot points
df.plot(x="longitude", y="latitude", kind="scatter", c="RCI", colormap="Reds", 
        title=f"RCI Global Distribution", ax=ax, colorbar=False)

# define colorbar values
norm = mpl.colors.Normalize(vmin=df["RCI"].min(), vmax=df["RCI"].max())

# set colorbar on ax
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="2%", pad=0.15)
mpl.colorbar.ColorbarBase(cax, cmap=mpl.cm.Reds, norm=norm, label="RCI")

# add grid
#ax.grid(b=True, alpha=0.5)

plt.show()


df = pd.read_csv("results.csv",usecols=["latitude", "longitude", "SAVI", "NDWI", "RCI"])

# initialize an axis
fig, ax = plt.subplots(figsize=(8,6))

# plot map on axis
countries = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
countries.plot(color="lightgrey",ax=ax)



# plot points
df.plot(x="longitude", y="latitude", kind="scatter", c="NDWI", colormap="Blues", 
        title=f"NDWI Global Distribution", ax=ax, colorbar=False)

# define colorbar values
norm = mpl.colors.Normalize(vmin=df["NDWI"].min(), vmax=df["NDWI"].max())

# set colorbar on ax
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="2%", pad=0.15)
mpl.colorbar.ColorbarBase(cax, cmap=mpl.cm.Blues, norm=norm, label="NDWI")

# add grid
#ax.grid(b=True, alpha=0.5)

plt.show()


"""
# initialize an axis
fig, ax = plt.subplots(figsize=(8,6))

# plot map on axis
countries = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
countries.plot(color="lightgrey",ax=ax)

#fig = px.scatter_geo(df,lat='latitude',lon='longitude', hover_name="SAVI")
#fig.update_layout(title = 'SAVI Global Distribution', title_x=0.5)
#fig.show()

# plot points
df.plot(x="longitude", y="latitude", kind="scatter", c="SAVI", colormap="Greens", 
        title=f"SAVI Global Distribution", ax=ax,grid=False)
# set colorbar on ax

# add grid
#ax.grid(b=True, alpha=0.5)

plt.show()"""
