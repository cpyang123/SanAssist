SELECT *, :prompt_pattern as Prompt
FROM {{ ref("personal_records") }}
--ORDER BY {{ ctx.order_by_cols }}
