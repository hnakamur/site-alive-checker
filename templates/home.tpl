{% extends "base.html" %}
{% block title %}Welcome to top page{% endblock %}

{% block content %}
{% for title in titles %}
<h2>{{ title }}</h2>
{% endfor %}
{% endblock %}
