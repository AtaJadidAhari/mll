import dash
from dash import dcc, html, dash_table, callback
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
import plotly.io as pio

or_dn_agg_tab = pd.read_csv("./data/agg_table/or_dn_agg_tab.csv", sep=",")

or_up_agg_tab = pd.read_csv("./data/agg_table/or_up_agg_tab.csv", sep=",")

fraser_agg_tab = pd.read_csv("./data/agg_table/fraser_agg_tab.csv", sep=",")

activation_agg_tab = pd.read_csv("./data/agg_table/activation_agg_tab.csv", sep=",")

fkpm_agg_tab = pd.read_csv("./data/sup_table/fpkm_tab.csv", sep=',')

activation_resource_tab = pd.read_csv("./data/resource_table/activation_resource_tab.csv", sep=',').drop(['Study group'], axis=1)
fraser_resource_tab = pd.read_csv("./data/resource_table/fraser_resource_tab.csv", sep=',').drop(['Study group'], axis=1)
or_up_resource_tab = pd.read_csv("./data/resource_table/or_up_resource_tab.csv", sep=',').drop(['Study group'], axis=1)
or_dn_resource_tab = pd.read_csv("./data/resource_table/or_dn_resource_tab.csv", sep=',').drop(['Study group'], axis=1)

manuscript_wording = pd.read_csv("./data/leukemie_driver_manuscript_wording-sample_annotation.tsv", sep="\t")
manuscript_wording = manuscript_wording.drop(
    ["Cohort during analysis", "Cohort German abbreviation", "Study group during analysis",
     "Number of samples per study group", "Number of samples per cohort"], axis=1)

manuscript_wording = manuscript_wording.rename(columns={"Cohort": "Disease entity",
                                                        "Cohort abbreviation": "Abbreviation",
                                                        "Number of sampples per cohort": "Number of samples per disease entity", })
study_group_mapping_dict = manuscript_wording.set_index('Abbreviation')['Study group'].to_dict()
study_group_mapping_dict['Total'] = 'Total'

dash.register_page(__name__)

