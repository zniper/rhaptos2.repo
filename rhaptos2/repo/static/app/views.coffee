# # Backbone Views
# Most views have the following properties:
#
# 1. Load a Handlebar template using the `hbs` plugin (see `define` below)
# 2. Attach listeners to the corresponding model (see `initialize` methods)
# 3. Attach jQuery listeners to the rendered template (see `onRender` methods)
# 4. Navigate to a different "page" (see `Controller.*` in the `jQuery.on` handlers)
#
# Description of method naming:
#
# 1. `_change*` Modifies the model based on a change in the view
# 2. `_update*` Modifies the view based on changes to the model
#
#  Authors: Michael Mulich, Philip Schatz
#  Copyright (c) 2012 Rice University
#
#  This software is subject to the provisions of the GNU Lesser General
#  Public License Version 2.1 (LGPL).  See LICENSE.txt for details.

#
define [
  'underscore'
  'backbone'
  'marionette'
  'jquery'
  'aloha'
  'app/controller'
  './languages'
  'i18n!app/nls/strings'
  # Load the Handlebar templates
  'hbs!app/views/content-list'
  'hbs!app/views/content-list-item'
  'hbs!app/views/modal-wrapper'
  'hbs!app/views/edit-metadata'
  'hbs!app/views/edit-roles'
  'hbs!app/views/language-variants'
  'hbs!app/views/aloha-toolbar'
  # `bootstrap` and `select2` add to jQuery and don't export anything of their own
  # so they are 'defined' _after_ everything else
  'bootstrap'
  'select2'
], (_, Backbone, Marionette, jQuery, Aloha, Controller, Languages, __, SEARCH_RESULT, SEARCH_RESULT_ITEM, DIALOG_WRAPPER, EDIT_METADATA, EDIT_ROLES, LANGUAGE_VARIANTS, ALOHA_TOOLBAR) ->

  # **FIXME:** Move these URLs into a common module so the mock AJAX code can use them too
  KEYWORDS_URL = '/keywords/'
  USERS_URL = '/users/'
  DELAY_BEFORE_SAVING = 3000

  # Select2 is a multiselect UI library.
  # It queries the webserver to provide search results as you type
  #
  # Given a `url` to query (like `/users` or `/keywords`) this returns a config
  # used when binding select2 to an input.
  SELECT2_AJAX_HANDLER = (url) ->
    quietMillis: 500
    url: url
    dataType: 'json'
    data: (term, page) ->
      q: term # search term
    # parse the results into the format expected by Select2
    results: (data, page) ->
      return {
        results: ({id:id, text:id} for id in data)
      }


  # **FIXME:** Move these subjects to a common module so the mock code can use them and can be used elsewhere
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

  # Given the language list in [languages.coffee](languages.html)
  # this reorganizes them so they can be shown in a dropdown.
  LANGUAGES = [{code: '', native: '', english: ''}]
  for languageCode, value of Languages.getLanguages()
    value = jQuery.extend({}, value)  # Clone the value.
    jQuery.extend(value, {code: languageCode})
    LANGUAGES.push(value)


  # ## "Generic" Views
  #
  # A list of search results (stubs of models only containing an icon, url, title)
  # need a generic view for an item.
  #
  # Since we don't really distinguish between a search result view and a workspace/collection/etc
  # just consider them the same.
  SearchResultItemView = Marionette.ItemView.extend
    template: SEARCH_RESULT_ITEM
    onRender: ->
      @$el.on 'click', =>
        id = @model.get 'id'
        Controller.editContent(id)

  # This can also be thought of as the Workspace view
  SearchResultView = Marionette.CompositeView.extend
    template: SEARCH_RESULT
    itemView: SearchResultItemView

    initialize: ->
      @listenTo @collection, 'reset', => @render()
      @listenTo @collection, 'update', => @render()



  # ## Edit Content
  # Edit the module body and (eventually) metadata from the same view
  ContentEditView = Marionette.ItemView.extend
    # **TODO:** Turn this into a handlebars module so we can add editing metadata in the same div
    #
    # The toolbar div has a `.aloha-dialog` so clicking on it
    # doesn't cause the editable area to lose focus.
    #
    # See `Aloha-Editor/src/lib/aloha.js`:
    #
    #     if (Aloha.activeEditable && !jQuery(".aloha-dialog").is(':visible') && !Aloha.eventHandled) {
    #      Aloha.activeEditable.blur();
    #      ...
    template: (serialized_model) -> "<div class='content-edit-view'><div class='toolbar aloha-dialog'></div><div class='body disabled'>#{serialized_model.body or 'This module is empty. Please change it'}</div></div>"

    initialize: ->
      @listenTo @model, 'change:body', (model, value) =>
        alohaId = @$el.find('.body').attr('id')
        # Sometimes Aloha hasn't loaded up yet
        if alohaId and @$el.parents()[0]
          alohaEditable = Aloha.getEditableById(alohaId)
          editableBody = alohaEditable.getContents()
          alohaEditable.setContents(value) if value != editableBody
        else
          @$el.find('.body').empty().append(value)

    onRender: ->
      # Wait until Aloha is started before loading MathJax.
      # Also, wrap all math in a span/div. MathJax replaces the MathJax element
      # losing all jQuery data attached to it (like popover data, the original Math Formula, etc).
      #
      # Add `aloha-cleanme` so this span is unwrapped when serialized to XHTML
      @$el.find('math').wrap '<span class="math-element aloha-cleanme"></span>'
      MathJax.Hub.Configured() if MathJax?

      # Inside the view is a toolbar and a .body which will have an aloha editable area
      $body = @$el.find('.body')
      $toolbar = @$el.find('.toolbar')

      # Once Aloha has finished loading enable the body
      Aloha.ready ->
        $body.aloha()
        $body.removeClass('disabled')
        # Move the focus onto the body (needs to be delayed though)
        setTimeout (=> $body.focus()), 100

      # Populate the toolbar from the handlebars template
      $toolbar.html(ALOHA_TOOLBAR {})

      # Auto save after the user has stopped making changes
      updateModelAndSave = =>
        alohaId = $body.attr('id')
        # Sometimes Aloha hasn't loaded up yet
        # Only save when the body has changed
        if alohaId
          alohaEditable = Aloha.getEditableById(alohaId)
          editableBody = alohaEditable.getContents()
          @model.set 'body', editableBody
          @model.save() if @model.changedAttributes()

      # Grr, the `aloha-smart-content-changed` can only be listened to globally
      # (via `Aloha.bind`) instead of on each editable.
      #
      # This is problematic when we have multiple Aloha editors on a page.
      # Instead, autosave after some period of inactivity.
      $body.on 'blur', updateModelAndSave



  MetadataEditView = Marionette.ItemView.extend
    template: EDIT_METADATA

    # Bind methods onto jQuery events that happen in the view
    events:
      'change select[name=language]': '_updateLanguageVariant'

    # Update the UI when the language changes.
    # Also called during initial render
    _updateLanguage: () ->
      language = @model.get('language') or ''
      [lang] = language.split('-')
      @$el.find("select[name=language]").select2('val', lang)
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

    # Populate some of the dropdowns like language and subjects.
    # Also, initialize the select2 widget on elements
    onRender: ->
      # Set the title
      @$el.find('*[name=title]').val(@model.get 'title')

      # Populate the Language dropdown and Subjects checkboxes
      $languages = @$el.find('*[name=language]')
      for lang in LANGUAGES
        $lang = jQuery('<option></option>').attr('value', lang.code).text(lang.native)
        $languages.append($lang)

      $languages.select2
        placeholder: __('Select a language')

      $subjects = @$el.find('.subjects')
      for subject in METADATA_SUBJECTS
        $subject = jQuery('<label class="checkbox"><input type="checkbox" name="subjects"/></label>')
        .append(subject)
        # Add the value attribute onto the child `input` element
        $subject.children().attr('value', subject)
        $subjects.append $subject

      # Enable multiselect on certain elements
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

      # Select the correct language (Handlebars can't do that)
      @_updateLanguage()
      @_updateSubjects()
      @_updateKeywords()

      @delegateEvents()

      # Focus on the title
      @$el.find('input[name=title]').focus()
      @

    # This is used by `DialogWrapper` which offers a "Save" and "Cancel" buttons
    attrsToSave: () ->
      title = @$el.find('input[name=title]').val()
      language = @$el.find('select[name=language]').val()
      variant = @$el.find('select[name=variantLanguage]').val()
      language = variant or language
      subjects = (jQuery(checkbox).val() for checkbox in @$el.find('input[name=subjects]:checked'))
      keywords = (kw for kw in @$el.find('*[name=keywords]').val().split('|'))
      # Keywords could be the empty string in which case it would be set to `[""]`
      keywords = [] if '' is keywords[0]

      return {
        title: title
        language: language
        subjects: subjects
        keywords: keywords
      }


  RolesEditView = Marionette.ItemView.extend
    template: EDIT_ROLES

    onRender: ->
      $authors = @$el.find('*[name=authors]')
      $copyrightHolders = @$el.find('*[name=copyrightHolders]')

      $authors.select2
        # **FIXME:** The authors should be looked up instead of being arbitrary text
        tags: @model.get('authors') or []
        tokenSeparators: [',']
        separator: '|'
        #ajax: SELECT2_AJAX_HANDLER(USERS_URL)
      $copyrightHolders.select2
        tags: @model.get('copyrightHolders') or []
        tokenSeparators: [',']
        separator: '|'
        #ajax: SELECT2_AJAX_HANDLER(USERS_URL)

      # Populate the multiselect widgets with data from the backbone model
      @_updateAuthors()
      @_updateCopyrightHolders()

      @delegateEvents()

    _updateAuthors: -> @$el.find('*[name=authors]').select2 'val', (@model.get('authors') or [])
    _updateCopyrightHolders: -> @$el.find('*[name=copyrightHolders]').select2 'val', (@model.get('copyrightHolders') or [])

    attrsToSave: () ->
      # Grab the authors from the multiselect input element.
      # They are separated with a `|` character defined when select2 was configured
      authors = (kw for kw in @$el.find('*[name=authors]').val().split('|'))
      copyrightHolders = (kw for kw in @$el.find('*[name=copyrightHolders]').val().split('|'))

      return {
        authors: authors
        copyrightHolders: copyrightHolders
      }



  # ## DialogWrapper
  # This class wraps a view in a div and only causes changes when
  # the 'Save' button is clicked.
  #
  # Looks like phil came to the same conclusion as the author of Marionette
  # (Don't make a Bootstrap Modal in a `Backbone.View`):
  # [http://lostechies.com/derickbailey/2012/04/17/managing-a-modal-dialog-with-backbone-and-marionette/]
  DialogWrapper = Marionette.ItemView.extend
    template: DIALOG_WRAPPER
    onRender: ->
      @options.view.render()
      @$el.find('.dialog-body').append @options.view.$el

      # Fire a cancel event when the cancel button is pressed
      @$el.on 'click', '.cancel', => @trigger 'cancelled'

      # Trigger the `model.save` when the save button is clicked
      # using the attributes from `@options.view.attrsToSave()`
      @$el.on 'click', '.save', (evt) =>
        evt.preventDefault()
        attrs = @options.view.attrsToSave()

        @options.view.model.save attrs,
          success: (res) =>
            # Trigger a 'sync' because if 'success' is provided 'sync' is not triggered
            @options.view.model.trigger('sync')
            @trigger 'saved'

          error: (res) =>
            alert('Something went wrong when saving: ' + res)


  return {
    WorkspaceView: SearchResultView
    SearchResultView: SearchResultView
    DialogWrapper: DialogWrapper
    MetadataEditView: MetadataEditView
    RolesEditView: RolesEditView
    ContentEditView: ContentEditView
  }
