q_dl_table = """
{% autoescape off %}
select top {{ rows }} {{ fields }}
from [Cursor_rpt_LK].dbo.v_Tender_Contract s (nolock)
{% if filters %}where {{ filters }} {% endif %}
{% endautoescape %}
"""