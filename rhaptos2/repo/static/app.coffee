# # Application Root
# This is the start of the application. Steps:
#
# 1. Load dependencies (JS/CSS/JSON)
# 2. Register client-side routes
# 3. Load any HTML/JSON sent from the server that is sprinkled in the HTML file
#
# For example, if the user goes to a piece of content we already send
# the content inside a `div` tag.
# The same can be done with metadata/roles (as a JSON object sent in the HTML)
define ['jquery', 'aloha', 'app/views', 'i18n!app/nls/strings', 'css!app'], (jQuery, Aloha, Views, __) ->


  # **HACK:** to discourage people from using the global jQuery
  # and instead use the `requirejs` version.
  # This helps ensure plugins that extend jQuery (like bootstrap)
  # are properly listed as dependencies in requirejs' `define`
  @jQuery = @$ = ->
    console.warn 'You should add "jquery" to your dependencies in define() instead of using the global jQuery!'
    jQuery.apply @, arguments
  jQuery.extend(@jQuery, jQuery)

  # ## Load the Model
  # Assume the app starts with editing a single `Module`.
  # Either the user is editing an existing `Module` or a new one.
  content = null
  loadModel = ->
    uuid = jQuery('#uuid').val() # TODO: Replace `#uuid` with Backbone Routes
    if uuid
      content = new Views.Module(id: uuid, url: "/module/#{uuid}/metadata/")
      content.fetch()
    else
      content = new Views.Module()
  loadModel()
  # **TODO:** Use backbone routes instead of `#uuid` to figure out the current content
  jQuery('#uuid').on 'change', ->
    loadModel()


  # ## Bind UI Popups
  # This section generates the UI menus and buttons
  #
  # `__()` is a i18n function that looks up a localized string
  jQuery('#metadata-link').on 'click', (evt) ->
    evt.preventDefault()
    modal = new Views.ModalWrapper(new Views.MetadataEditView(model: content), __('Edit Metadata'))
    modal.show()

  jQuery('#roles-link').on 'click', (evt) ->
    evt.preventDefault()
    modal = new Views.ModalWrapper(new Views.RolesEditView(model: content), __('Edit Roles'))
    modal.show()


  # ## Start Aloha
  # Once Aloha has finished loading, enable it on the document and let MathJax know it can start rendering
  Aloha.ready ->
    Aloha.jQuery('.document').aloha().focus()

    # Wait until Aloha is started before loading MathJax
    # Also, wrap all math in a span/div. MathJax replaces the MathJax element
    # losing all jQuery data attached to it (like popover data, the original Math Formula, etc)
    # Add `aloha-cleanme` so this span is unwrapped when serialized to XHTML
    jQuery('math').wrap '<span class="math-element aloha-cleanme"></span>'
    MathJax.Hub.Configured()
