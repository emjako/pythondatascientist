import pandas as pd
from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, Div, HoverTool
from bokeh.models.widgets import Select
from bokeh.io import curdoc

# Récupération et préparation des données
# (on extrait uniquement les logements avec plus de 20 commentaires)
listing=pd.read_csv("../data/listing_extrait.csv", low_memory=False)
listing_chers = listing[listing["number_of_reviews"]>20]\
[["host_is_superhost","number_of_reviews", "price","name","room_type",
  "bedrooms","review_scores_rating"]]
# Définition des widgets (un outil de sélection en fonction de la colonne
# superhost)
superhost = Select(title="Super-host", value="All", options=["Vrai","Faux"])
# Définition de la source de données. Elle est vide et utilise un dictionnaire
source = ColumnDataSource(data=dict(nb_com=[], note_com=[], type_chambre=[],
                                    name=[], price=[]))
# Définition des informations à afficher lorsqu’on passe sur un point
TOOLTIPS=HoverTool(tooltips=[
    ("Nom", "@name"),
    ("Prix", "@price"),
    ("Nombre de commentaires", "@nb_com"),
    ("Note moyenne", "@note_com"),
    ("Type logement", "@type_chambre")
])

# construction de la figure et ajout des points à partir des données
p = figure(plot_height=600, plot_width=700,
title="", toolbar_location=None, tools=[TOOLTIPS])
p.circle(x="nb_com", y="note_com", source=source, size=2)

# définition d’une fonction de mise à jour des données
def update() :
    if superhost.value == "Vrai":
        super="t"
    else:
        super="f"

    listing2=listing_chers[listing_chers["host_is_superhost"]==super]
    p.xaxis.axis_label = "Nombre de commentaires"
    p.yaxis.axis_label = "Note moyenne"
    # mise à jour des données
    source.data = dict(nb_com=listing2["number_of_reviews"],
                       note_com=listing2["review_scores_rating"],
                       type_chambre = listing2["room_type"],
                       name=listing2["name"],
                       price=listing2["price"]
                      )
# gestion des contrôles pour la mise à jour
# (on en a un seul dans notre cas Select)
controls = [superhost]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

# construction du layout pour l’affichage
inputs = widgetbox(*controls, sizing_mode="fixed")
l = layout([inputs, p], sizing_mode="fixed")
# premier chargement des données
update()
# utilisation de curdoc() pour générer la dataviz
curdoc().add_root(l)
curdoc().title = "AirBnB"
