from squirrels import DashboardArgs, dashboards as d
from matplotlib import pyplot as plt, figure as f, axes as a
import io
import base64
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer





async def main(sqrl: DashboardArgs) -> d.PngDashboard:
    """
    Create a dashboard by retrieving datasets using "sqrl.dataset" method and transform the datasets to return as a PngDashboard or a HtmlDashboard.
    - The PngDashboard constructor takes a single argument for either a matplotlib.figure.Figure or io.BytesIO/bytes of PNG data
    - The HtmlDashboard constructor takes a single argument for a io.StringIO/string of HTML data

    It is imperative to set the correct return type in the function signature for "main" above! It allows Squirrels to provide the correct format to
    the data catalog without having to run this function.
    """
    
    spending_by_month_df = await sqrl.dataset(
        "overview_dataset", fixed_parameters={"group_by": "g4"}
    )
    
    # Create a figure with two subplots
    fig, (ax0, ax1) = plt.subplots(2, 1, figsize=(8, 8), height_ratios=(1, 2))
    fig: f.Figure
    ax0: a.Axes
    ax1: a.Axes
    fig.tight_layout(pad=4, h_pad=6)

    # Create a bar chart of spending by month
    spending_by_month_df.sort_values("month").plot(x="month", y="total_amount", ax=ax0)
    ax0.set_title("Spending by Month")

    # Create a pie chart of spending by subcategory
    df_by_subcategory = spending_by_subcategory_df.set_index("subcategory").sort_values(
        "total_amount", ascending=False
    )
    autopct = lambda pct: ("%.1f%%" % pct) if pct > 6 else ""
    df_by_subcategory.plot(
        y="total_amount", kind="pie", ax=ax1, autopct=autopct, legend=False, ylabel=""
    )
    ax1.set_title("Spending by Subcategory")

    return d.PngDashboard(fig)



def generate_html_with_plot(plot, description):
    """
    Converts a pyplot plot and a description into an HTML string
    that displays the plot and its description.

    :param plot: A matplotlib.pyplot plot
    :param description: A string description of the plot
    :return: An HTML string
    """
    # Save the plot to a BytesIO buffer
    buf = io.BytesIO()
    plot.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)

    # Encode the image to base64
    encoded_image = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    # Create the HTML string
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Plot with Description</title>
    </head>
    <body>
        <h1>Plot</h1>
        <img src="data:image/png;base64,{encoded_image}" alt="Plot Image">
        <p>{description}</p>
    </body>
    </html>
    """
    return html_template

