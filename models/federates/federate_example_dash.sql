SELECT *, :prompt_pattern as Prompt
FROM {{ ref("metrics_dataset") }}
--ORDER BY {{ ctx.order_by_cols }}
