#  authoringtools_client_tools.{coffee,js} - The script used set up and control
#    the extended tools interface. These are the tools that are found in the
#    tools dropdown in the interface.
#
#  Authors: Michael Mulich, Philip Schatz
#  Copyright (c) 2012 Rice University
#
#  This software is subject to the provisions of the GNU Lesser General
#  Public License Version 2.1 (LGPL).  See LICENSE.txt for details.

define [
  'backbone'
  'jquery'
  './languages'
  # Load the Handlebars templates
  'hbs!app/views/content-list'
  'hbs!app/views/modal-wrapper'
  'hbs!app/views/edit-metadata'
  'hbs!app/views/edit-roles'
  'hbs!app/views/language-variants'
  # `bootstrap` and `select2` add to jQuery and don't export anything of their own
  # so they are 'defined' _after_ everything else
  'bootstrap'
  'select2'
], (Backbone, jQuery, Languages, WORKSPACE, MODAL_WRAPPER, EDIT_METADATA, EDIT_ROLES, LANGUAGE_VARIANTS) ->

  # FIXME: Move these URLs into a common module so the mock AJAX code can use them too
  KEYWORDS_URL = '/keywords/'
  USERS_URL = '/users/'
  DELAY_BEFORE_SAVING = 3000

  SELECT2_AJAX_HANDLER = (url) ->
    quietMillis: 500
    url: url
    dataType: 'json'
    data: (term, page) ->
      q: term # search term
    # parse the results into the format expected by Select2
    results: (data, page) ->
      #data.unshift query.term
      return {
        results: ({id:id, text:id} for id in data)
      }


  # FIXME: Move these subjects to a common module so the mock code can use them and can be used elsewhere
  METADATA_SUBJECTS = ['Arts', 'Mathematics and Statistics', 'Business',
    'Science and Technology', 'Humanities', 'Social Sciences']

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

  LANGUAGES = [{code: '', native: '', english: ''}]
  for languageCode, value of Languages.getLanguages()
    value = jQuery.extend({}, value)  # Clone the value.
    jQuery.extend(value, {code: languageCode})
    LANGUAGES.push(value)


  WorkspaceView = Backbone.View.extend
    tagName: 'div'
    className: 'workspace'

    initialize: ->
      @listenTo @model, 'reset', => @render()
      @listenTo @model, 'update', => @render()
    render: ->
      @$el.empty().append WORKSPACE { items: @model.toJSON() }

  ContentEditView = Backbone.View.extend
    className: 'body'

    initialize: ->
      @listenTo @model, 'change:body', (model, value) =>
        alohaId = @$el.attr('id')
        # Sometimes Aloha hasn't loaded up yet
        if alohaId and @$el.parents()[0]
          alohaEditable = Aloha.getEditableById(alohaId)
          editableBody = alohaEditable.getContents()
          alohaEditable.setContents(value) if value != editableBody
        else
          @$el.empty().append(value)


    render: ->
      @$el.append @model.get('body')

      # Wait until Aloha is started before loading MathJax
      # Also, wrap all math in a span/div. MathJax replaces the MathJax element
      # losing all jQuery data attached to it (like popover data, the original Math Formula, etc)
      # Add `aloha-cleanme` so this span is unwrapped when serialized to XHTML
      @$el.find('math').wrap '<span class="math-element aloha-cleanme"></span>'
      MathJax.Hub.Configured()

      @$el.aloha()
      setTimeout (=> @$el.focus()), 100

      # Auto save after the user has stopped making changes for DELAY_BEFORE_SAVING millisecs
      #autosaveTimeout = null
      updateModelAndSave = =>
        alohaId = @$el.attr('id')
        # Sometimes Aloha hasn't loaded up yet
        if alohaId
          alohaEditable = Aloha.getEditableById(alohaId)
          editableBody = alohaEditable.getContents()
          @model.save 'body', editableBody
        #clearTimeout autosaveTimeout
        #autosaveTimeout = setTimeout autoSave DELAY_BEFORE_SAVING

      # Grr, 'aloha-smart-content-changed' doesn't work unless you globally bind (Aloha.bind)
      @$el.on 'blur', updateModelAndSave

  MetadataEditView = Backbone.View.extend
    tagName: 'div'
    className: 'metadata'

    # Description of method naming:
    #
    # 1. `_change*` Modifies the model based on a change in the view
    # 2. `_update*` Modifies the view based on changes to the model
    events:
      'change select[name=language]': '_updateLanguageVariant'

    # Update the UI when the language changes
    # Also called during initial render
    _updateLanguage: () ->
      language = @model.get('language') or ''
      [lang] = language.split('-')
      @$el.find("select[name=language] option[value=#{lang}]")
      .attr('selected', true)
      @_updateLanguageVariant()

    _updateLanguageVariant: () ->
      $language = @$el.find('select[name=language]')
      language = @model.get('language') or ''
      [lang, variant] = language.split('-')
      if $language.val() != lang
        lang = $language.val()
        variant = null
      $variant = @$el.find('select[name=variantLanguage]')
      variants = []
      for code, value of Languages.getCombined()
        if code[..1] == lang
          jQuery.extend(value, {code: code})
          variants.push(value)
      if variants.length > 0
        # Generate the language variants dropdown.
        $variant.removeAttr('disabled')
        $variant.html(LANGUAGE_VARIANTS('variants': variants))
        $variant.find("option[value=#{language}]").attr('selected', true)
      else
        $variant.html('').attr('disabled', true)

    # Helper method to populate a multiselect input
    _updateSelect2: (inputName, modelKey) ->
      @$el.find("input[name=#{inputName}]").attr('checked', false)
      for subject in @model.get(modelKey) or []
        @$el.find("input[name=#{inputName}][value='#{subject}']").attr('checked', true)

    # Update the View with new subjects selected
    _updateSubjects: ->
      @$el.find('input[name=subjects]').attr('checked', false)
      for subject in @model.get('subjects') or []
        @$el.find("input[name=subjects][value='#{subject}']").attr('checked', true)

    # Update the View with new keywords selected
    _updateKeywords: -> @$el.find('input[name=keywords]').select2('val', @model.get 'keywords')

    render: ->
      templateObj = jQuery.extend({}, @model.toJSON())
      templateObj._languages = LANGUAGES
      templateObj._subjects = METADATA_SUBJECTS
      @$el.append EDIT_METADATA(templateObj)

      # tagit (specifically its config of autocomplete) requires this element be part of the DOM
      # so we add the keywords to the body and then put it back
      $keywords = @$el.find('*[name=keywords]')
      $keywords.select2
        tags: @model.get('keywords') or []
        tokenSeparators: [',']
        separator: '|' # String used to delimit ids in $('input').val()
        ajax: SELECT2_AJAX_HANDLER(KEYWORDS_URL)
        initSelection: (element, callback) ->
          data = []
          _.each element.val().split('|'), (str) -> data.push {id: str, text: str}
          callback(data)

      # Select the correct language (mustache can't do that)
      @_updateLanguage()
      @_updateSubjects()
      @_updateKeywords()

      @delegateEvents()

      # Focus on the title
      @$el.find('input[name=title]').focus()
      @

    # This is used by wrappers like ModalWrapper that offer a "Save" button
    attrsToSave: () ->
      title = @$el.find('input[name=title]').val()
      language = @$el.find('select[name=language]').val()
      variant = @$el.find('select[name=variantLanguage]').val()
      language = variant if variant
      subjects = (jQuery(checkbox).val() for checkbox in @$el.find('input[name=subjects]:checked'))
      # Grab the keywords differently, because they are not part
      #   of the form. They are entered as 'li' entries.
      keywords = (kw for kw in @$el.find('*[name=keywords]').val().split('|'))

      return {
        title: title
        language: language
        subjects: subjects
        keywords: keywords
      }


  RolesEditView = Backbone.View.extend
    tagName: 'div'
    className: 'roles'

    render: () ->
      @$el.append jQuery(EDIT_ROLES(@model.toJSON()))

      $authors = @$el.find('*[name=authors]')
      $copyrightHolders = @$el.find('*[name=copyrightHolders]')

      $authors.select2
        # FIXME: The tags should be looked up instead of being hardcoded
        tags: @model.get('authors') or []
        tokenSeparators: [',']
        separator: '|'
        #ajax: SELECT2_AJAX_HANDLER(USERS_URL)
      $copyrightHolders.select2
        tags: @model.get('copyrightHolders') or []
        tokenSeparators: [',']
        separator: '|'
        #ajax: SELECT2_AJAX_HANDLER(USERS_URL)

      @_updateAuthors()
      @_updateCopyrightHolders()

      @delegateEvents()
      @

    _updateAuthors: -> @$el.find('*[name=authors]').select2 'val', (@model.get('authors') or [])
    _updateCopyrightHolders: -> @$el.find('*[name=copyrightHolders]').select2 'val', (@model.get('copyrightHolders') or [])

    attrsToSave: () ->
      # Grab the authors
      authors = (kw for kw in @$el.find('*[name=authors]').val().split('|'))
      copyrightHolders = (kw for kw in @$el.find('*[name=copyrightHolders]').val().split('|'))

      return {
        authors: authors
        copyrightHolders: copyrightHolders
      }


  # ## ModalWrapper
  # This class wraps a view in a modal dialog and only causes changes when
  # the 'Save' button is clicked.
  class ModalWrapper
    constructor: (@view, title) ->
      @view.render()
      @$el = jQuery(MODAL_WRAPPER(title: title))
      @$el.find('.modal-body').html('').append @view.$el

      # Trigger the save when the save button is clicked
      @$el.on 'click', '.save', (evt) =>
        evt.preventDefault()
        # Get the value of the attributes that need to be saved from the View
        # and then save them to the server
        attrs = @view.attrsToSave()

        @view.model.save attrs,
          success: (res) =>
            # Trigger a 'sync' because if 'success' is provided 'sync' is not triggered
            @view.model.trigger('sync')
            @$el.modal('hide')

          error: (res) =>
            alert('Something went wrong when saving: ' + res)


    show: ->
      @$el.appendTo('body') if not @$el.parent()[0]
      @$el.modal(keyboard: true)
    hide: ->
      @$el.modal('hide')


  return {
    WorkspaceView: WorkspaceView
    ModalWrapper: ModalWrapper
    MetadataEditView: MetadataEditView
    RolesEditView: RolesEditView
    ContentEditView: ContentEditView
  }
