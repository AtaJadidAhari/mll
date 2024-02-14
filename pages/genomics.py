import dash
from dash import dcc, html, dash_table, callback
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
import plotly.io as pio


# Sample data
n_var_samp = pd.read_csv("./data/sup_table/n_var_samp_tab.csv", sep=',')

n_var_gene_tab = pd.read_csv("./data/sup_table/n_var_gene_tab.csv", sep=',')

n_var_vep_tab = pd.read_csv("./data/sup_table/n_var_vep_tab.csv", sep=',')

intogen_resource_tab = pd.read_csv("./data/resource_table/intogen_resource_tab.csv", sep=',').drop(['Entity'], axis=1)

fusion_agg_tab = pd.read_csv("./data/agg_table/fusion_agg_tab.csv", sep=',')

absplice_agg_tab = pd.read_csv("./data/agg_table/absplice_agg_tab.csv", sep=",")

absplice_ratio_tab = pd.read_csv("./data/agg_table/absplice_ratio_tab.csv", sep=",")

absplice_resource_tab = pd.read_csv("./data/resource_table/absplice_resource_tab.csv", sep=',').drop(['Study group'], axis=1)

manuscript_wording = pd.read_csv("./data/leukemie_driver_manuscript_wording-sample_annotation.tsv", sep="\t")
manuscript_wording = manuscript_wording.drop(
    ["Cohort during analysis", "Cohort German abbreviation", "Study group during analysis", "Number of samples per study group", "Number of samples per cohort"], axis=1)

manuscript_wording = manuscript_wording.rename(columns={"Cohort": "Disease entity",
                                                        "Cohort abbreviation": "Abbreviation",
                                                        "Number of sampples per cohort": "Number of samples per disease entity", })
