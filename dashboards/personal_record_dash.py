import plotly.graph_objects as go
from squirrels import DashboardArgs, dashboards as d
import plotly.subplots as sp
from smaller_inference_LLM_model import generate_response_with_patient_data


# Define healthy ranges (simplified)
healthy_ranges = {
    "Systolic BP": (90, 120),
    "Diastolic BP": (60, 80),
    "Heart Rate": (60, 100),
    "BMI": (18.5, 24.9),
    "SpO2": (95, 100),
    "Creatinine": (0.5, 1.2),
    "CRP": (0, 1),
    "WBC Count": (4, 11),
    "Hemoglobin": (12, 16),
}

# Calculate deviations
def calculate_deviation(value, healthy_range):
    if value < healthy_range[0]:
        return healthy_range[0] - value
    elif value > healthy_range[1]:
        return value - healthy_range[1]
    return 0


async def main(sqrl: DashboardArgs) -> d.HtmlDashboard:
    """
    Create a dashboard by retrieving datasets using "sqrl.dataset" method and transform the datasets to return as a PngDashboard or a HtmlDashboard.
    - The PngDashboard constructor takes a single argument for either a matplotlib.figure.Figure or io.BytesIO/bytes of PNG data
    - The HtmlDashboard constructor takes a single argument for a io.StringIO/string of HTML data

    It is imperative to set the correct return type in the function signature for "main" above! It allows Squirrels to provide the correct format to
    the data catalog without having to run this function.
    """
    
    df = await sqrl.dataset("protected_dataset_dash")
    
    prompt = str(df.iloc[0,-1])
    
    print(prompt)
    
    df = df.iloc[[0], :-1]
    response = generate_response_with_patient_data(prompt, df.to_dict())
    
    # print(df)
    categories = list(healthy_ranges.keys())
    patient_values = df.loc[0, categories]  # Example: values for the first patient

    cleaned_fig = sp.make_subplots(
        rows=1,
        cols=len(categories),
        shared_xaxes=False,
        shared_yaxes=False,
        subplot_titles=categories,
    )

    # Add each metric to its own y-axis with clear range bands
    for i, metric in enumerate(categories):
        # Plot the healthy range as a filled band
        cleaned_fig.add_trace(
            go.Scatter(
                x=[0, 1],  # Dummy x-values for the shaded band
                y=[healthy_ranges[metric][1], healthy_ranges[metric][1]],
                mode="lines",
                line=dict(color="rgba(0, 255, 0, 0)"),
                name="",
                showlegend=(i == 0),  # Show legend only once
            ),
            row=1,
            col=i + 1,
        )
        cleaned_fig.add_trace(
            go.Scatter(
                x=[0, 1],  # Dummy x-values for the shaded band
                y=[healthy_ranges[metric][0], healthy_ranges[metric][0]],
                mode="lines",
                fill="tonexty",
                fillcolor="rgba(0, 255, 0, 0.2)",
                line=dict(color="rgba(0, 255, 0, 0)"),
                name="Healthy Range",
                showlegend=(i == 0),  # Show legend only once
            ),
            row=1,
            col=i + 1,
        )
        # Plot the patient value as a point
        cleaned_fig.add_trace(
            go.Scatter(
                x=[0.5],
                y=[patient_values[i]],
                mode="markers",
                name=f"Patient: {df.loc[0, 'Name']}",
                marker=dict(size=10, color="red"),
                showlegend=(i == 0),  # Show legend only once
            ),
            row=1,
            col=i + 1,
        )

    # Update layout to improve readability
    condition = str(df["Medical Condition"][0])
    cleaned_fig.update_layout(
        title= f"Health Metrics Comparison (Condition: {condition})" ,
        height=600,
        margin=dict(t=50, b=50),
        showlegend=True,
    )

    # Export the combined figure as an interactive HTML string
    combined_html_string = cleaned_fig.to_html(full_html=True, include_plotlyjs='cdn')
    
    
    
    print(response)

    # Create the HTML content for the textbox
    description_html = f"""
    <div style="width: 80%; margin: 20px auto; text-align: center;">
        <p style="font-size: 16px; color: gray;">
            This chart displays various health metrics for a patient compared to the healthy range. 
            Each subplot represents a different metric, with the shaded area showing the healthy range and the red dot representing the patient's value.
            <br>
            <br>
            <b>AI Diagnosis/Recommendation:</b>
            <br>
            {response}
        </p>
    </div>
    """

    # Append the textbox HTML to the plotly-generated HTML
    final_html_string = combined_html_string.replace("</body>", f"{description_html}</body>")
    
    print(final_html_string)
    # print()


    return d.HtmlDashboard(final_html_string)
