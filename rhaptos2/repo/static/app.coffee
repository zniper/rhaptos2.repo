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
define [
  'jquery'
  'underscore'
  'backbone'
  'marionette'
  'aloha'
  'app/models'
  'app/views'
  'i18n!app/nls/strings'
  'css!app'
], (jQuery, _, Backbone, Marionette, Aloha, Models, Views, __) ->

  # # Various HACKS
  # These should be removed when the webserver URLs/routes are cleaned up

  # **HACK:** to discourage people from using the global jQuery
  # and instead use the `requirejs` version.
  # This helps ensure plugins that extend jQuery (like bootstrap)
  # are properly listed as dependencies in requirejs' `define`
  @jQuery = @$ = ->
    console.warn 'You should add "jquery" to your dependencies in define() instead of using the global jQuery!'
    jQuery.apply @, arguments
  jQuery.extend(@jQuery, jQuery)


  # **FIXME:** By default Backbone sends the JSON object as the body when a PUT is called.
  # Instead, send each key/value as a PUT parameter
  Backbone_sync_orig = Backbone.sync
  Backbone.sync = (method, model, options) =>
    if 'update' == method
      data = _.extend {}, model.toJSON()
      # **FIXME:** This URL (and the funky data.json param) is a HACK and should be fixed
      data.json = JSON.stringify(model)
      href = options['url'] or model.url() or throw 'URL to sync to not defined'
      href = "#{href}?#{jQuery.param(model.toJSON())}"

      params =
        type: 'PUT'
        url: href
        data: JSON.stringify(model)
        processData: false
        dataType: 'json'
        contentType: 'application/json'

      jQuery.ajax(_.extend(params, options))
    else
      Backbone_sync_orig method, model, options


  # # Application Code
  # The Single Page Application starts here


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
  contentController =
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
      # FIXME: display a spinner while we fetch the content and then call @_editContent
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
    controller: contentController
    appRoutes:
      '':             'workspace' # Show the workspace list of content
      'content':      'createContent' # Create a new piece of content
      'content/:id':  'editContent' # Edit an existing piece of content

  new ContentRouter()
  Backbone.history.start()

  # All navigation that is relative should be passed through the navigate
  # FIXME: display a spinner while we fetch the content and then call @_editContent
  # method, to be processed by the router. If the link has a `data-bypass`
  # attribute, bypass the delegation completely.
  jQuery(document).on 'click', 'a:not([data-bypass])', (evt) ->
    # Get the absolute anchor href.
    href = $(@).attr('href')

    # If the href exists and is a hash route, run it through Backbone.
    if href
      # Stop the default event to ensure the link will not cause a page
      # refresh.
      evt.preventDefault()

      # `Backbone.history.navigate` is sufficient for all Routers and will
      # trigger the correct events. The Router's internal `navigate` method
      # calls this anyways.
      Backbone.history.navigate(href, true)
