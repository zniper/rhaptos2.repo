require ["jquery", "underscore", "mustache", "atc/tools", "atc/templates", "jquery-mockjax", "bootstrap", "tagit", "jquery-ui"], ($, _, Mustache, Tools, Templates) ->

  # ATC Doesn't use requirejs yet and so needs global variables to many of the packages.
  window.$ = window.jQuery = $
  window._ = _
  window.Mustache = Mustache
  window.Templates = Templates
  Tools.construct()

  STATE_ROLES = [
    name: "Test Name"
    roles: ["Author"]
  ,
    name: "Another Name"
    roles: ["Author", "Maintainer"]
  ]
  $.mockjax
    type: "GET"
    url: "../..//module//roles/"
    responseTime: 250 #ms
    contentType: "application/json"
    responseText: STATE_ROLES
    response: (settings) ->
      JSON.stringify STATE_ROLES

  $.mockjax
    type: "POST" #FIXME: This should be a PUT (or at least PUT should work)
    url: "../..//module//roles/"
    responseTime: 250 #ms
    contentType: "application/json"

    #responseText: JSON.stringify([{name:'User Name', roles:['Author']}]),
    response: (settings) ->
      roles = JSON.parse(settings.data)

      # Can't just set the variable. it's already bound to mockjax.responseText above.
      # Clear it and re-add all the roles
      STATE_ROLES.splice 0, STATE_ROLES.length
      _.each roles, (userRoles) -> STATE_ROLES.push userRoles

