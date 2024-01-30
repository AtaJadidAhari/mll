import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash import dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
import plotly.io as pio

# Sample data
n_var_samp = pd.read_csv("./data/sup_table/n_var_samp_tab.csv", sep=',')

n_var_gene_tab = pd.read_csv("./data/sup_table/n_var_gene_tab.csv", sep=',')

n_var_vep_tab = pd.read_csv("./data/sup_table/n_var_vep_tab.csv", sep=',')

or_dn_agg_tab = pd.read_csv("./data/agg_table/or_dn_agg_tab.csv", sep=",")

or_up_agg_tab = pd.read_csv("./data/agg_table/or_up_agg_tab.csv", sep=",")

absplice_agg_tab = pd.read_csv("./data/agg_table/absplice_agg_tab.csv", sep=",")

absplice_ratio_tab = pd.read_csv("./data/agg_table/absplice_ratio_tab.csv", sep=",")

fraser_agg_tab = pd.read_csv("./data/agg_table/fraser_agg_tab.csv", sep=",")

activation_agg_tab = pd.read_csv("./data/agg_table/activation_agg_tab.csv", sep=",")

fusion_agg_tab = pd.read_csv("./data/agg_table/fusion_agg_tab.csv", sep=',')

fkpm_agg_tab = pd.read_csv("./data/sup_table/fpkm_tab.csv", sep=',')

sample_summary_tab = pd.read_csv("./data/agg_table/sample_summary_tab.csv", sep=',')

manuscript_wording = pd.read_csv("./data/leukemie_driver_manuscript_wording-sample_annotation.tsv", sep="\t")


