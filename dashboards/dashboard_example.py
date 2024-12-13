from squirrels import DashboardArgs, dashboards as d
from matplotlib import pyplot as plt, figure as f, axes as a
import io
import base64
import pandas as pd
import plotly.express as px
from smaller_inference_LLM_model import generate_response_with_patient_data

async def main(sqrl: DashboardArgs) -> d.HtmlDashboard:
    """
    Create a dashboard by retrieving datasets using "sqrl.dataset" method and transform the datasets to return as a PngDashboard or a HtmlDashboard.
    - The PngDashboard constructor takes a single argument for either a matplotlib.figure.Figure or io.BytesIO/bytes of PNG data
    - The HtmlDashboard constructor takes a single argument for a io.StringIO/string of HTML data

    It is imperative to set the correct return type in the function signature for "main" above! It allows Squirrels to provide the correct format to
    the data catalog without having to run this function.
    """
    
    raw_dataset = await sqrl.dataset("overview_dataset_dash")
    
    df = pd.DataFrame(raw_dataset)
    
    print(df)
    
    prompt = str(df["Prompt"][0])
    condition = str(df["Condition"][0])
    del df["Prompt"] 
    # Identify potential categorical columns
    categorical_cols = [col for col in df.columns if col not in ['total_count', 'date']]

    df['date'] = pd.to_datetime(df['date'])
    # Aggregate by month
    df['Month'] = df['date'].dt.to_period('M')
    del df['date']
    
    df_monthly = df.groupby(['Month'] + categorical_cols).sum().reset_index()
    df_monthly['Month'] = df_monthly['Month'].dt.to_timestamp()  # Convert Period to Timestamp for plotting
    
    print(df_monthly)
    
    # Create the plot
    fig = px.line(
        df_monthly,
        x='Month',
        y='total_count',
        color=categorical_cols[0] if categorical_cols else None,  # Use the first categorical column if exists
        title='Monthly Aggregated Time Series for ' + condition,
        labels={'Month': 'Month', 'total_count': 'Total Count'}
    )

    # Show the plot
    # Export the combined figure as an interactive HTML string
    fig_html_string = fig.to_html(full_html=True, include_plotlyjs='cdn')
    
    df_monthly['Month'] = str(df_monthly['Month'])
    
    print(df_monthly.head(2).to_dict())
    print(prompt)
    
    response = generate_response_with_patient_data(prompt, df_monthly.head(50).to_dict())
    print(response)
    # Create the HTML content for the textbox
    description_html = f"""
    <div style="width: 80%; margin: 20px auto; text-align: center;">
        <p style="font-size: 16px; color: gray;">
            <b>AI Description:</b>
            <br>
            {response}
        </p>
    </div>
    """

    # Append the textbox HTML to the plotly-generated HTML
    final_html_string = fig_html_string.replace("</body>", f"{description_html}</body>")

    return d.HtmlDashboard(final_html_string)



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

