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

class MetadataModal
  constructor: ->
    @$el = $('#metadata-modal')
    @render()
  submit_handler: (event) =>
    data = {}
    # Write the form values to JSON
    $.map($('#metadata-modal form').serializeArray(), (obj) ->
      data[obj['name']] = obj['value']
    )
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

class RolesModal
  constructor: ->
    @$el = $('#roles-modal')
    @render()
  render: ->
    data = {}
    entries = [
      {name: 'Michael', roles: ['Maintainer', 'Copyright Holder']}
      {name: 'Isabel', roles: ['Author']}
      ]
    for entry in entries
      roles = []
      for role in ROLES
        value = {name: role}
        if role in entry.roles
          value.selected = true
        roles.push(value)
      entry.roles = roles
    data.entries = entries
    data.roles_vocabulary = ROLES
    partials = {roles_name_entry: Templates.roles_name_entry}
    $('#roles-modal .modal-body').html(Mustache.to_html(Templates.roles, data, partials))
    # $('#role-entry-form button').click(@handle_addition)
  handle_addition: (event) ->
    

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
