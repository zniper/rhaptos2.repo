# # Page Controllers
#
# This module sets up page regions (ie header, footer, sidebar, etc),
# route listeners, and updates the URL and DOM with the correct views
#
# This makes it easier in other parts of the code to 'Go back to the Workspace'
# or "Edit this content" when clicking on a link.
define [
  'jquery'
  'backbone'
  'marionette'
  'app/models'
  # There is a cyclic dependency between views and controllers
  # So we use the `exports` module to get around that problem.
  'app/views'
  'exports'
  'i18n!app/nls/strings'
], (jQuery, Backbone, Marionette, Models, Views, exports, __) ->

  # The main Region used for layouts
  mainRegion = new Marionette.Region
    el: '#main'

  # ## Main Controller
  # Changes all the regions on the page to begin editing a new/existing
  # piece of content.
  #
  # If another part of the code wants to create/edit content
  # it should call these methods instead of changing the URL directly.
  # (depending on the browser the URLs could start with a hash so anchor links won't work)
  #
  # Methods on this object can be called directly and will update the URL.
  mainController =
    # Begin monitoring URL changes and match the current route
    # In here so App can call it once it has completed loading
    start: -> Backbone.history.start()

    # ### Show Workspace
    # Shows the workspace listing and updates the URL
    workspace: ->
      # List the workspace
      workspace = new Models.Workspace()
      workspace.fetch()
      view = new Views.WorkspaceView {collection: workspace}
      mainRegion.show view
      # Update the URL
      Backbone.history.navigate ''

      workspace.on 'change', ->
        view.render()

    # ### Create new content
    # Calling this method directly will start editing a new piece of content
    # and will update the URL
    createContent: ->
      content = new Models.Content()
      @_editContent content
      # Update the URL
      Backbone.history.navigate 'content'

    # ### Edit existing content
    # Calling this method directly will start editing an existing piece of content
    # and will update the URL.
    editContent: (id) ->
      content = new Models.Content()
      content.set 'id', id
      content.fetch()
      # **FIXME:** display a spinner while we fetch the content and then call `@_editContent`
      @_editContent content
      # Update the URL
      Backbone.history.navigate "content/#{id}"

    # Internal method that updates the metadata/roles links so they
    # refer to the correct Content Model
    _editContent: (content) ->
      # ## Bind UI Popups
      # This section generates the UI menus and buttons
      #
      # **FIXME:** Remove the buttons from the global toolbar
      # so we don't have to perform this hackish code.
      #
      # `__()` is a i18n function that looks up a localized string
      jQuery('#metadata-link').off 'click'
      jQuery('#roles-link').off 'click'

      jQuery('#metadata-link').on 'click', (evt) ->
        view = new Views.MetadataEditView {model: content}
        modal = new Views.ModalWrapper(view, __('Edit Metadata'))
        modal.show()

      jQuery('#roles-link').on 'click', (evt) ->
        view = new Views.RolesEditView {model: content}
        modal = new Views.ModalWrapper(view, __('Edit Roles'))
        modal.show()

      view = new Views.ContentEditView(model: content)
      mainRegion.show view


  # ## Bind Routes
  ContentRouter = Marionette.AppRouter.extend
    controller: mainController
    appRoutes:
      '':             'workspace' # Show the workspace list of content
      'content':      'createContent' # Create a new piece of content
      'content/:id':  'editContent' # Edit an existing piece of content

  # Start listening to URL changes
  new ContentRouter()

  # Because of cyclic dependencies we tack on all of the
  # controller methods onto the exported object instead of
  # just returning the controller object
  jQuery.extend(exports, mainController)
