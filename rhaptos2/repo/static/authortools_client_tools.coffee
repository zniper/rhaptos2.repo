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
ROLES = ["Author", "Maintainer", "Copyright Holder"]

MODAL_SPINNER_OPTIONS = {
  lines: 13  # The number of lines to draw
  length: 16  # The length of each line
  width: 6  # The line thickness
  radius: 27  # The radius of the inner circle
  corners: 1  # Corner roundness (0..1)
  rotate: 0  # The rotation offset
  color: '#444'  # #rgb or #rrggbb
  speed: 0.9  # Rounds per second
  trail: 69  # Afterglow percentage
  shadow: false  # Whether to render a shadow
  hwaccel: false  # Whether to use hardware acceleration
  className: 'spinner'  # The CSS class to assign to the spinner
  zIndex: 2e9  # The z-index (defaults to 2000000000)
  top: 'auto'  # Top position relative to parent in px
  left: '265px'  # Left position relative to parent in px
}

_generate_url = (area, id) ->
  ###
    Returns a URL for given area and id. This is a simple abstraction for
    acquiring the URL.
  ###
  return MODULEURL + id + '/' + area


class BaseModal
  ###
    A base class for common modal behavior and state.
  ###

  # A class defined selector used to assign 'el' and '$el'.
  selector: null
  # Alight with the Backbone.View properties:
  el: null
  $el: null

  constructor: ->
    if !@selector?
      throw new Error("Required property 'selector' is undefined.")
    @$el = $(@selector)
    @el = @$el.first()[0]
    # Bind the 'render' method to the modal 'show' event.
    @$el.on('show', @_stateful_renderer)
    # Bind a method for cleaning up the modal body.
    @$el.on('hidden', @_clean_up)

  ###
    -- Public api methods --
  ###

  render: (data) ->
    ###
      Display logic for this modal
    ###

  get_data: ->
    ###
      Acquire the data that is used to display the modal.
    ###


  ###
    -- Private methods --
  ###

  _stateful_renderer: =>
    ###
      Render with state awareness... Display a loading state, connection
      errors, etc.
    ###
    $target = $('.modal-body', @$el)
    opts = MODAL_SPINNER_OPTIONS
    $.extend(opts, {top: $target.height()/2, left: $target.width()/2})
    spinner = new Spinner(MODAL_SPINNER_OPTIONS).spin($target[0])

    state_wrapper = (data) =>
      spinner.stop()
      @render(data)
    $.when(@get_data()).done(state_wrapper)

  _clean_up: =>
    ###
      Clear the modal body and so that we have a fresh state for the next time.
    ###
    $('.modal-body', @$el).html('')


class MetadataModal extends BaseModal
  selector: '#metadata-modal'
  constructor: ->
    super()
    $('button[type="submit"]', @$el).click(@submit_handler)
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
      url: _generate_url('metadata', module_id)
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
  render: (data) ->
    # Collect the language data.
    languages = [{code: '', native: '', english: ''}]
    for language_code, value of Language.getLanguages()
      $.extend(value, {code: language_code})
      if data.language? and data.language == language_code
        $.extend(value, {selected: 'selected'})
      languages.push(value)
    data.languages = languages

    # Collect the variant languages, if there are any.
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

  get_data: ->
    # XXX The best way to get the module ID at this time is to pull it out
    #     of the module editor form. The 'serialise_form' function is defined
    #     globally in the 'authortools_client.js' file.
    module_id = serialise_form().uuid
    return $.ajax({
      type: 'GET'
      url: _generate_url('metadata', module_id)
      contentType: 'application/json'
      })


class RoleEntry
  ###
    Data for a single role.
  ###
  constructor: (name, roles, collection) ->
    @name = name || ""
    @roles = roles || []
    @collection = collection || null


class RoleCollection
  ###
    A collection/container of RoleEntry objects.
  ###
  constructor: (entries) ->
    @entries = entries || []
    # Associate the entries with this collection for back referencing.
    for entry in entries
      entry.collection = @
  add: (entry) ->
    ###
      Adds an entry to this collection object.
    ###
    entry.collection = @
    i = @entries.push(entry)
    return @entries[i-1]
  remove: (entry) ->
    ###
      Removes the given entry from this collection object.
    ###
    @entries.splice(@entries.indexOf(entry), 1)


