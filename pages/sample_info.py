import dash
from dash import dcc, html, dash_table, callback
from dash.dependencies import Input, Output, State
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



dash.register_page(__name__, path='/')


layout = html.Div([

     # manuscript wording
    dbc.Card([
        html.H2(["Disease entity and study group table"],),
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
            html.H2(["Number of individuals, genders, and age groups aggregated by disease entities"],),
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

]),