study_group_mapping_dict = manuscript_wording.set_index('Abbreviation')['Study group'].to_dict()
study_group_mapping_dict['Total'] = 'Total'

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
                             export_format='csv',
                             )
    ]),
    
    # Number of filtered variants per sample
    dbc.Card([
        dbc.Row([
            html.H2(["Number of filtered variants per sample"], style={'textAlign': 'center'}),

            # Sidebar layout
            dbc.Col([
                dcc.Dropdown(
                    id='drop_down_n_var_samp',
                    options=[{'label': group, 'value': group} for group in np.unique(n_var_samp['DiseaseEntity'])],
                    value='AML',
                    multi=False
                ),
            ], width=4),

            # Main panel layout
            dbc.Row([
                dcc.Graph(id='n_var_samp_histogram'),
                dash_table.DataTable(id='n_var_samp_table',
                                     columns=[{'name': col, 'id': col} for col in n_var_samp.columns],
                                     data=n_var_samp.to_dict('records'),
                                     page_size=10,  # Show 10 rows per page
                                     sort_action='native',  # Enable column sorting
                                     filter_action='native',  # Enable built-in filtering
                                     style_table={'height': '300px', 'overflowY': 'auto'},
                                     export_format='csv',
                                     )
            ], ),

        ], ),
    ], ),

    # Number of filtered variants per gene
    dbc.Card([
        dbc.Row([
            html.H2(["Number of filtered variants aggregated by disease entities and genes"],
                    style={'textAlign': 'center'}),

            # Sidebar layout
            dbc.Col([
                dcc.Dropdown(
                    id='drop_down_n_var_gene',
                    options=[{'label': group, 'value': group} for group in n_var_gene_tab['GeneSymbol']],
                    value='EYS',
                    multi=False
                ),
            ], width=4),

            # Main panel layout
            dbc.Row([
                dcc.Graph(id='n_var_gene_histogram'),
                dash_table.DataTable(id='n_var_gene_table',
                                     columns=[{'name': col, 'id': col} for col in n_var_gene_tab.columns],
                                     data=n_var_gene_tab.to_dict('records'),
                                     page_size=10,  # Show 10 rows per page
                                     sort_action='native',  # Enable column sorting
                                     filter_action='native',  # Enable built-in filtering
                                     style_table={'height': '300px', 'overflowY': 'auto'},
                                     export_format='csv',
                                     )
            ], ),

        ], ),
    ], ),

    # Number of filtered variants vep
    dbc.Card([
        dbc.Row([
            html.H2(["Number of filtered variants aggregated by disease entities and genes and VEP consequences"],
                    style={'textAlign': 'center'}),

            # Sidebar layout
            dbc.Col([
                dcc.Dropdown(
                    id='drop_down_n_var_vep_gene',
                    options=[{'label': group, 'value': group} for group in n_var_vep_tab['GeneSymbol']],
                    value='MMRN1',
                    multi=False
                ),
            ], width=4),
            dbc.Col([
                dcc.Dropdown(
                    id='drop_down_n_var_vep_consequence',
                    multi=False
                ),
            ], width=4),

            # Main panel layout
            dbc.Row([
                dcc.Graph(id='n_var_vep_histogram'),
                dash_table.DataTable(id='n_var_vep_table',
                                     columns=[{'name': col, 'id': col} for col in n_var_vep_tab.columns],
                                     data=n_var_vep_tab.to_dict('records'),
                                     page_size=10,  # Show 10 rows per page
                                     sort_action='native',  # Enable column sorting
                                     filter_action='native',  # Enable built-in filtering
                                     style_table={'height': '300px', 'overflowY': 'auto'},
                                     export_format='csv',
                                     )
            ], ),

        ], ),
    ], ),

    # abSplice
    dbc.Card([
        dbc.Row([
            html.H2(["AbSplice-DNA"], ),
            html.H4(["Number of splice-affecting variants aggregated by disease entities and genes"], ),

            # Sidebar layout
            dbc.Col([
                dcc.Dropdown(
                    id='absplice_dropdown',
                    options=[{'label': gene, 'value': gene} for gene in absplice_agg_tab['GeneSymbol']],
                    value='MGMT',
                    multi=False
                ),
            ], width=4),

            # Main panel layout
            dbc.Row([
                dcc.Graph(id='absplice_agg_tab_histogram'),
                dash_table.DataTable(id='absplice_agg_tab',
                                     columns=[{'name': col, 'id': col} for col in absplice_agg_tab.columns],
                                     data=absplice_agg_tab.to_dict('records'),
                                     page_size=10,  # Show 10 rows per page
                                     sort_action='native',  # Enable column sorting
                                     filter_action='native',  # Enable built-in filtering
                                     style_table={'height': '300px', 'overflowY': 'auto'},
                                     export_format='csv',
                                     )
            ], ),
            dbc.Row([
                html.H4(["Number of splice-affecting variants per gene per entity when applying different filters"], ),
                dash_table.DataTable(id='activation resource table',
                                     columns=[{'name': col, 'id': col} for col in absplice_resource_tab.columns],
                                     data=absplice_resource_tab.to_dict('records'),
                                     page_size=10,  # Show 10 rows per page
                                     sort_action='native',  # Enable column sorting
                                     filter_action='native',  # Enable built-in filtering
                                     style_table={'height': '80%', 'overflowY': 'auto'},
                                     export_format='csv',

                                     )
            ], ),

        ], ),
    ], ),

    # abSplice ratio
    dbc.Card([
        html.H2([
            "AbSplice-DNA"], ),
        html.H4([
            "Fraction of splice-affecting variants within filtered variants aggregated by disease entities and genes"], ),
        # Sidebar layout
        dbc.Col([
            dcc.Dropdown(
                id='absplice_ratio_dropdown',
                options=[{'label': gene, 'value': gene} for gene in absplice_ratio_tab['GeneSymbol']],
                value='UROD',
                multi=False
            ),
        ], width=4),

        dbc.Row([
            dcc.Graph(id='absplice_ratio_tab_histogram'),
            dbc.Col(
                dash_table.DataTable(id='absplice_ratio_tab',
                                     columns=[{'name': col, 'id': col} for col in absplice_ratio_tab.columns],
                                     data=absplice_ratio_tab.to_dict('records'),
                                     page_size=10,  # Show 10 rows per page
                                     sort_action='native',  # Enable column sorting
                                     filter_action='native',  # Enable built-in filtering
                                     style_table={'height': '300px', 'overflowY': 'auto'},
                                     export_format='csv',
                                     )
            )
        ], ),
    ], ),
    
    # Intogen 7 tools
    dbc.Card([
        dbc.Row([
            html.H2(["Driver prediction results from intOGen 7 tools"], style={'textAlign': 'center'}),
            # Main panel layout
            dbc.Row([
                dash_table.DataTable(id='intogen_resource_tab',
                                     columns=[{'name': col, 'id': col} for col in intogen_resource_tab.columns],
                                     data=intogen_resource_tab.to_dict('records'),
                                     page_size=10,  # Show 10 rows per page
                                     sort_action='native',  # Enable column sorting
                                     filter_action='native',  # Enable built-in filtering
                                     style_table={'height': '400px', 'overflowY': 'auto'},
                                     export_format='csv',
                                     )
            ], ),

        ], ),
    ], ),
    
     # Fusion
    dbc.Card([
        dbc.Row([
            html.H2(["Fusion events aggregated by disease entities and genes"], style={'textAlign': 'center'}),

            # Sidebar layout
            dbc.Col([
                dcc.Dropdown(
                    id='gene_dropdown_fusion',
                    options=[{'label': gene, 'value': gene} for gene in fusion_agg_tab['Gene_pair']],
                    value='ARHGAP26--NR3C1',
                    multi=False
                ),
            ], width=4),

            # Main panel layout
            dbc.Row([
                dcc.Graph(id='fusion_agg_tab_histogram'),
                dash_table.DataTable(id='fusion_agg_table',
                                     columns=[{'name': col, 'id': col} for col in fusion_agg_tab.columns],
                                     data=fusion_agg_tab.to_dict('records'),
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


@callback(
    Output('drop_down_n_var_vep_consequence', 'options'),
    Output('drop_down_n_var_vep_consequence', 'value'),
    Input('drop_down_n_var_vep_gene', 'value')
)
def update_dropdown_category2(selected_gene):
    # Get available options based on the selected value of the first dropdown
    options = [{'label': group, 'value': group} for group in
               np.unique(n_var_vep_tab[n_var_vep_tab['GeneSymbol'] == selected_gene]['Consequence'])],
    # Set the default value to the first option
    default_value = options[0][0]['value']
    return options[0], default_value


@callback(
    Output('n_var_samp_histogram', 'figure'),
    [Input('drop_down_n_var_samp', 'value')]
)
def update_n_var_sample_histogram(selected_cohort):
    cohort_data_subset = n_var_samp[n_var_samp['DiseaseEntity'] == selected_cohort]
    fig = px.scatter(cohort_data_subset, y='Number_of_variant', x="AnonamizedID",
                     labels={'Number_of_variant': 'Number of variants'},
                     ).update_layout(template="plotly_white").update_xaxes(autorange="reversed")
    return fig


@callback(
    Output('n_var_gene_histogram', 'figure'),
    [Input('drop_down_n_var_gene', 'value')]
)
def update__n_var_gene_histogram(selected_gene):
    gene_data_subset = n_var_gene_tab[n_var_gene_tab['GeneSymbol'] == selected_gene]
    melted_df = gene_data_subset.melt(id_vars=['GeneSymbol'], value_vars=gene_data_subset.columns[2:],
                                      var_name='Disease entity',
                                      value_name='Number of variants')
    melted_df['Study group'] = melted_df['Disease entity'].map(study_group_mapping_dict)
    fig = px.bar(melted_df, x='Disease entity', y='Number of variants', color='Study group',
                 )
    fig.update_traces(width=1).update_layout(template="plotly_white")
    return fig


@callback(
    Output('n_var_vep_histogram', 'figure'),
    [Input('drop_down_n_var_vep_gene', 'value'),
     Input('drop_down_n_var_vep_consequence', 'value')]
)
def update_n_var_vep_histogram(selected_gene, consequence):
    gene_data_subset = n_var_vep_tab[
        (n_var_vep_tab['GeneSymbol'] == selected_gene) & (n_var_vep_tab['Consequence'] == consequence)]
    melted_df = gene_data_subset.melt(id_vars=['GeneSymbol'], value_vars=gene_data_subset.columns[4:],
                                      var_name='Disease entity',
                                      value_name='Number of variants')
    melted_df['Study group'] = melted_df['Disease entity'].map(study_group_mapping_dict)
    fig = px.bar(melted_df, x='Disease entity', y='Number of variants', color='Study group',
                 )
    fig.update_traces(width=1).update_layout(template="plotly_white")
    return fig
    
    
@callback(
    Output('fusion_agg_tab_histogram', 'figure'),
    [Input('gene_dropdown_fusion', 'value')]
)
def update_fusion_histogram(selected_gene):
    gene_data_subset = fusion_agg_tab[fusion_agg_tab['Gene_pair'] == selected_gene]
    melted_df = pd.melt(gene_data_subset,
                          id_vars=['Gene_pair', 'GeneID_1', 'GeneSymbol_1', 'GeneID_2', 'GeneSymbol_2'],
                          var_name='Disease entity',
                          value_name='Gene Expression')
    melted_df['Study group'] = melted_df['Disease entity'].map(study_group_mapping_dict)
    fig = px.bar(melted_df, x='Disease entity', y='Gene Expression', color='Study group',
                 labels={'Gene Expression': 'Number of samples'},
                 barmode='group')
    fig.update_traces(width=1).update_layout(template="plotly_white")
    return fig

@callback(
    Output('absplice_agg_tab_histogram', 'figure'),
    [Input('absplice_dropdown', 'value')]
)
def update_absplice_histogram(selected_gene):
    gene_data_subset = absplice_agg_tab[absplice_agg_tab['GeneSymbol'] == selected_gene]
    melted_df = pd.melt(gene_data_subset, id_vars=['GeneID', 'GeneSymbol'], var_name='Disease entity',
                          value_name='Number of samples')
    melted_df['Study group'] = melted_df['Disease entity'].map(study_group_mapping_dict)
    fig = px.bar(melted_df, x='Disease entity', y='Number of samples', color='Study group',
                 barmode='group')
    fig.update_traces(width=1).update_layout(template="plotly_white")
    return fig


@callback(
    Output('absplice_ratio_tab_histogram', 'figure'),
    [Input('absplice_ratio_dropdown', 'value')]
)
def update_absplice_histogram(selected_gene):
    gene_data_subset = absplice_ratio_tab[absplice_ratio_tab['GeneSymbol'] == selected_gene]
    melted_df = pd.melt(gene_data_subset, id_vars=['GeneID', 'GeneSymbol'], var_name='Disease entity',
                          value_name='Ratio')
    melted_df['Study group'] = melted_df['Disease entity'].map(study_group_mapping_dict)
    fig = px.bar(melted_df, x='Disease entity', y='Ratio', color='Study group',
                 barmode='group')
    fig.update_traces(width=1).update_layout(template="plotly_white")
    return fig

