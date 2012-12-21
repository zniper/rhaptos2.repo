# Need to define a name for this module that matches the requirejs data-main attribute.
define 'Sandbox', ['jquery', 'model/tools', 'mockjax-routes'], ($, Tools, MOCK_CONTENT) =>
  model = new Tools.Content()
  model.set MOCK_CONTENT
  metadataView = new Tools.MetadataEditView {model: model}
  rolesView    = new Tools.RolesEditView {model: model}

  metadataModal = new Tools.ModalWrapper(metadataView, 'Edit Metadata (test)')
  rolesModal    = new Tools.ModalWrapper(rolesView, 'Edit Roles (test)')

  # Log when model changes are saved (not changed)
  model.on 'sync', ->
    console.log 'Model Saved!', @
    alert "Model Saved!\n#{JSON.stringify(@)}"

  $('.show-metadata').on 'click', => metadataModal.show()
  $('.show-roles'   ).on 'click', => rolesModal.show()
