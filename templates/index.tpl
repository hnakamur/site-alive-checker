{% extends "templates/base.html" %}
{% block title %}Welcome to top page{% endblock %}

{% block content %}
<h1>Sites</h1>
{% if sites %}
<table class="table table-bordered table-striped">
  <thead>
    <tr>
      <th>Name</th>
      <th>URL</th>
      <th>Recipient</th>
      <th>Interval minutes</th>
      <th>Watching enabled</th>
    </tr>
  </thead>
  <tbody>
  {% for site in sites %}
    <tr>
      <td><a href="/site/{{ site.key() }}">{{ site.name|e }}</a></td>
      <td>{{ site.url|e }}</td>
      <td>{{ site.recipient|e }}</td>
      <td>{{ site.interval_minutes }}</td>
      <td>{{ site.watching_enabled }}</td>
    </tr>
  {% endfor %}
  </tbody>
</table>
{% else %}
<div class="alert alert-info">
  <strong>Let's add a site!</strong>
  No sites are registered yet. Please add one.
</div>
{% endif %}
<a class="btn js-btn btn-primary" href="/sites/add">Add Site</a>
{% endblock %}
