WITH
patient_data_with_masked_id AS (
    SELECT *,
{%- if user.role == "manager" %}
        Name as Name
{%- else %}
        '***' as Name
{%- endif %},
        STRFTIME('%Y-%m', [Date of Admission] ) AS month
    FROM patient_data
)
SELECT *
FROM patient_data_with_masked_id
WHERE [Date of Admission] >= :start_date
    AND [Date of Admission] <= :end_date
    AND [Systolic BP] >= :min_amount
    AND [Systolic BP] <= :max_amount
    AND Age <= :max_age
    AND Age >= :min_age
    {% if is_placeholder("name_pattern") -%} AND Name LIKE :name_pattern {%- endif %}
ORDER By [Date of Admission] DESC
