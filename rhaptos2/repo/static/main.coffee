define ['jquery', 'model/tools'], (jQuery, Tools) ->

  # HACK to discourage people from using the global jQuery
  # and instead use the requirejs version.
  # This helps ensure plugins that extend jQuery (like bootstrap, jquery-ui, tagit)
  # are properly listed as dependencies in requirejs' `define`
  @jQuery = @$ = ->
    console.warn 'You should add "jquery" to your dependencies in define() instead of using the global jQuery!'
    jQuery.apply @, arguments
  jQuery.extend(@jQuery, jQuery)


  # Build a Model for the current content:
  # TODO: Use backbone routes to figure out the current content

  content = null
  loadModel = ->
    uuid = jQuery('#uuid').val()
    if uuid
      content = new Tools.Module(id: uuid, url: "/module/#{uuid}")
      content.fetch()
    else
      content = new Tools.Module()
  loadModel()
  jQuery('#uuid').on 'change', ->
    loadModel()


  jQuery('#metadata-link').on 'click', (evt) ->
    evt.preventDefault()
    modal = new Tools.ModalWrapper(new Tools.MetadataEditView(model: content), 'Edit Metadata')
    modal.show()

  jQuery('#roles-link').on 'click', (evt) ->
    evt.preventDefault()
    modal = new Tools.ModalWrapper(new Tools.RolesEditView(model: content), 'Edit Roles')
    modal.show()
