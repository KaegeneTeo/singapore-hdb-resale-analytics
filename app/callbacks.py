import os
import pandas as pd
import mysql.connector
import plotly.express as px
from dash import Output, Input, dcc, html

# Database connection params (reuse from .env)
DB_PARAMS = dict(
    database=os.getenv("MYSQL_DATABASE", "mydb"),
    user=os.getenv("MYSQL_USER", "myuser"),
    password=os.getenv("MYSQL_PASSWORD", "mypass"),
    host=os.getenv("MYSQL_HOST", "localhost"),
    port=int(os.getenv("MYSQL_PORT", "3306")),
)

def fetch_resale_data():
    conn = mysql.connector.connect(**DB_PARAMS)
    query = "SELECT * FROM hdb_resale"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def register_callbacks(app):
    # Introduction Tab
    @app.callback(
        Output("intro-content", "children"),
        Input("intro-content", "id")
    )
    def update_intro(_):
        return html.Div([
            html.H3("Welcome to the Singapore HDB Resale Analytics Dashboard!"),
            html.P("""
                This dashboard provides a comprehensive analysis of HDB resale transactions in Singapore. 
                Explore trends over time, compare towns and flat types, and discover key insights about the resale market. 
                Use the tabs above to navigate through the story, from overall market trends to detailed breakdowns.
            """),
            html.Ul([
                html.Li("The HDB resale market has seen significant changes in transaction volume and price over the years."),
                html.Li("Price trends differ by flat type and town, reflecting diverse demand and supply factors."),
                html.Li("Some towns consistently lead in transaction volume and price per sqm."),
                html.Li("Flat type mix and price distributions reveal affordability and market segmentation.")
            ])
        ], style={"maxWidth": "800px", "margin": "auto"})

    # Overview Tab: Transactions per year and average price per year
    @app.callback(
        Output("overview-content", "children"),
        Input("overview-content", "id")
    )
    def update_overview(_):
        try:
            df = fetch_resale_data()
            df["year"] = pd.to_datetime(df["month"], errors="coerce").dt.year
            yearly = df.groupby("year").size().reset_index(name="transactions")
            avg_price = df.groupby("year")["resale_price"].mean().reset_index(name="avg_price")
            # Bar chart: transactions
            fig1 = px.bar(yearly, x="year", y="transactions", title="Total Resale Transactions per Year",
                          color="transactions", color_continuous_scale="Blues")
            # Line chart: average price
            fig2 = px.line(avg_price, x="year", y="avg_price", markers=True, title="Average Resale Price per Year",
                           line_shape="spline", color_discrete_sequence=["#FF5733"])
            fig2.update_traces(line_width=3)
            return html.Div([
                dcc.Graph(figure=fig1, style={"height": "350px"}),
                dcc.Graph(figure=fig2, style={"height": "350px"})
            ])
        except Exception as e:
            return f"Error loading data: {e}"

    # Price Trends Tab: Median price by month (line, colored by flat type), price distribution (box)
        # Town Analysis Tab: Top towns by transactions, median price per sqm by town
        @app.callback(
            Output("town-analysis-content", "children"),
            Input("town-analysis-content", "id")
        )
        def update_town_analysis(_):
            try:
                df = fetch_resale_data()
                # Top 10 towns by transaction count
                top_towns = df["town"].value_counts().nlargest(10).reset_index()
                top_towns.columns = ["town", "transactions"]
                fig1 = px.bar(top_towns, x="transactions", y="town", orientation="h",
                              title="Top 10 Towns by Transaction Count",
                              color="transactions", color_continuous_scale="Viridis")
                # Median price per sqm by town
                df["price_per_sqm"] = df["resale_price"] / df["floor_area_sqm"]
                med_price = df.groupby("town")["price_per_sqm"].median().reset_index()
                med_price = med_price.sort_values("price_per_sqm", ascending=False)
                fig2 = px.bar(med_price, x="town", y="price_per_sqm",
                              title="Median Price per Sqm by Town",
                              color="price_per_sqm", color_continuous_scale="Plasma")
                fig2.update_xaxes(tickangle=45)
                return html.Div([
                    dcc.Graph(figure=fig1, style={"height": "350px"}),
                    dcc.Graph(figure=fig2, style={"height": "350px"})
                ])
            except Exception as e:
                return f"Error loading data: {e}"

        # Flat Type Breakdown Tab: Pie chart and box plot
        @app.callback(
            Output("flat-type-breakdown-content", "children"),
            Input("flat-type-breakdown-content", "id")
        )
        def update_flat_type_breakdown(_):
            try:
                df = fetch_resale_data()
                df["price_per_sqm"] = df["resale_price"] / df["floor_area_sqm"]
                # Pie chart: proportion by flat type
                flat_counts = df["flat_type"].value_counts().reset_index()
                flat_counts.columns = ["flat_type", "count"]
                fig1 = px.pie(flat_counts, names="flat_type", values="count",
                              title="Proportion of Transactions by Flat Type",
                              color_discrete_sequence=px.colors.qualitative.Pastel)
                # Box plot: price per sqm by flat type
                fig2 = px.box(df, x="flat_type", y="price_per_sqm", color="flat_type",
                              title="Price per Sqm by Flat Type",
                              color_discrete_sequence=px.colors.qualitative.Pastel)
                return html.Div([
                    dcc.Graph(figure=fig1, style={"height": "350px"}),
                    dcc.Graph(figure=fig2, style={"height": "350px"})
                ])
            except Exception as e:
                return f"Error loading data: {e}"

        # Conclusion Tab
        @app.callback(
            Output("conclusion-content", "children"),
            Input("conclusion-content", "id")
        )
        def update_conclusion(_):
            return html.Div([
                html.H3("Conclusion: Key Insights from the HDB Resale Market"),
                html.P("""
                    The Singapore HDB resale market demonstrates dynamic trends across years, towns, and flat types. 
                    Transaction volumes and prices have evolved, with certain towns and flat types consistently leading in activity and value. 
                    Price per sqm and transaction mix highlight both affordability and premium segments in the market.
                """),
                html.Ul([
                    html.Li("Transaction volumes peaked in certain years, reflecting policy and market influences."),
                    html.Li("Average and median prices have generally increased, but with variation by flat type and town."),
                    html.Li("Towns like Tampines, Woodlands, and Jurong West are among the most active."),
                    html.Li("5-room and Executive flats command higher prices per sqm, but 4-room flats dominate in volume."),
                    html.Li("The market remains diverse, offering options for different budgets and needs.")
                ]),
                html.P("""
                    Use this dashboard to explore further and inform your understanding of Singapore's public housing market.
                """),
            ], style={"maxWidth": "800px", "margin": "auto"})
    @app.callback(
        Output("price-trends-content", "children"),
        Input("price-trends-content", "id")
    )
    def update_price_trends(_):
        try:
            df = fetch_resale_data()
            df["month"] = pd.to_datetime(df["month"], errors="coerce")
            # Median price by month and flat type
            medians = df.groupby(["month", "flat_type"])["resale_price"].median().reset_index()
            fig1 = px.line(medians, x="month", y="resale_price", color="flat_type",
                          title="Median Resale Price by Month and Flat Type",
                          color_discrete_sequence=px.colors.qualitative.Set2)
            fig1.update_traces(mode="lines+markers")
            # Box plot: resale price by flat type
            fig2 = px.box(df, x="flat_type", y="resale_price", points="outliers",
                          color="flat_type", title="Resale Price Distribution by Flat Type",
                          color_discrete_sequence=px.colors.qualitative.Set2)
            return html.Div([
                dcc.Graph(figure=fig1, style={"height": "350px"}),
                dcc.Graph(figure=fig2, style={"height": "350px"})
            ])
        except Exception as e:
            return f"Error loading data: {e}"
