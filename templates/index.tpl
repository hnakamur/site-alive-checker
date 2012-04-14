{% extends "templates/base.html" %}
{% block title %}Welcome to top page{% endblock %}

{% block content %}
<h1>Sites</h1>
<table class="table table-bordered table-striped">
  <thead>
    <tr><th>Name</th><th>URL</th><th>Recipient</th></tr>
  </thead>
  <tbody>
  {% for site in sites %}
    <tr><td>{{ site.name }}</td><td>{{ site.url }}</td><td>{{ site.recipient }}</td></tr>
  {% endfor %}
  </tbody>
</table>
<a class="btn js-btn btn-primary" href="/sites/add">Add Site</a>
{% endblock %}
