{% extends "templates/base.html" %}
{% block title %}Add a Site{% endblock %}

{% block content %}
<h1>Add a Site</h1>
<form name="site_form" action="/sites/add" class="form-horizontal" method="POST">
  <div class="control-group">
    <label class="control-label" for="input01">Site name</label>
    <div class="controls">
      <input type="text" id="input01" name="input01" value="" class="input-xlarge"></input>
      <p class="help-block">In addition to freeform text, any HTML5 text-based input appears like so.</p>
    </div>
  </div>
  <div class="control-group">
    <label class="control-label" for="input01">URL</label>
    <div class="controls">
      <input type="text" id="input01" name="input01" value="" class="input-xlarge"></input>
      <p class="help-block">In addition to freeform text, any HTML5 text-based input appears like so.</p>
    </div>
  </div>
  <div class="control-group">
    <label class="control-label" for="input01">Email address</label>
    <div class="controls">
      <input type="text" id="input01" name="input01" value="" class="input-xlarge"></input>
      <p class="help-block">In addition to freeform text, any HTML5 text-based input appears like so.</p>
    </div>
  </div>
  <div class="control-group">
    <label class="control-label" for="select01">Check interval</label>
    <div class="controls">
      <select id="select01">
        <option value="1">1 minute</option>
        <option value="2">2 minutes</option>
        <option value="3">3 minutes</option>
        <option value="4">4 minutes</option>
        <option value="5">5 minutes</option>
      </select>
    </div>
  </div>
  <div class="form-actions">
    <button type="submit" class="btn btn-primary">Save</button>
     
    <button type="reset" class="btn">Cancel</button>
  </div>
</form>
{% endblock %}