class RolesModal extends BaseModal
  selector: '#roles-modal'
  constructor: ->
    super()
    # Bind the submit event handler.
    $('button[type="submit"]', @$el).click(@submit_handler)

  render: (data) ->
    entries = data
    @collection = new RoleCollection(entries)
    $('#roles-modal .modal-body').html(Mustache.to_html(Templates.roles, {roles_vocabulary: ROLES}))

    # Create a row for entering new entries to the roles listing.
    entry = new RoleEntry()
    $add_entry = $(Mustache.to_html(Templates.roles_add_entry, @_prepare_entry_for_rendering(entry)))
    $('input[type="checkbox"]', $add_entry).click(@_role_selected_handler(entry))
    $('.role-add-action', $add_entry).click(@_role_add_handler(entry))
    $('#roles-modal tbody').append($add_entry)

    for entry in @collection.entries
      @render_entry(entry)

  get_data: ->
    # XXX The best way to get the module ID at this time is to pull it out
    #     of the module editor form. The 'serialise_form' function is defined
    #     globally in the 'authortools_client.js' file.
    module_id = serialise_form().uuid
    return $.ajax({
      type: 'GET'
      url: _generate_url('roles', module_id)
      contentType: 'application/json'
      })

  render_entry: (entry) ->
    data = @_prepare_entry_for_rendering(entry)
    # Render the entry...
    $rendered_entry = $(Mustache.to_html(Templates.roles_name_entry, data))
    # Attach the event handlers
    $('input[type="checkbox"]', $rendered_entry).click(@_role_selected_handler(entry))
    $('.role-removal-action', $rendered_entry).click(@_role_removal_handler(entry))
    # Append the entry to the modal.
    $('#roles-modal tbody tr:last').before($rendered_entry)
  submit_handler: (event) =>
    # XXX The best way to get the module ID at this time is to pull it out
    #     of the module editor form. The 'serialise_form' function is defined
    #     globally in the 'authortools_client.js' file.
    module_id = serialise_form().uuid
    # Post the data to the server.
    console.log('Posting metadata for module: ' + module_id)
    data = ({name: e.name, roles: e.roles} for e in @collection.entries)
    $.ajax({
      type: 'POST'
      url: _generate_url('roles', module_id)
      data: JSON.stringify(data, null, 2)
      dataType: 'json'
      contentType: 'application/json'
      success: => @$el.modal('hide')
    })
    # Return false to prevent the form from submitting.
    return false
  _prepare_entry_for_rendering: (entry) ->
    ###
      Create a Mustache compatible RoleEntry representation.
    ###
    # Copy/clone the object.
    data = $.extend({}, entry)
    roles = []
    for role in ROLES
      value = {name: role}
      if role in data.roles
        value.selected = true
      roles.push(value)
    $.extend(data, {roles: roles})
    return data
  _role_add_handler: (entry) ->
    ###
      Create an event handler that will add a RoleEntry
      to the collection and render it.
    ###
    # XXX What I'm doing here is horrible... seriously...
    #     The loosely coupled nature of the following statements
    #     is aweful.
    event_handler = (event) =>
      # Grab the name from the input field
      $row = $(event.target).parents('tr')
      $name_field = $row.find('input[name="name"]')
      name = $name_field.val()
      # Add the entry to the collection.
      _entry = @collection.add(new RoleEntry(name, entry.roles))
      console.log("Added '#{name}' to the roles collection.")
      @render_entry(_entry)
      # Reset the entry object and the input fields.
      $name_field.val('')
      $row.find('input[type="checkbox"]').attr('checked', false)
      entry.roles = []
    return event_handler
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
  _role_removal_handler: (entry) ->
    ###
      Creates an event handler that will remove the given RoleEntry from the
      page and from the collection.
    ###
    event_handler = (event) =>
      $(event.target).parents('tr').remove()
      entry.collection.remove(entry)
      console.log("Removed '#{entry.name}' from the roles collection.")
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
