#  authoringtools_client_tools.{coffee,js} - The script used set up and control
#    the extended tools interface. These are the tools that are found in the
#    tools dropdown in the interface.
#
#  Authors: Michael Mulich, Philip Schatz
#  Copyright (c) 2012 Rice University
#
#  This software is subject to the provisions of the GNU Lesser General
#  Public License Version 2.1 (LGPL).  See LICENSE.txt for details.

# __Note:__ `bootstrap` and `select2` add to jQuery and don't export anything of their own
define ['backbone', 'jquery', './templates', './languages', 'bootstrap', 'select2'], (Backbone, jQuery, Templates, Languages) ->

  # FIXME: Move these URLs into a common module so the mock AJAX code can use them too
  KEYWORDS_URL = '/keywords/'
  USERS_URL = '/users/'

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

  # Default language for new content is the browser's language
  browserLanguage = (navigator.userLanguage or navigator.language or '').toLowerCase()

  # This model contains the following members:
  # * `title` - a text title of the module
  # * `language` - the main language (eg `en-us`)
  # * `subjects` - an array of strings (eg `['Mathematics', 'Business']`)
  # * `keywords` - an array of keywords (eg `['constant', 'boltzmann constant']`)
  # * `authors` - an `Collection` of `User`s that are attributed as authors
  Module = Backbone.Model.extend
    defaults:
      language: browserLanguage
    url: ->
      @get 'url'


  MetadataEditView = Backbone.View.extend
    tagName: 'div'
    className: 'metadata'

    # Description of method naming:
    # `_change*` Modifies the model based on a change in the view
    # `_update*` Modifies the view based on changes to the model
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
        $variant.html(Templates.LANGUAGE_VARIANTS('variants': variants))
        $variant.find("option[value=#{language}]").attr('selected', true)
      else
        $variant.html('').attr('disabled', true)

    # Update the View with new subjects selected
    _updateSubjects: ->
      @$el.find('input[name=subjects]').attr('checked', false)
      for subject in @model.get('subjects') or []
        @$el.find("input[name=subjects][value='#{subject}']").attr('checked', true)

    render: () ->
      templateObj = jQuery.extend({}, @model.toJSON())
      templateObj._languages = LANGUAGES
      templateObj._subjects = METADATA_SUBJECTS
      @$el.append Templates.METADATA(templateObj)

      # Select the correct language (mustache can't do that)
      @_updateLanguage()
      @_updateSubjects()

      # tagit (specifically its config of autocomplete) requires this element be part of the DOM
      # so we add the keywords to the body and then put it back
      $keywords = @$el.find('*[name=keywords]')
      $keywords.select2
        tags: @model.get('keywords') or []
        tokenSeparators: [',']
        separator: '|' # String used to delimit ids in $('input').val()
        ajax: SELECT2_AJAX_HANDLER(KEYWORDS_URL)

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

    # Description of method naming:
    # `_change*` Modifies the model based on a change in the view
    # `_update*` Modifies the view based on changes to the model

    render: () ->
      @$el.append jQuery(Templates.ROLES(@model.toJSON()))

      $authors = @$el.find('*[name=authors]')
      $copyrightHolders = @$el.find('*[name=copyrightHolders]')

      $authors.select2
        tags: @model.get('authors') or []
        tokenSeparators: [',']
        separator: '|'
        #ajax: SELECT2_AJAX_HANDLER(USERS_URL)
      $copyrightHolders.select2
        tags: @model.get('copyrightHolders') or []
        tokenSeparators: [',']
        separator: '|'
        #ajax: SELECT2_AJAX_HANDLER(USERS_URL)

      @delegateEvents()
      @

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
      @$el = jQuery(Templates.MODAL_WRAPPER(title: title))
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
      @$el.modal(keyboard: true)
    hide: ->
      @$el.modal('hide')


  return {
    Module: Module
    ModalWrapper: ModalWrapper
    MetadataEditView: MetadataEditView
    RolesEditView: RolesEditView
  }
