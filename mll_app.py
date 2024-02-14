import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash import dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
import plotly.io as pio
import dash_loading_spinners as dls

sample_summary_tab = pd.read_csv("./data/agg_table/sample_summary_tab.csv", sep=',')

manuscript_wording = pd.read_csv("./data/leukemie_driver_manuscript_wording-sample_annotation.tsv", sep="\t")
manuscript_wording = manuscript_wording.drop(
    ["Cohort during analysis", "Cohort German abbreviation", "Study group during analysis"], axis=1)

manuscript_wording = manuscript_wording.rename(columns={"Cohort": "Disease entity",
                                                        "Cohort abbreviation": "Abbreviation",
                                                        "Number of sampples per cohort": "Number of samples per disease entity", })

external_stylesheets = [dbc.themes.BOOTSTRAP]

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True, use_pages=True)

app.title = "MLL5kdata"

app.scripts.config.serve_locally = True
# Define the layout of the app
app.layout = dbc.Container([

    dbc.NavbarSimple(id='my_vavbar',
                     children=[
                         dbc.NavItem(dbc.NavLink("Driver predictor", href="/prediction")),
                         dbc.NavItem(dbc.NavLink("Transcriptomics", href="/transcriptomics", )),
                         dbc.NavItem(dbc.NavLink("Genomics", href="/genomics")),
                         dbc.NavItem(dbc.NavLink("Sample info", href="/", )),
                     ],
                     sticky="top",
                     color="dark",
                     dark=True,
                     ),

    dbc.Card([
        html.H3(
            "Analysis of 3,760 hematologic malignancies reveals rare transcriptomic aberrations of driver genes", ),
        html.H4(["Companion website to the study: Xueqi Cao, Sandra Huber, Ata Jadid Ahari, Franziska R. Traube, Marc Seifert, Christopher C. Oakes, Polina Secheyko, Sergey Vilov, Ines Scheller, Nils Wagner, Vicente A. Yépez, Piers Blombery, Torsten Haferlach, Matthias Heinig, Leonhard Wachutka, Stephan Hutter, Julien Gagneur", html.Br(), "medRXiv: ", html.A('https://doi.org/10.1101/2023.08.08.23293420', href='https://doi.org/10.1101/2023.08.08.23293420', target='_blank'), html.Br(), "github: ", html.A('https://github.com/gagneurlab/Leukemia_outlier', href='https://github.com/gagneurlab/Leukemia_outlier', target='_blank')], style={"text-align": "left"},),
        html.H4(["Request access to the complete data shall be done via the website of the Torsten Haferlach Leukemia Diagnostics Foundation: ", html.A('https://torsten-haferlach-leukaemiediagnostik-stiftung.de/en/', href='https://torsten-haferlach-leukaemiediagnostik-stiftung.de/en/', target='_blank')], style={"text-align": "left"},), 
    ]),

    dash.page_container,
    dls.Hash(id='loading', fullscreen=True, show_initially=True, ),
], )


@app.callback(
    Output('sample_summary_histogram', 'figure'),
    [Input('drop_down_age', 'value')]
)
def update_sample_summary_histogram(selected_entity):
    gene_data_subset = sample_summary_tab[sample_summary_tab['DiseaseEntity'] == selected_entity]
    melted_df = gene_data_subset.melt(id_vars=['DiseaseEntity'], value_vars=gene_data_subset.columns[4:],
                                      var_name='Age groups',
                                      value_name='Number of individuals')
    fig = px.bar(melted_df, x='Age groups', y='Number of individuals', color='Age groups',
                 )
    fig.update_traces(width=1).update_layout(template="plotly_white")
    return fig


server = app.server

# Run the Dash app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)