def age_distribution():
    subset = sample_summary_tab.iloc[:, [0, 2, 3]]
    legend_names = {'Number_of_male': 'Male', 'Number_of_female': 'Female'}
    age_fig = px.bar(subset, x='DiseaseEntity', y=['Number_of_male', 'Number_of_female'],
                     labels={'value': 'Number of Individuals', 'variable': 'Gender'},
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
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Card([
        # html.H2(["MLL 5k project"]),
        html.H3(
            "Analysis of 3,760 hematologic malignancies reveals rare transcriptomic aberrations of driver genes.", ),
        html.A("https://doi.org/10.1101/2023.08.08.23293420", href="https://doi.org/10.1101/2023.08.08.23293420",
               target="_blank"),
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
                                     style_table={'height': '300px', 'overflowY': 'auto'}
                                     # Set table height and enable scrolling
                                     )
            ], ),

        ], ),
    ], ),

    # Number of filtered variants per gene
    dbc.Card([
        dbc.Row([
            html.H2(["Number of filtered variants per gene"], style={'textAlign': 'center'}),

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
                                     style_table={'height': '300px', 'overflowY': 'auto'}
                                     # Set table height and enable scrolling
                                     )
            ], ),

        ], ),
    ], ),

    # Number of filtered variants vep
    dbc.Card([
        dbc.Row([
            html.H2(["Number of filtered variants vep"], style={'textAlign': 'center'}),

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
                                     style_table={'height': '300px', 'overflowY': 'auto'}
                                     # Set table height and enable scrolling
                                     )
            ], ),

        ], ),
    ], ),

    # Mean FPKM
    dbc.Card([
        dbc.Row([
            html.H2(["Mean FPKM matrix aggregated by disease entities and genes"], style={'textAlign': 'center'}),

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
                                     style_table={'height': '300px', 'overflowY': 'auto'}
                                     # Set table height and enable scrolling
                                     )
            ], ),

        ], ),
    ], ),

    # Number of individuals, genders, and age
    dbc.Card([
        dbc.Row([
            html.H2(["Number of individuals, genders, and age groups aggregated by disease entities"],
                    style={'textAlign': 'center'}),

            # Sidebar layout
            dbc.Col([
                dcc.Dropdown(
                    id='drop_down_age',
                    options=[{'label': group, 'value': group} for group in sample_summary_tab['DiseaseEntity']],
                    value='AML',
                    multi=False
                ),
            ], width=4),

            # Main panel layout
            dbc.Row([
                dcc.Graph(id='sample_summary_histogram'),
                dcc.Graph(
                    id='age_bar_plot',
                    figure=age_distribution()
                ),
                dash_table.DataTable(id='sample_summary_table',
                                     columns=[{'name': col, 'id': col} for col in sample_summary_tab.columns],
                                     data=sample_summary_tab.to_dict('records'),
                                     page_size=10,  # Show 10 rows per page
                                     sort_action='native',  # Enable column sorting
                                     filter_action='native',  # Enable built-in filtering
                                     style_table={'height': '300px', 'overflowY': 'auto'}
                                     # Set table height and enable scrolling
                                     )
            ], ),
        ], ),
    ], ),

    # or_dn aggregated table
    dbc.Card([
        dbc.Row([
            html.H2(["OUTRIDER: Number of  underexpression outliers aggregated by disease entities and genes"],
                    style={'textAlign': 'center', "margin-top": "20px", "margin-bottom": "20px"}),
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
                                     style_table={'height': '80%', 'overflowY': 'auto'}
                                     # Set table height and enable scrolling
                                     )
            ], ),
        ], style={'justify': 'center', }),
    ], ),

    # or_up aggregated table
    dbc.Card([
        dbc.Row([
            html.H2(["OUTRIDER: Number of  overexpression outliers aggregated by disease entities and genes"],
                    style={'textAlign': 'center', "margin-top": "20px", "margin-bottom": "20px"}),
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
                                     style_table={'height': '80%', 'overflowY': 'auto'}
                                     # Set table height and enable scrolling
                                     )
            ], ),
        ], style={'justify': 'center', }),
    ], ),

    # activation
    dbc.Card([
        dbc.Row([
            html.H2(["Number of activation outliers aggregated by disease entities and genes"],
                    style={'textAlign': 'center'}),

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
                                     style_table={'height': '300px', 'overflowY': 'auto'}
                                     # Set table height and enable scrolling
                                     )
            ], ),
        ], ),
    ], ),

    # Fraser
    dbc.Card([
        dbc.Row([
            html.H2(["FRASER: Number of  splicing outliers aggregated by disease entities and genes"],
                    style={'textAlign': 'center'}),

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
                                     style_table={'height': '300px', 'overflowY': 'auto'}
                                     # Set table height and enable scrolling
                                     )
            ], ),
        ], ),
    ], ),

    # abSplice
    dbc.Card([
        dbc.Row([
            html.H2(["AbSplice-DNA: Number of splice-affecting variants aggregated by disease entities and genes"],
                    style={'textAlign': 'center'}),

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
                                     style_table={'height': '300px', 'overflowY': 'auto'}
                                     # Set table height and enable scrolling
                                     )
            ], ),

        ], ),
    ], ),

    # abSplice ratio
    dbc.Card([
        html.H2([
                    "AbSplice-DNA: Fraction of splice-affecting variants within filtered variants aggregated by disease entities and genes"],
                style={'textAlign': 'center'}),
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
                                     style_table={'height': '300px', 'overflowY': 'auto'}
                                     # Set table height and enable scrolling
                                     )
            )
        ], ),
    ], ),

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
                                     style_table={'height': '300px', 'overflowY': 'auto'}
                                     # Set table height and enable scrolling
                                     )
            ], ),

        ], ),
    ], ),

    dbc.Card([
        html.H2(["Manuscript abbreviation table"], style={'textAlign': 'center'}),
        dash_table.DataTable(id='manuscript_wording_table',
                             columns=[{'name': col, 'id': col} for col in manuscript_wording.columns],
                             data=manuscript_wording.to_dict('records'),
                             page_size=10,  # Show 10 rows per page
                             sort_action='native',  # Enable column sorting
                             filter_action='native',  # Enable built-in filtering
                             style_table={'height': '300px', 'overflowY': 'auto'}
                             # Set table height and enable scrolling
                             )
    ]),

], )


