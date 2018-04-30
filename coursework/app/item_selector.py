
def item_selector(num):
    { %
    for item in store %}
    { % if item.cat == "Mens" %}
    { % if item.id == 1 %}
    < p > {{item.name}} < / p >
    < img
    src = "{{ url_for("
    static
    ", filename=item.image) }}" >


{ % endif %}
{ % endif %}
{ % endfor %}