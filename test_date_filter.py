from django.template import Template, Context
t = Template('{{ v|date:"Y-m-d" }}')
result = t.render(Context({'v': None}))
print("None result:", repr(result))
