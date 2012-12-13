define ['jasmine', 'model/tools', 'mockjax-routes'], (jasmine, Tools, MOCK_CONTENT) ->
 j = jasmine.getEnv()
 j.describe 'View :: Metadata', ->
  j.beforeEach ->

    # Configure the mock ajax routes for testing
    @model = new Tools.Metadata()
    @model.set MOCK_CONTENT

    @metadataView = new Tools.MetadataEditView(model: @model)
    @rolesView    = new Tools.RolesEditView(model: @model)

    @metadataModal = new Tools.ModalWrapper(@metadataView, 'Edit Metadata (test)')
    @rolesModal    = new Tools.ModalWrapper(@rolesView, 'Edit Roles (test)')

  j.describe '(Sanity Check) All Views', ->
    j.it 'should have a .$el', ->
      expect(@metadataView.$el ).not.toBeFalsy()
      expect(@rolesView.$el    ).not.toBeFalsy()
      expect(@metadataModal.$el).not.toBeFalsy()
      expect(@rolesModal.$el   ).not.toBeFalsy()
    j.it 'should initially be hidden', ->
      expect(@metadataView.$el.is(':visible')).toEqual false
    j.it 'should show without errors', ->
      expect(@metadataModal.show.bind(@metadataModal)).not.toThrow()
      expect(@metadataModal.hide.bind(@metadataModal)).not.toThrow()
      expect(@rolesModal.show.bind(@rolesModal)      ).not.toThrow()
      expect(@rolesModal.hide.bind(@rolesModal)      ).not.toThrow()
