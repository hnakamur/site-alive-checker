{% extends "templates/base.html" %}
{% from "templates/_formhelpers.html" import field_errors %}
{% block title %}Add a Site{% endblock %}

{% block content %}
<h1>Add a Site</h1>
<form name="site" action="/sites/add" class="form-horizontal" method="POST">
  <div class="control-group">
    <label class="control-label" for="input01">Site name</label>
    <div class="controls">
      {{ form.name(class_="input-xlarge") }}
      {{ field_errors(form.name) }}
    </div>
  </div>
  <div class="control-group">
    <label class="control-label" for="input01">URL</label>
    <div class="controls">
      {{ form.url(class_="input-xlarge") }}
      {{ field_errors(form.url) }}
    </div>
  </div>
  <div class="control-group">
    <label class="control-label" for="input01">Sender address</label>
    <div class="controls">
      {{ form.sender(class_="input-xlarge") }}
      {{ field_errors(form.sender) }}
    </div>
  </div>
  <div class="control-group">
    <label class="control-label" for="input01">Recipient address</label>
    <div class="controls">
      {{ form.recipient(class_="input-xlarge") }}
      {{ field_errors(form.recipient) }}
    </div>
  </div>
  <div class="control-group">
    <label class="control-label" for="input01">Mail subject</label>
    <div class="controls">
      {{ form.subject(class_="input-xlarge") }}
      {{ field_errors(form.subject) }}
    </div>
  </div>
  <div class="control-group">
    <label class="control-label" for="select01">Check interval</label>
    <div class="controls">
      {{ form.interval_minutes }}
      {{ field_errors(form.interval_minutes) }}
    </div>
  </div>
  <div class="control-group">
    <label class="control-label" for="select01">Watching enabled</label>
    <div class="controls">
      {{ form.watching_enabled }}
      {{ field_errors(form.watching_enabled) }}
    </div>
  </div>
  <div class="form-actions">
    <button type="submit" class="btn btn-primary">Save</button>
     
    <button type="reset" class="btn">Cancel</button>
  </div>
</form>
{% endblock %}