@app.callback(
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


@app.callback(
    Output('n_var_samp_histogram', 'figure'),
    [Input('drop_down_n_var_samp', 'value')]
)
def update_n_var_sample_histogram(selected_gene):
    gene_data_subset = n_var_samp[n_var_samp['DiseaseEntity'] == selected_gene]
    fig = px.scatter(gene_data_subset, y='Number_of_variant', x="AnonamizedID",
                     labels={'Number_of_variant': 'Number of variants'},
                     ).update_layout(template="plotly_white").update_xaxes(autorange="reversed")
    return fig


@app.callback(
    Output('n_var_gene_histogram', 'figure'),
    [Input('drop_down_n_var_gene', 'value')]
)
def update__n_var_gene_histogram(selected_gene):
    gene_data_subset = n_var_gene_tab[n_var_gene_tab['GeneSymbol'] == selected_gene]
    melted_df = gene_data_subset.melt(id_vars=['GeneSymbol'], value_vars=gene_data_subset.columns[2:],
                                      var_name='Disease Entity',
                                      value_name='Number of variants')
    fig = px.bar(melted_df, x='Disease Entity', y='Number of variants', color='Disease Entity',
                 )
    fig.update_traces(width=1).update_layout(template="plotly_white")
    return fig


@app.callback(
    Output('n_var_vep_histogram', 'figure'),
    [Input('drop_down_n_var_vep_gene', 'value'),
     Input('drop_down_n_var_vep_consequence', 'value')]
)
def update_n_var_vep_histogram(selected_gene, consequence):
    gene_data_subset = n_var_vep_tab[
        (n_var_vep_tab['GeneSymbol'] == selected_gene) & (n_var_vep_tab['Consequence'] == consequence)]
    melted_df = gene_data_subset.melt(id_vars=['GeneSymbol'], value_vars=gene_data_subset.columns[4:],
                                      var_name='Disease Entity',
                                      value_name='Number of variants')
    fig = px.bar(melted_df, x='Disease Entity', y='Number of variants', color='Disease Entity',
                 )
    fig.update_traces(width=1).update_layout(template="plotly_white")
    return fig


@app.callback(
    Output('fpkm_histogram', 'figure'),
    [Input('drop_down_fpkm', 'value')]
)
def update_fpkm_histogram(selected_gene):
    gene_data_subset = fkpm_agg_tab[fkpm_agg_tab['GeneSymbol'] == selected_gene]
    melted_df = gene_data_subset.melt(id_vars=['GeneSymbol'], value_vars=gene_data_subset.columns[2:],
                                      var_name='Disease Entity',
                                      value_name='FPKM expression')
    fig = px.bar(melted_df, x='Disease Entity', y='FPKM expression', color='Disease Entity',
                 )
    fig.update_traces(width=1).update_layout(template="plotly_white")
    return fig


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


@app.callback(
    Output('or_dn_histogram', 'figure'),
    [Input('or_dn_dropdown', 'value')]
)
def update_or_dn_histogram(selected_gene):
    gene_data_subset = or_dn_agg_tab[or_dn_agg_tab['GeneSymbol'] == selected_gene]
    melted_data = pd.melt(gene_data_subset, id_vars=['GeneID', 'GeneSymbol'], var_name='Disease Type',
                          value_name='Gene Expression')

    fig = px.bar(melted_data, x='Disease Type', y='Gene Expression', color='Disease Type',
                 labels={'Gene Expression': 'Number of samples'},
                 barmode='group',
                 )
    fig.update_traces(width=1).update_layout(template="plotly_white")
    return fig


@app.callback(
    Output('or_up_histogram', 'figure'),
    [Input('or_up_dropdown', 'value')]
)
def update_or_up_histogram(selected_gene):
    gene_data_subset = or_up_agg_tab[or_up_agg_tab['GeneSymbol'] == selected_gene]
    melted_data = pd.melt(gene_data_subset, id_vars=['GeneID', 'GeneSymbol'], var_name='Disease Type',
                          value_name='Gene Expression')

    fig = px.bar(melted_data, x='Disease Type', y='Gene Expression', color='Disease Type',
                 labels={'Gene Expression': 'Number of samples'},
                 barmode='group',
                 )
    fig.update_traces(width=1).update_layout(template="plotly_white")
    return fig


@app.callback(
    Output('activation_agg_tab_histogram', 'figure'),
    [Input('gene_dropdown_activation', 'value')]
)
def update_activation_histogram(selected_gene):
    gene_data_subset = activation_agg_tab[activation_agg_tab['GeneSymbol'] == selected_gene]
    melted_data = pd.melt(gene_data_subset, id_vars=['GeneID', 'GeneSymbol'], var_name='Disease Type',
                          value_name='Gene Expression')

    fig = px.bar(melted_data, x='Disease Type', y='Gene Expression', color='Disease Type',
                 labels={'Gene Expression': 'Number of samples'},
                 barmode='group')
    fig.update_traces(width=1).update_layout(template="plotly_white")
    return fig


@app.callback(
    Output('fraser_agg_tab_histogram', 'figure'),
    [Input('gene_dropdown_fraser', 'value')]
)
def update_fraser_histogram(selected_gene):
    gene_data_subset = fraser_agg_tab[fraser_agg_tab['GeneSymbol'] == selected_gene]
    melted_data = pd.melt(gene_data_subset, id_vars=['GeneID', 'GeneSymbol'], var_name='Disease Type',
                          value_name='Gene Expression')

    fig = px.bar(melted_data, x='Disease Type', y='Gene Expression', color='Disease Type',
                 labels={'Gene Expression': 'Number of samples'},
                 barmode='group')
    fig.update_traces(width=1).update_layout(template="plotly_white")
    return fig


@app.callback(
    Output('absplice_agg_tab_histogram', 'figure'),
    [Input('absplice_dropdown', 'value')]
)
def update_absplice_histogram(selected_gene):
    gene_data_subset = absplice_agg_tab[absplice_agg_tab['GeneSymbol'] == selected_gene]
    melted_data = pd.melt(gene_data_subset, id_vars=['GeneID', 'GeneSymbol'], var_name='Disease Type',
                          value_name='Gene Expression')

    fig = px.bar(melted_data, x='Disease Type', y='Gene Expression', color='Disease Type',
                 labels={'Gene Expression': 'Number of samples'},
                 barmode='group')
    fig.update_traces(width=1).update_layout(template="plotly_white")
    return fig


@app.callback(
    Output('absplice_ratio_tab_histogram', 'figure'),
    [Input('absplice_ratio_dropdown', 'value')]
)
def update_absplice_histogram(selected_gene):
    gene_data_subset = absplice_ratio_tab[absplice_ratio_tab['GeneSymbol'] == selected_gene]
    melted_data = pd.melt(gene_data_subset, id_vars=['GeneID', 'GeneSymbol'], var_name='Disease Type',
                          value_name='Gene Expression')

    fig = px.bar(melted_data, x='Disease Type', y='Gene Expression', color='Disease Type',
                 labels={'Gene Expression': 'Number of samples'},
                 barmode='group')
    fig.update_traces(width=1).update_layout(template="plotly_white")
    return fig


@app.callback(
    Output('fusion_agg_tab_histogram', 'figure'),
    [Input('gene_dropdown_fusion', 'value')]
)
def update_fusion_histogram(selected_gene):
    gene_data_subset = fusion_agg_tab[fusion_agg_tab['Gene_pair'] == selected_gene]
    melted_data = pd.melt(gene_data_subset,
                          id_vars=['Gene_pair', 'GeneID_1', 'GeneSymbol_1', 'GeneID_2', 'GeneSymbol_2'],
                          var_name='Disease Type',
                          value_name='Gene Expression')

    fig = px.bar(melted_data, x='Disease Type', y='Gene Expression', color='Disease Type',
                 labels={'Gene Expression': 'Number of samples'},
                 barmode='group')
    fig.update_traces(width=1).update_layout(template="plotly_white")
    return fig


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
