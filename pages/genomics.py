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


dash.register_page(__name__)


layout = html.Div([

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
def update_n_var_sample_histogram(selected_gene):
    gene_data_subset = n_var_samp[n_var_samp['DiseaseEntity'] == selected_gene]
    fig = px.scatter(gene_data_subset, y='Number_of_variant', x="AnonamizedID",
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
    fig = px.bar(melted_df, x='Disease entity', y='Number of variants', color='Disease entity',
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
    fig = px.bar(melted_df, x='Disease entity', y='Number of variants', color='Disease entity',
                 )
    fig.update_traces(width=1).update_layout(template="plotly_white")
    return fig
