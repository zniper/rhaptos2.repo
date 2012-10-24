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

METADATA_SUBJECTS = ["Arts", "Mathematics and Statistics", "Business",
  "Science and Technology", "Humanities", "Social Sciences"]


_generate_metadata_url = (id) ->
  return MODULEURL + id + '/metadata'

class MetadataModal
  constructor: ->
    @$el = $('#metadata-modal')
    $('#metadata-modal button[type="submit"]').click(@submit_handler)
    # Attach the rendering code to the modal 'show' event.
    @$el.on('show', $.proxy(@render, @))
  submit_handler: (event) =>
    data = {}
    # Write the form values to JSON
    $.map($('#metadata-modal form').serializeArray(), (obj) ->
      # Special case for the subject list. Probably a better way to do this...
      if obj.name == 'subjects'
        if not (obj.name of data) then data[obj.name] = []
        data[obj.name].push(obj.value)
      else
        data[obj.name] = obj.value
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
    # XXX The best way to get the module ID at this time is to pull it out
    #     of the module editor form. The 'serialise_form' function is defined
    #     globally in the 'authortools_client.js' file.
    module_id = serialise_form().uuid

    renderer = (data) ->
      # XXX Should check for issues before doing the following...

      # Collect the language data.
      languages = [{code: '', native: '', english: ''}]
      for language_code, value of Language.getLanguages()
        $.extend(value, {code: language_code})
        if data.language? and data.language == language_code
          $.extend(value, {selected: 'selected'})
        languages.push(value)
      data.languages = languages
      if data.language?
        variant_languages = [{code: '', native: '', english: ''}]
        for language_code, value of Language.getCombined()
          if language_code[..1] != data.language
            continue
          $.extend(value, {code: language_code})
          if data.variant_language? and data.variant_language == language_code
            $.extend(value, {selected: 'selected'})
          variant_languages.push(value)
        data.variant_languages = variant_languages

      # Collect the subject data.
      subjects = []
      for subject in METADATA_SUBJECTS
        value = {name: subject}
        if data.subjects? and subject in data.subjects
          value.selected = 'checked'
        subjects.push(value)
      data.subjects = subjects

      # Render to the page.
      $('#metadata-modal .modal-body').html(Mustache.to_html(Templates.metadata, data))
      $('#metadata-modal select[name="language"]').change(@language_handler)

    $.when(
      $.ajax({
        type: 'GET'
        url: _generate_metadata_url(module_id)
        contentType: 'application/json'
      })
    ).then($.proxy(renderer, @))
  

exports.construct = ->
  $('.dropdown-toggle').dropdown()
  # Initialize the tool links to display on click.
  for modal_link_id in ['#import-link', '#metadata-link', '#sharing-link', '#publish-link']
    $(modal_link_id).modal(show: false)
  # Render the data into the modal body.
  $('#import-modal .modal-body').html(Mustache.to_html(Templates.metadata, {}))
  metadata_modal = new MetadataModal()
  $('#sharing-modal .modal-body').html(Mustache.to_html(Templates.sharing, {}))
  $('#publish-modal .modal-body').html(Mustache.to_html(Templates.publish, {}))

window.Tools = exports
