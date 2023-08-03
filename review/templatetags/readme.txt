utilisable uniquement dans les templates de l'application

{% extends 'base.html' %} 
{% block content %}

    {% load custom_filters %}
    {% for element in elements %}
        {% if element|is_instance_of_blog %}
        ...faire quelques chose ici...
        {% endif %}

{% endblock content %}