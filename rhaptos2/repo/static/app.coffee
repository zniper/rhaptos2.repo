define ['jquery', 'aloha', 'app/views'], (jQuery, Aloha, Views) ->

  # HACK to discourage people from using the global jQuery
  # and instead use the requirejs version.
  # This helps ensure plugins that extend jQuery (like bootstrap)
  # are properly listed as dependencies in requirejs' `define`
  @jQuery = @$ = ->
    console.warn 'You should add "jquery" to your dependencies in define() instead of using the global jQuery!'
    jQuery.apply @, arguments
  jQuery.extend(@jQuery, jQuery)

  # Bind the editor to the document and let mathjax know it can start rendering
  Aloha.ready ->
    Aloha.jQuery('.document').aloha().focus()

    # Wait until Aloha is started before loading MathJax
    # Also, wrap all math in a span/div. MathJax replaces the MathJax element
    # losing all jQuery data attached to it (like popover data, the original Math Formula, etc)
    # add aloha-cleanme so this span is unwrapped
    jQuery('math').wrap '<span class="math-element aloha-cleanme"></span>'
    MathJax.Hub.Configured()


  # Build a Model for the current content:
  # TODO: Use backbone routes to figure out the current content

  content = null
  loadModel = ->
    uuid = jQuery('#uuid').val()
    if uuid
      content = new Views.Module(id: uuid, url: "/module/#{uuid}/metadata/")
      content.fetch()
    else
      content = new Views.Module()
  loadModel()
  jQuery('#uuid').on 'change', ->
    loadModel()


  jQuery('#metadata-link').on 'click', (evt) ->
    evt.preventDefault()
    modal = new Views.ModalWrapper(new Views.MetadataEditView(model: content), 'Edit Metadata')
    modal.show()

  jQuery('#roles-link').on 'click', (evt) ->
    evt.preventDefault()
    modal = new Views.ModalWrapper(new Views.RolesEditView(model: content), 'Edit Roles')
    modal.show()
