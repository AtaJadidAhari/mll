import dash
from dash import dcc, html, dash_table, callback
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
import plotly.io as pio

prediction_complete = pd.read_csv("./data/prediction/S1_prediction_complete_dataset.csv", sep=",")

prediction_strudy_group = pd.read_csv("./data/prediction/S2_prediction_study_groups.csv", sep=",")


dash.register_page(__name__)

layout = html.Div([

    
    # Prediction all
    dbc.Card([
        dbc.Row([
            html.H2(["Prediction result of the hematologic malignancy drive gene prediction model using the complete dataset"], style={'textAlign': 'center'}),
            # Main panel layout
            dbc.Row([
                dash_table.DataTable(id='prediction_all',
                                     columns=[{'name': col, 'id': col} for col in prediction_complete.columns],
                                     data=prediction_complete.to_dict('records'),
                                     page_size=10,  # Show 10 rows per page
                                     sort_action='native',  # Enable column sorting
                                     filter_action='native',  # Enable built-in filtering
                                     style_table={'height': '400px', 'overflowY': 'auto'},
                                     export_format='csv',
                                     )
            ], ),

        ], ),
    ], ),
    
    # Prediction cohort wise
    dbc.Card([
        dbc.Row([
            html.H2(["Prediction result of the hematologic malignancy driver gene prediction model using each of the 14 study groups"], style={'textAlign': 'center'}),
            # Main panel layout
            dbc.Row([
                dash_table.DataTable(id='prediction_cohort_wise',
                                     columns=[{'name': col, 'id': col} for col in prediction_strudy_group.columns],
                                     data=prediction_strudy_group.to_dict('records'),
                                     page_size=10,  # Show 10 rows per page
                                     sort_action='native',  # Enable column sorting
                                     filter_action='native',  # Enable built-in filtering
                                     style_table={'height': '400px', 'overflowY': 'auto'},
                                     export_format='csv',
                                     )
            ], ),

        ], ),
    ], ),

])



