import plotly.express as px
import plotly.graph_objects as go

def make_line_chart(df, x, y, color=None, title=None):
    fig = px.line(df, x=x, y=y, color=color, title=title)
    return fig

def make_bar_chart(df, x, y, color=None, title=None):
    fig = px.bar(df, x=x, y=y, color=color, title=title)
    return fig

def make_box_plot(df, x, y, color=None, title=None):
    fig = px.box(df, x=x, y=y, color=color, title=title)
    return fig

def make_violin_plot(df, x, y, color=None, title=None):
    fig = px.violin(df, x=x, y=y, color=color, box=True, points="all", title=title)
    return fig
