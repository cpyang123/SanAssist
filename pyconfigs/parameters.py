from squirrels import (
    ParametersArgs,
    parameters as p,
    parameter_options as po,
    data_sources as ds,
)


def main(sqrl: ParametersArgs) -> None:
    """
    Create all widget parameters in this file. If two or more datasets use a different set of parameters, define them all
    here, and specify the subset of parameters used for each dataset in the "squirrels.yml" file.

    Parameters are created by a factory method associated to the parameter class. For example, "CreateWithOptions" is the factory method used here:
    > p.SingleSelectParameter.CreateWithOptions(...)

    The parameter classes available are:
    - SingleSelectParameter, MultiSelectParameter, DateParameter, DateRangeParameter, NumberParameter, NumberRangeParameter, TextParameter

    The factory methods available are:
    - CreateSimple, CreateWithOptions, CreateFromSource
    """

    ## Example of creating SingleSelectParameter and specifying each option by code
    group_by_options = [
        po.SelectParameterOption(
            "g0",
            "Blood Type",
            columns=["[Date of Admission]", "[Blood Type]"],
            aliases=["date", "blood_type"],
        ),
        po.SelectParameterOption(
            "g1", "Date", columns=["[Date of Admission]"], aliases=["date"]
        ),
        po.SelectParameterOption(
            "g2",
            "Gender",
            columns=["[Date of Admission]", "Gender"],
            aliases=["date", "gender"],
        ),
        po.SelectParameterOption(
            "g3",
            "Insurance",
            columns=["[Date of Admission]", "[Insurance Provider]"],
            aliases=["date", "insurance"],
        ),
    ]
    p.SingleSelectParameter.CreateWithOptions(
        "group_by",
        "Group By",
        group_by_options,
        description="Dimension(s) to aggregate by",
    )

    ## Example of creating a TextParameter
    parent_name = "group_by"
    name_text_options = [po.TextParameterOption(default_text="emily johnson")]
    p.TextParameter.CreateWithOptions(
        "name_filter",
        "Patient Name",
        name_text_options,
        description="The name of the patient",
    )

    prompt_opt = [
        po.TextParameterOption(default_text="How's the patient looking like?")
    ]
    p.TextParameter.CreateWithOptions(
        "prompt_text",
        "Prompt",
        prompt_opt,
        description="Prompt for the LLM",
    )

    ## Example of creating DateParameter from lookup query/table
    start_date_source = ds.DateDataSource(
        "SELECT min([Date of Admission]) AS min_date, max([Date of Admission]) AS max_date FROM patient_data",
        default_date_col="min_date",
        min_date_col="min_date",
        max_date_col="max_date",
    )
    p.DateParameter.CreateFromSource(
        "start_date",
        "Start Date",
        start_date_source,
        description="Start date to filter transactions by",
    )

    ## Example of creating DateParameter from list of DateParameterOption's
    end_date_option = [
        po.DateParameterOption(
            "2023-12-31", min_date="2010-01-01", max_date="2024-12-31"
        )
    ]
    p.DateParameter.CreateWithOptions(
        "end_date",
        "End Date",
        end_date_option,
        description="End date to filter transactions by",
    )

    ## Example of creating DateRangeParameter
    p.DateRangeParameter.CreateSimple(
        "date_range",
        "Date Range",
        "2011-01-01",
        "2024-12-31",
        min_date="2010-01-01",
        max_date="2024-12-31",
        description="Date range to filter transactions by",
    )

    ## Example of creating MultiSelectParameter from lookup query/table
    category_ds = ds.SelectDataSource(
        "seed_categories", "category_id", "category", from_seeds=True
    )
    p.MultiSelectParameter.CreateFromSource(
        "category",
        "Category Filter",
        category_ds,
        description="The expense categories to filter transactions by",
    )

    p.SingleSelectParameter.CreateFromSource(
        "condition", "Condition", category_ds, description="Condition of Interest"
    )

    ## Example of creating MultiSelectParameter with parent from lookup query/table
    parent_name = "category"
    subcategory_ds = ds.SelectDataSource(
        "seed_subcategories",
        "subcategory_id",
        "subcategory",
        from_seeds=True,
        parent_id_col="category_id",
    )
    p.MultiSelectParameter.CreateFromSource(
        "subcategory",
        "Subcategory Filter",
        subcategory_ds,
        parent_name=parent_name,
        description="The expense subcategories to filter transactions by (available options are based on selected value(s) of 'Category Filter')",
    )

    # ## Example of creating NumberParameter
    # p.NumberParameter.CreateSimple(
    #     "min_filter", "Amounts Greater Than", min_value=0, max_value=500, increment=10,
    #     description="Number to filter on transactions with an amount greater than this value"
    # )

    # ## Example of creating NumberParameter from lookup query/table
    # query = "SELECT 0 as min_value, max(-amount) as max_value, 10 as increment FROM transactions WHERE category <> 'Income'"
    # max_amount_ds = ds.NumberDataSource(query, "min_value", "max_value", increment_col="increment", default_value_col="max_value")
    # p.NumberParameter.CreateFromSource(
    #     "max_filter", "Amounts Less Than", max_amount_ds, description="Number to filter on transactions with an amount less than this value"
    # )

    ## Example of creating NumberRangeParameter
    p.NumberRangeParameter.CreateSimple(
        "bp_between_filter",
        "Systolic BP Between",
        0,
        200,
        default_lower_value=10,
        default_upper_value=200,
        description="Number range to filter systolic blood pressure",
    )

    p.NumberRangeParameter.CreateSimple(
        "age_filter",
        "Patients age between",
        0,
        100,
        default_lower_value=10,
        default_upper_value=90,
        description="Age range of patient",
    )
