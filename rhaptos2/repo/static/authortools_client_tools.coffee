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

_generateUrl = (area, id) ->
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
    @$el.on('show', @_statefulRenderer)
    # Bind a method for cleaning up the modal body.
    @$el.on('hidden', @_cleanUp)

  ###
    -- Public api methods --
  ###

  render: (data) ->
    ###
      Display logic for this modal
    ###

  loadData: ->
    ###
      Acquire the data that is used to display the modal.
    ###

  $: (arg) =>
    ###
      Contextualized jQuery just like Backbone.View does it.
    ###
    return $(arg, @$el)

  ###
    -- Private methods --
  ###

  _statefulRenderer: =>
    ###
      Render with state awareness... Display a loading state, connection
      errors, etc.
    ###
    $target = @$('.modal-body')
    opts = MODAL_SPINNER_OPTIONS
    $.extend(opts, {top: $target.height()/2, left: $target.width()/2})
    spinner = new Spinner(MODAL_SPINNER_OPTIONS).spin($target[0])

    stateWrapper = (data) =>
      spinner.stop()
      @render(data)
    $.when(@loadData()).done(stateWrapper)

  _cleanUp: =>
    ###
      Clear the modal body and so that we have a fresh state for the next time.
    ###
    @$('.modal-body').html('')


class MetadataModal extends BaseModal
  selector: '#metadata-modal'
  constructor: ->
    super()
    @$('button[type="submit"]').click(@submitHandler)

  submitHandler: (event) =>
    data = {}
    # Write the form values to JSON
    $.map(@$('form').serializeArray(), (obj) ->
      # Special case for the subject list. Probably a better way to do this...
      if obj.name == 'subjects'
        if not (obj.name of data) then data[obj.name] = []
        data[obj.name].push(obj.value)
      else
        data[obj.name] = obj.value
    )
    # Grab the keywords differently, because they are not part
    #   of the form. They are entered as 'li' entries.
    data['keywords'] = @$('#metadata-keywords').tagit('tags')

    # XXX The best way to get the module ID at this time is to pull it out
    #     of the module editor form. The 'serialise_form' function is defined
    #     globally in the 'authortools_client.js' file.
    module_id = serialise_form().uuid
    # Post the data to the server.
    console.log('Posting metadata for module: ' + module_id)
    $.ajax({
      type: 'POST'
      url: _generateUrl('metadata/', module_id)
      data: JSON.stringify(data, null, 2)
      dataType: 'json'
      contentType: 'application/json'
      success: => @$el.modal('hide')
    })
    # Return false to prevent the form from submitting.
    return false

  languageHandler: (event) =>
    selectedCode = $(event.target).val()
    variants = []
    for code, value of Language.getCombined()
      if code[..1] == selectedCode
        $.extend(value, {code: code})
        variants.push(value)
    $variantLang = @$('select[name="variantLanguage"]')
    if variants.length > 0
      # Insert an empty option into the list.
      variants.splice(0, 0, {code: '', english: ''})
      template = '{{#variants}}<option value="{{code}}">{{english}}</option>{{/variants}}'
      $variantLang.removeAttr('disabled').html(Mustache.to_html(template, {'variants': variants}))
    else
      @$('select[name="variant_language"]').html('').attr('disabled', 'disabled')

  render: (data) ->
    # Collect the language data.
    languages = [{code: '', native: '', english: ''}]
    for languageCode, value of Language.getLanguages()
      value = $.extend({}, value)  # Clone the value.
      $.extend(value, {code: languageCode})
      if data.language? and data.language == languageCode
        $.extend(value, {selected: 'selected'})
      languages.push(value)
    data.languages = languages

    # Collect the variant languages, if there are any.
    if data.language?
      variantLanguages = [{code: '', native: '', english: ''}]
      for languageCode, value of Language.getCombined()
        if languageCode[..1] != data.language
          continue
        $.extend(value, {code: languageCode})
        if data.variantLanguage? and data.variantLanguage == languageCode
          $.extend(value, {selected: 'selected'})
        variantLanguages.push(value)
      data.variantLanguages = variantLanguages

    # Collect the subject data.
    subjects = []
    for subject in METADATA_SUBJECTS
      value = {name: subject}
      if data.subjects? and subject in data.subjects
        value.selected = 'checked'
      subjects.push(value)
    data.subjects = subjects

    # Render to the page.
    @$('.modal-body').html(Mustache.to_html(Templates.METADATA, data))
    @$('select[name="language"]').change(@languageHandler)
    keywordCallback = (request, response) ->
      $.ajax({
        type: 'GET'
        url: '/keywords'
        contentType: 'application/json'
        success: (data) ->
          response(data)
        })
    @$('#metadata-keywords').tagit(
      tagSource: keywordCallback
      initialTags: data.keywords
      minLength: 3
      # The 'space' character has been removed to allow for multi-word
      #   keywords. (e.g. Quantum Physics)
      triggerKeys: ['enter', 'comma', 'tab']
      )

  loadData: ->
    # XXX The best way to get the module ID at this time is to pull it out
    #     of the module editor form. The 'serialise_form' function is defined
    #     globally in the 'authortools_client.js' file.
    module_id = serialise_form().uuid
    return $.ajax({
      type: 'GET'
      url: _generateUrl('metadata/', module_id)
      contentType: 'application/json'
      })