layout = html.Div([

    dbc.Card([
        html.H2(["Abbreviation table"], ),
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

    # Mean FPKM
    dbc.Card([
        dbc.Row([
            html.H2(["Mean FPKM matrix aggregated by disease entities and genes"], ),

            # Sidebar layout
            dbc.Col([
                dcc.Dropdown(
                    id='drop_down_fpkm',
                    options=[{'label': group, 'value': group} for group in fkpm_agg_tab['GeneSymbol']],
                    value='TSPAN6',
                    multi=False
                ),
            ], width=4),

            # Main panel layout
            dbc.Row([
                dcc.Graph(id='fpkm_histogram'),
                dash_table.DataTable(id='fpkm_table',
                                     columns=[{'name': col, 'id': col} for col in fkpm_agg_tab.columns],
                                     data=fkpm_agg_tab.to_dict('records'),
                                     page_size=10,  # Show 10 rows per page
                                     sort_action='native',  # Enable column sorting
                                     filter_action='native',  # Enable built-in filtering
                                     style_table={'height': '300px', 'overflowY': 'auto'},
                                     export_format='csv',
                                     ),
            ], ),

        ], ),
    ], ),

    # or_dn aggregated table
    dbc.Card([
        dbc.Row([
            html.H2(["OUTRIDER"]),
            html.H4(["Number of  underexpression outliers aggregated by disease entities and genes"], ),
            # Sidebar layout
            dbc.Col([
                dcc.Dropdown(
                    id='or_dn_dropdown',
                    options=[{'label': gene, 'value': gene} for gene in or_dn_agg_tab['GeneSymbol']],
                    value='PLP2',
                    multi=False
                ),
            ], width=4),

            # Main panel layout

            dcc.Graph(id='or_dn_histogram'),
            dbc.Col([
                dash_table.DataTable(id='or_dn aggregated table',
                                     columns=[{'name': col, 'id': col} for col in or_dn_agg_tab.columns],
                                     data=or_dn_agg_tab.to_dict('records'),
                                     page_size=10,  # Show 10 rows per page
                                     sort_action='native',  # Enable column sorting
                                     filter_action='native',  # Enable built-in filtering
                                     style_table={'height': '80%', 'overflowY': 'auto'},
                                     export_format='csv',

                                     )
            ], ),
            dbc.Col([
                html.H4(["Number of underexpression outliers per gene per entity when applying different filters"], ),
                dash_table.DataTable(id='or_dn resource table',
                                     columns=[{'name': col, 'id': col} for col in or_dn_resource_tab.columns],
                                     data=or_dn_resource_tab.to_dict('records'),
                                     page_size=10,  # Show 10 rows per page
                                     sort_action='native',  # Enable column sorting
                                     filter_action='native',  # Enable built-in filtering
                                     style_table={'height': '80%', 'overflowY': 'auto'},
                                     export_format='csv',

                                     )
            ], ),
        ], style={'justify': 'center', }),
    ], ),

    # or_up aggregated table
    dbc.Card([
        dbc.Row([
            html.H2(["OUTRIDER"], ),
            html.H4(["Number of  overexpression outliers aggregated by disease entities and genes"], ),
            # Sidebar layout
            dbc.Col([
                dcc.Dropdown(
                    id='or_up_dropdown',
                    options=[{'label': gene, 'value': gene} for gene in or_up_agg_tab['GeneSymbol']],
                    value='KIF27',
                    multi=False
                ),
            ], width=4),

            # Main panel layout

            dcc.Graph(id='or_up_histogram'),
            dbc.Col([
                dash_table.DataTable(id='or_up aggregated table',
                                     columns=[{'name': col, 'id': col} for col in or_up_agg_tab.columns],
                                     data=or_up_agg_tab.to_dict('records'),
                                     page_size=10,  # Show 10 rows per page
                                     sort_action='native',  # Enable column sorting
                                     filter_action='native',  # Enable built-in filtering
                                     style_table={'height': '80%', 'overflowY': 'auto'},
                                     export_format='csv',
                                     )
            ], ),
            dbc.Col([
                html.H4(["Number of overexpression outliers per gene per entity when applying different filters"], ),
                dash_table.DataTable(id='or_up resource table',
                                     columns=[{'name': col, 'id': col} for col in or_up_resource_tab.columns],
                                     data=or_up_resource_tab.to_dict('records'),
                                     page_size=10,  # Show 10 rows per page
                                     sort_action='native',  # Enable column sorting
                                     filter_action='native',  # Enable built-in filtering
                                     style_table={'height': '80%', 'overflowY': 'auto'},
                                     export_format='csv',

                                     )
            ], ),

        ], style={'justify': 'center', }),
    ], ),

    # activation
    dbc.Card([
        dbc.Row([
            html.H2(["NB-act"], ),
            html.H4(["Number of activation outliers aggregated by disease entities and genes"], ),
            # Sidebar layout
            dbc.Col([
                dcc.Dropdown(
                    id='gene_dropdown_activation',
                    options=[{'label': gene, 'value': gene} for gene in activation_agg_tab['GeneSymbol']],
                    value='KCNS3',
                    multi=False
                ),
            ], width=4),

            # Main panel layout
            dbc.Row([
                dcc.Graph(id='activation_agg_tab_histogram'),
                dash_table.DataTable(id='ctivation_agg_table',
                                     columns=[{'name': col, 'id': col} for col in activation_agg_tab.columns],
                                     data=activation_agg_tab.to_dict('records'),
                                     page_size=10,  # Show 10 rows per page
                                     sort_action='native',  # Enable column sorting
                                     filter_action='native',  # Enable built-in filtering
                                     style_table={'height': '300px', 'overflowY': 'auto'},
                                     export_format='csv',
                                     )
            ], ),
            dbc.Row([
                html.H4(["Number of activation outliers per gene per entity when applying different filters"], ),
                dash_table.DataTable(id='activation resource table',
                                     columns=[{'name': col, 'id': col} for col in activation_resource_tab.columns],
                                     data=activation_resource_tab.to_dict('records'),
                                     page_size=10,  # Show 10 rows per page
                                     sort_action='native',  # Enable column sorting
                                     filter_action='native',  # Enable built-in filtering
                                     style_table={'height': '80%', 'overflowY': 'auto'},
                                     export_format='csv',

                                     )
            ], ),
        ], ),
    ], ),

    # Fraser
    dbc.Card([
        dbc.Row([
            html.H2(["FRASER"], ),
            html.H4(["Number of splicing outliers aggregated by disease entities and genes"], ),

            # Sidebar layout
            dbc.Col([
                dcc.Dropdown(
                    id='gene_dropdown_fraser',
                    options=[{'label': gene, 'value': gene} for gene in fraser_agg_tab['GeneSymbol']],
                    value='UBC',
                    multi=False
                ),
            ], width=4),

            # Main panel layout
            dbc.Row([

                dcc.Graph(id='fraser_agg_tab_histogram'),
                dash_table.DataTable(id='fraser_table',
                                     columns=[{'name': col, 'id': col} for col in fraser_agg_tab.columns],
                                     data=fraser_agg_tab.to_dict('records'),
                                     page_size=10,  # Show 10 rows per page
                                     sort_action='native',  # Enable column sorting
                                     filter_action='native',  # Enable built-in filtering
                                     style_table={'height': '300px', 'overflowY': 'auto'},
                                     export_format='csv',
                                     )
            ], ),
            dbc.Row([
                html.H4(["Number of splicing outliers per gene per entity when applying different filters"], ),
                dash_table.DataTable(id='activation resource table',
                                     columns=[{'name': col, 'id': col} for col in fraser_resource_tab.columns],
                                     data=fraser_resource_tab.to_dict('records'),
                                     page_size=10,  # Show 10 rows per page
                                     sort_action='native',  # Enable column sorting
                                     filter_action='native',  # Enable built-in filtering
                                     style_table={'height': '80%', 'overflowY': 'auto'},
                                     export_format='csv',

                                     )
            ], ),
        ], ),
    ], ),

])


@callback(
    Output('fpkm_histogram', 'figure'),
    [Input('drop_down_fpkm', 'value')]
)
def update_fpkm_histogram(selected_gene):
    gene_data_subset = fkpm_agg_tab[fkpm_agg_tab['GeneSymbol'] == selected_gene]
    melted_df = gene_data_subset.melt(id_vars=['GeneSymbol'], value_vars=gene_data_subset.columns[2:],
                                      var_name='Disease entity',
                                      value_name='FPKM expression')
    melted_df['Study group'] = melted_df['Disease entity'].map(study_group_mapping_dict)
    fig = px.bar(melted_df, x='Disease entity', y='FPKM expression', color='Study group',
                 )
    fig.update_traces(width=1).update_layout(template="plotly_white")
    return fig


@callback(
    Output('or_dn_histogram', 'figure'),
    [Input('or_dn_dropdown', 'value')]
)
def update_or_dn_histogram(selected_gene):
    gene_data_subset = or_dn_agg_tab[or_dn_agg_tab['GeneSymbol'] == selected_gene]
    melted_df = pd.melt(gene_data_subset, id_vars=['GeneID', 'GeneSymbol'], var_name='Disease entity',
                          value_name='Number of samples')
    melted_df['Study group'] = melted_df['Disease entity'].map(study_group_mapping_dict)
    fig = px.bar(melted_df, x='Disease entity', y='Number of samples', color='Study group',
                 barmode='group',
                 )
    fig.update_traces(width=1).update_layout(template="plotly_white")
    return fig


@callback(
    Output('or_up_histogram', 'figure'),
    [Input('or_up_dropdown', 'value')]
)
def update_or_up_histogram(selected_gene):
    gene_data_subset = or_up_agg_tab[or_up_agg_tab['GeneSymbol'] == selected_gene]
    melted_df = pd.melt(gene_data_subset, id_vars=['GeneID', 'GeneSymbol'], var_name='Disease entity',
                          value_name='Number of samples')
    melted_df['Study group'] = melted_df['Disease entity'].map(study_group_mapping_dict)
    fig = px.bar(melted_df, x='Disease entity', y='Number of samples', color='Study group',
                 barmode='group',
                 )
    fig.update_traces(width=1).update_layout(template="plotly_white")
    return fig


@callback(
    Output('activation_agg_tab_histogram', 'figure'),
    [Input('gene_dropdown_activation', 'value')]
)
def update_activation_histogram(selected_gene):
    gene_data_subset = activation_agg_tab[activation_agg_tab['GeneSymbol'] == selected_gene]
    melted_df = pd.melt(gene_data_subset, id_vars=['GeneID', 'GeneSymbol'], var_name='Disease entity',
                          value_name='Number of samples')
    melted_df['Study group'] = melted_df['Disease entity'].map(study_group_mapping_dict)
    fig = px.bar(melted_df, x='Disease entity', y='Number of samples', color='Study group',
                 barmode='group')
    fig.update_traces(width=1).update_layout(template="plotly_white")
    return fig


@callback(
    Output('fraser_agg_tab_histogram', 'figure'),
    [Input('gene_dropdown_fraser', 'value')]
)
def update_fraser_histogram(selected_gene):
    gene_data_subset = fraser_agg_tab[fraser_agg_tab['GeneSymbol'] == selected_gene]
    melted_df = pd.melt(gene_data_subset, id_vars=['GeneID', 'GeneSymbol'], var_name='Disease entity',
                          value_name='Number of samples')
    melted_df['Study group'] = melted_df['Disease entity'].map(study_group_mapping_dict)
    fig = px.bar(melted_df, x='Disease entity', y='Number of samples', color='Study group',
                 barmode='group')
    fig.update_traces(width=1).update_layout(template="plotly_white")
    return fig
