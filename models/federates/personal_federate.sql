SELECT *
FROM {{ ref("personal_records") }}
--ORDER BY {{ ctx.order_by_cols }}
