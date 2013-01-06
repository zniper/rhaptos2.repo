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
  'hbs!app/layout-content'
  'exports'
  'i18n!app/nls/strings'
], (jQuery, Backbone, Marionette, Models, Views, LAYOUT_CONTENT, exports, __) ->

  # Squirrel away the original contents of the main div (content HTML when viewing the content page for example)
  $main = jQuery('#main')
  $originalContents = $main.contents()
  $main.empty()

  mainRegion = new Marionette.Region
    el: '#main'

  ContentLayout = Marionette.Layout.extend
    template: LAYOUT_CONTENT
    regions:
      body:         '#body'
      sidebar:      '#sidebar'
      sidebarRight: '#sidebar-right'
      aboveBody:    '#body-above'
      # Specific to content
      metadata: '#metadata'
      roles: '#roles'
  contentLayout = new ContentLayout()

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
      mainRegion.show contentLayout
      contentLayout.body.show view
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
      # **FIXME:** display a spinner while we fetch the content and then call `@_editContent`
      content.fetch
        error: => alert "Problem getting content #{id}"
        success: =>
          @_editContent content
          # Update the URL
          Backbone.history.navigate "content/#{id}"


    # Internal method that updates the metadata/roles links so they
    # refer to the correct Content Model
    _editContent: (content) ->
      # ## Bind Metadata Dialogs
      mainRegion.show contentLayout

      configAccordionDialog = (region, view) ->
        dialog = new Views.DialogWrapper {view: view}
        region.show dialog
        # When save/cancel are clicked collapse the accordion
        dialog.on 'saved',     => region.$el.parent().collapse 'hide'
        dialog.on 'cancelled', => region.$el.parent().collapse 'hide'

      # Set up the metadata dialog
      configAccordionDialog contentLayout.metadata, new Views.MetadataEditView {model: content}
      configAccordionDialog contentLayout.roles,    new Views.RolesEditView {model: content}

      view = new Views.ContentEditView(model: content)
      contentLayout.body.show view


  # ## Bind Routes
  ContentRouter = Marionette.AppRouter.extend
    controller: mainController
    appRoutes:
      '':             'workspace' # Show the workspace list of content
      'content':      'createContent' # Create a new piece of content
      'content/:id':  'editContent' # Edit an existing piece of content

    routes:
      '_layout':  'showLayout'

    showLayout: ->
      DesignView = Backbone.View.extend
        render: ->
          @$el.css {border: '1px dotted', 'background-color': '#ccc'}
          @$el.css @options.css
          @$el.text @options.name
      mainRegion.show contentLayout
      contentLayout.body.show new DesignView {name:'body', css: {height: '100em'}}
      contentLayout.sidebar.show new DesignView {name:'sidebar', css: {height: '10em'}}
      contentLayout.sidebarRight.show new DesignView {name:'sidebar-right', css: {height: '10em'}}
      contentLayout.aboveBody.show new DesignView {name:'above-body', css: {height: '5em'}}

  # Start listening to URL changes
  new ContentRouter()

  # Because of cyclic dependencies we tack on all of the
  # controller methods onto the exported object instead of
  # just returning the controller object
  jQuery.extend(exports, mainController)
