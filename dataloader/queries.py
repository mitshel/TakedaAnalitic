q_dl_table = """
{% autoescape off %}
select top 100 {{ fields }}
from [Cursor_rpt_LK].dbo.v_Tender_Contract s (nolock)
{% endautoescape %}
"""