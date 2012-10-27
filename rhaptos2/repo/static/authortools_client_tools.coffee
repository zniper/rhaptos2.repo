###
  authoringtools_client_tools.{coffee,js} - The script used set up and control
    the extended tools interface. These are the tools that are found in the
    tools dropdown in the interface.

  Author: Michael Mulich
  Copyright (c) 2012 Rice University

  This software is subject to the provisions of the GNU Lesser General
  Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
###

# This variable is attached to the window at the very end,
# effectively making it global.
# window.Tools = exports;
exports = {}

_generate_metadata_url = (id) ->
  return MODULEURL + id + '/metadata'

_form_values_to_object = (selector) ->
  data = {}
  $.map($(selector).serializeArray(), (obj) ->
    data[obj['name']] = obj['value']
  )
  return data


class MetadataModal
  constructor: ->
    @$el = $('#metadata-modal')
    @render()
  submit_handler: (event) =>
    data = _form_values_to_object('#metadata-modal form')
    # XXX The best way to get the module ID at this time is to pull it out
    #     of the module editor form. The 'serialise_form' function is defined
    #     globally in the 'authortools_client.js' file.
    module_id = serialise_form().uuid
    # Post the data to the server.
    console.log('Posting metadata for module: ' + module_id)
    $.ajax({
      type: 'POST'
      url: _generate_metadata_url(module_id)
      data: JSON.stringify(data, null, 2)
      dataType: 'json'
      contentType: 'application/json'
      success: -> $('#metadata-modal').modal('hide')
    })
    # Return false to prevent the form from submitting.
    return false
  language_handler: ->
    selected_code = $(this).val()
    variants = []
    for code, value of Language.getCombined()
      if code[..1] == selected_code
        $.extend(value, {code: code})
        variants.push(value)
    $variant_lang = $('#metadata-modal select[name="variant_language"]')
    if variants.length > 0
      # Insert an empty option into the list.
      variants.splice(0, 0, {code: '', english: ''})
      template = '{{#variants}}<option value="{{code}}">{{english}}</option>{{/variants}}'
      $variant_lang.removeAttr('disabled').html(Mustache.to_html(template, {'variants': variants}))
    else
      $('#metadata-modal select[name="variant_language"]').html('').attr('disabled', 'disabled')
  render: ->
    data = {}
    languages = [{code: '', native: '', english: ''}]
    for language_code, value of Language.getLanguages()
      $.extend(value, {'code': language_code})
      languages.push(value)
    $.extend(data, {'languages': languages})
    $('#metadata-modal .modal-body').html(Mustache.to_html(Templates.metadata, data))
    $('#metadata-modal select[name="language"]').change(@language_handler)
    $('#metadata-modal button[type="submit"]').click(@submit_handler)


ROLES = ["Author", "Maintainer", "Copyright Holder"]

class RoleEntry
  ###
    Data for a single role.
  ###
  constructor: (name, roles, collection) ->
    @name = name
    @roles = roles
    @collection = collection || null


class RoleCollection
  ###
    A collection/container of RoleEntry objects.
  ###
  constructor: (entries) ->
    @entries = entries || []
    for entry in entries
      entry.collection = @

class RolesModal
  constructor: ->
    @$el = $('#roles-modal')
    @render()
  render: ->
    # TODO Pull entry data from server
    entries = [
      new RoleEntry('Michael', ['Maintainer', 'Copyright Holder'])
      new RoleEntry('Isabel', ['Author'])
      ]
    collection = new RoleCollection(entries)
    $('#roles-modal .modal-body').html(Mustache.to_html(Templates.roles, {roles_vocabulary: ROLES}))
    for entry in collection.entries
      data = $.extend({}, entry)
      roles = []
      for role in ROLES
        value = {name: role}
        if role in entry.roles
          value.selected = true
        roles.push(value)
      $.extend(data, {roles: roles})
      # Render the entry...
      $rendered_entry = $(Mustache.to_html(Templates.roles_name_entry, data))
      # Append the entry to the modal.
      $('#roles-modal tbody').append($rendered_entry)
  _role_selected_handler: (entry) ->
    ###
      Creates an event handler that will modify the given RoleEntry based
      on the selection.
    ###
    event_handler = (event) =>
      $target = $(event.target)
      role_name = $target.val()
      if $target.is(':checked')
        # Add the role to the entry.
        entry.roles.push(role_name)
        console.log("Gave the '#{role_name}' role to '#{entry.name}'.")
      else
        entry.roles.pop(entry.roles.indexOf(role_name))
        console.log("Took the '#{role_name}' role away from '#{entry.name}'.")
    return event_handler


exports.construct = ->
  $('.dropdown-toggle').dropdown()
  # Initialize the tool links to display on click.
  for modal_link_id in ['#import-link', '#metadata-link', '#roles-link', '#sharing-link', '#publish-link']
    $(modal_link_id).modal(show: false)
  # Render the data into the modal body.
  $('#import-modal .modal-body').html(Mustache.to_html(Templates.metadata, {}))
  metadata_modal = new MetadataModal()
  roles_modal = new RolesModal()
  $('#sharing-modal .modal-body').html(Mustache.to_html(Templates.sharing, {}))
  $('#publish-modal .modal-body').html(Mustache.to_html(Templates.publish, {}))

window.Tools = exports
