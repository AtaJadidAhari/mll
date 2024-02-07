import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash import dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
import plotly.io as pio

sample_summary_tab = pd.read_csv("./data/agg_table/sample_summary_tab.csv", sep=',')

manuscript_wording = pd.read_csv("./data/leukemie_driver_manuscript_wording-sample_annotation.tsv", sep="\t")
manuscript_wording = manuscript_wording.drop(
    ["Cohort during analysis", "Cohort German abbreviation", "Study group during analysis"], axis=1)

manuscript_wording = manuscript_wording.rename(columns={"Cohort": "Disease entity",
                                                        "Cohort abbreviation": "Abbreviation",
                                                        "Number of sampples per cohort": "Number of samples per disease entity", })


def age_distribution():
    subset = sample_summary_tab.iloc[:, [0, 2, 3]]
    legend_names = {'Number_of_male': 'Male', 'Number_of_female': 'Female'}
    age_fig = px.bar(subset, x='DiseaseEntity', y=['Number_of_male', 'Number_of_female'],
                     labels={'value': 'Number of Individuals', 'variable': 'Gender', "DiseaseEntity": "Disease entity"},
                     category_orders={"Gender": ["Male", "Female"]},
                     barmode='group').update_layout(template="plotly_white")
    age_fig = age_fig.for_each_trace(lambda t: t.update(name=legend_names[t.name],
                                                        legendgroup=legend_names[t.name],
                                                        hovertemplate=t.hovertemplate.replace(t.name,
                                                                                              legend_names[t.name])
                                                        )
                                     )
    return age_fig


external_stylesheets = [dbc.themes.BOOTSTRAP]

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True, use_pages=True)
dash.register_page("Sample info", path='/')
app.title = "MLL5kdata"

app.scripts.config.serve_locally = True
# Define the layout of the app
app.layout = dbc.Container([

     dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Transcriptomics", href="/transcriptomics")),
                dbc.NavItem(dbc.NavLink("Prediction", href="/prediction")),
                dbc.NavItem(dbc.NavLink("Genomics", href="/genomics")),   
                dbc.NavItem(dbc.NavLink("Sample info", href="/")),          
            ],
            sticky="top",
            brand="MLL5kData",
            brand_href="/",
            color="dark",
            dark=True,
        ), 
        
    dbc.Card([
        html.H3(
            "Analysis of 3,760 hematologic malignancies reveals rare transcriptomic aberrations of driver genes.", ),
        html.A("https://doi.org/10.1101/2023.08.08.23293420", href="https://doi.org/10.1101/2023.08.08.23293420",
               target="_blank"),


    ]),
        
   



    # manuscript wording
    dbc.Card([
        html.H2(["Abbreviation table"], style={'textAlign': 'center'}),
        dash_table.DataTable(id='manuscript_wording_table',
                             columns=[{'name': col, 'id': col} for col in manuscript_wording.columns],
                             data=manuscript_wording.to_dict('records'),
                             page_size=10,  # Show 10 rows per page
                             sort_action='native',  # Enable column sorting
                             filter_action='native',  # Enable built-in filtering
                             style_table={'height': '300px', 'overflowY': 'auto'},
                             export_format='csv',
                             )
    ]),

    # Number of individuals, genders, and age
    dbc.Card([
        dbc.Row([
            html.H2(["Number of individuals, genders, and age groups aggregated by disease entities"],
                    style={'textAlign': 'center'}),

            # Sidebar layout

            # Main panel layout
            dbc.Row([
                dcc.Graph(
                    id='age_bar_plot',
                    figure=age_distribution()
                ),
                dbc.Col([
                    dcc.Dropdown(
                        id='drop_down_age',
                        options=[{'label': group, 'value': group} for group in sample_summary_tab['DiseaseEntity']],
                        value='AML',
                        multi=False
                    ),
                ], width=4),
                dcc.Graph(id='sample_summary_histogram'),
                dash_table.DataTable(id='sample_summary_table',
                                     columns=[{'name': col, 'id': col} for col in sample_summary_tab.columns],
                                     data=sample_summary_tab.to_dict('records'),
                                     page_size=10,  # Show 10 rows per page
                                     sort_action='native',  # Enable column sorting
                                     filter_action='native',  # Enable built-in filtering
                                     style_table={'height': '300px', 'overflowY': 'auto'},
                                     export_format='csv',
                                     )
            ], ),
        ], ),
    ], ),
    dash.page_container,
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