class RoleEntry
  ###
    Data for a single role.
  ###
  constructor: (@name='', @roles=[], @collection=null) ->


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
    @$('button[type="submit"]').click(@submitHandler)

  render: (data) ->
    entries = data
    @collection = new RoleCollection(entries)
    @$('.modal-body').html(Mustache.to_html(Templates.ROLES, {roles_vocabulary: ROLES}))

    # Create a row for entering new entries to the roles listing.
    entry = new RoleEntry()
    $addEntry = $(Mustache.to_html(Templates.ROLES_ADD_ENTRY, @_prepareEntryForRendering(entry)))
    $('input[type="checkbox"]', $addEntry).click(@_roleSelectedHandler(entry))
    $('.role-add-action', $addEntry).click(@_roleAddHandler(entry))
    @$('tbody').append($addEntry)

    for entry in @collection.entries
      @renderEntry(entry)

  loadData: ->
    # XXX The best way to get the module ID at this time is to pull it out
    #     of the module editor form. The 'serialise_form' function is defined
    #     globally in the 'authortools_client.js' file.
    module_id = serialise_form().uuid
    return $.ajax({
      type: 'GET'
      url: _generateUrl('roles/', module_id)
      contentType: 'application/json'
      })

  renderEntry: (entry) ->
    data = @_prepareEntryForRendering(entry)
    # Render the entry...
    $renderedEntry = $(Mustache.to_html(Templates.ROLES_NAME_ENTRY, data))
    # Attach the event handlers
    $('input[type="checkbox"]', $renderedEntry).click(@_roleSelectedHandler(entry))
    $('.role-removal-action', $renderedEntry).click(@_roleRemovalHandler(entry))
    # Append the entry to the modal.
    @$('tbody tr:last').before($renderedEntry)

  submitHandler: (event) =>
    # XXX The best way to get the module ID at this time is to pull it out
    #     of the module editor form. The 'serialise_form' function is defined
    #     globally in the 'authortools_client.js' file.
    module_id = serialise_form().uuid
    # Post the data to the server.
    console.log('Posting metadata for module: ' + module_id)
    data = ({name: e.name, roles: e.roles} for e in @collection.entries)
    $.ajax({
      type: 'POST'
      url: _generateUrl('roles/', module_id)
      data: JSON.stringify(data, null, 2)
      dataType: 'json'
      contentType: 'application/json'
      success: => @$el.modal('hide')
    })
    # Return false to prevent the form from submitting.
    return false

  _prepareEntryForRendering: (entry) ->
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

  _roleAddHandler: (entry) ->
    ###
      Create an event handler that will add a RoleEntry
      to the collection and render it.
    ###
    # XXX What I'm doing here is horrible... seriously...
    #     The loosely coupled nature of the following statements
    #     is aweful.
    eventHandler = (event) =>
      # Grab the name from the input field
      $row = $(event.target).parents('tr')
      $nameField = $row.find('input[name="name"]')
      name = $nameField.val()
      # Add the entry to the collection.
      _entry = @collection.add(new RoleEntry(name, entry.roles))
      console.log("Added '#{name}' to the roles collection.")
      @renderEntry(_entry)
      # Reset the entry object and the input fields.
      $nameField.val('')
      $row.find('input[type="checkbox"]').attr('checked', false)
      entry.roles = []
    return eventHandler

  _roleSelectedHandler: (entry) ->
    ###
      Creates an event handler that will modify the given RoleEntry based
      on the selection.
    ###
    eventHandler = (event) =>
      $target = $(event.target)
      role_name = $target.val()
      if $target.is(':checked')
        # Add the role to the entry.
        entry.roles.push(role_name)
        console.log("Gave the '#{role_name}' role to '#{entry.name}'.")
      else
        entry.roles.pop(entry.roles.indexOf(role_name))
        console.log("Took the '#{role_name}' role away from '#{entry.name}'.")
    return eventHandler

  _roleRemovalHandler: (entry) ->
    ###
      Creates an event handler that will remove the given RoleEntry from the
      page and from the collection.
    ###
    eventHandler = (event) =>
      $(event.target).parents('tr').remove()
      entry.collection.remove(entry)
      console.log("Removed '#{entry.name}' from the roles collection.")
    return eventHandler


exports.construct = ->
  $('.dropdown-toggle').dropdown()
  # Initialize the tool links to display on click.
  for modal_link_id in ['#import-link', '#metadata-link', '#roles-link', '#sharing-link', '#publish-link']
    $(modal_link_id).modal(show: false)
  # Render the data into the modal body.
  $('#import-modal .modal-body').html(Mustache.to_html(Templates.IMPORT, {}))
  metadata_modal = new MetadataModal()
  roles_modal = new RolesModal()
  $('#sharing-modal .modal-body').html(Mustache.to_html(Templates.SHARING, {}))
  $('#publish-modal .modal-body').html(Mustache.to_html(Templates.PUBLISH, {}))

window.Tools = exports
