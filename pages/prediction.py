import dash
from dash import dcc, html, dash_table, callback
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
import plotly.io as pio

prediction_complete = pd.read_csv("./data/prediction/S1_prediction_complete_dataset_desc.csv", sep=",")
prediction_complete['Prediction'] = prediction_complete['Prediction'].apply(lambda x: round(x, 3))

prediction_study_group = pd.read_csv("./data/prediction/S2_prediction_study_groups_desc.csv", sep=",")
prediction_study_group['Prediction'] = prediction_study_group['Prediction'].apply(lambda x: round(x, 3))

manuscript_wording = pd.read_csv("./data/leukemie_driver_manuscript_wording-sample_annotation.tsv", sep="\t")
manuscript_wording = manuscript_wording.drop(
    ["Cohort during analysis", "Cohort German abbreviation", "Study group during analysis",
     "Number of samples per study group", "Number of samples per cohort"], axis=1)

manuscript_wording = manuscript_wording.rename(columns={"Cohort": "Disease entity",
                                                        "Cohort abbreviation": "Abbreviation",
                                                        "Number of sampples per cohort": "Number of samples per disease entity", })


def plot_all_predictions():
    number_of_genes_to_plot = 50
    subset = prediction_complete.iloc[:number_of_genes_to_plot, ]
    age_fig = px.bar(subset, x='GeneSymbol', y='Prediction',
                     barmode='group').update_layout(template="plotly_white")
    return age_fig


dash.register_page(__name__)

layout = html.Div([

    dbc.Card([
        html.H2(["Abbreviation table"], style={'textAlign': 'center'}),
        dash_table.DataTable(id='manuscript_wording_table',
                             columns=[{'name': col, 'id': col} for col in manuscript_wording.columns],
                             data=manuscript_wording.to_dict('records'),
                             page_size=10,  # Show 10 rows per page
                             sort_action='native',  # Enable column sorting
                             filter_action='native',  # Enable built-in filtering
                             style_table={'height': '300px', 'overflowY': 'auto'},
                             style_cell={'textAlign': 'left'},
                             export_format='csv',
                             )
    ]),

    # Prediction all
    dbc.Card([
        dbc.Row([
            html.H2([
                        "Prediction result of the hematologic malignancy driver gene prediction model using the complete dataset"],
                    style={'textAlign': 'center'}),
            # Main panel layout
            dbc.Row([
                dcc.Graph(
                    id='all_predictions_plot',
                    figure=plot_all_predictions()
                ),
                dash_table.DataTable(id='prediction_all',
                                     columns=[{'name': col, 'id': col} for col in prediction_complete.columns],
                                     data=prediction_complete.to_dict('records'),
                                     page_size=10,  # Show 10 rows per page
                                     sort_action='native',  # Enable column sorting
                                     filter_action='native',  # Enable built-in filtering
                                     style_table={'height': '400px', 'overflowY': 'auto'},
                                     style_cell={'textAlign': 'left'},
                                     export_format='csv',
                                     )
            ], ),

        ], ),
    ], ),

    # Prediction cohort wise
    dbc.Card([
        dbc.Row([
            html.H2([
                        "Prediction result of the hematologic malignancy driver gene prediction model using each of the 14 study groups"],
                    style={'textAlign': 'center'}),
            # Main panel layout

            dbc.Row([

                # Sidebar layout
                dbc.Col([
                    dcc.Dropdown(
                        id='prediction_dropdown',
                        options=[{'label': group, 'value': group} for group in
                                 np.unique(prediction_study_group['StudyGroup'])],
                        value='AML',
                        multi=False
                    ),
                ], width=4),

                # Main panel layout

                dcc.Graph(id='cohort_wise_predictions_plot'),

                dash_table.DataTable(id='prediction_cohort_wise',
                                     columns=[{'name': col, 'id': col} for col in prediction_study_group.columns],
                                     data=prediction_study_group.to_dict('records'),
                                     page_size=10,  # Show 10 rows per page
                                     sort_action='native',  # Enable column sorting
                                     filter_action='native',  # Enable built-in filtering
                                     style_table={'height': '400px', 'overflowY': 'auto'},
                                     style_cell={'textAlign': 'left'},
                                     export_format='csv',
                                     )
            ], ),

        ], ),
    ], ),

])


@callback(
    Output('cohort_wise_predictions_plot', 'figure'),
    [Input('prediction_dropdown', 'value')]
)
def update_fpkm_histogram(selected_gene):
    gene_data_subset = prediction_study_group[prediction_study_group['StudyGroup'] == selected_gene]
    number_of_genes_to_plot = 50
    subset = gene_data_subset.iloc[:number_of_genes_to_plot, ]
    fig = px.bar(subset, x='GeneSymbol', y='Prediction',
                 barmode='group').update_layout(template="plotly_white")
    return fig
