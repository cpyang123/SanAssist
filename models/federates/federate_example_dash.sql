SELECT *, :prompt_pattern as Prompt, {{ctx.select_condition}} as Condition
FROM {{ ref("metrics_dataset") }}
--ORDER BY {{ ctx.order_by_cols }}
