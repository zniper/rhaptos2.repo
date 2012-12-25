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


# ## FIXME Section
# This next define (with a random name) is a HACK so
# the toolbar is inserted into the DOM before Aloha's toolbar plugin loads
# It's a nasty, nasty hack and the Aloha Toolbar code should be fixed
# so one can programmatically retreive the actions for buttons and bind them
# to toolbar buttons.
$toolbar = null
HACK_LOAD_TOOLBAR_BEFORE_ALOHA = "__app_intenral_#{Math.random()}"
define HACK_LOAD_TOOLBAR_BEFORE_ALOHA, [
  'hbs!app/views/aloha-toolbar'
], (ALOHA_TOOLBAR) ->
  $toolbar = jQuery(ALOHA_TOOLBAR {}).appendTo('body').find('div').hide()


define [
  'jquery'
  'underscore'
  'backbone'
  'aloha'
  'app/models'
  'app/views'
  HACK_LOAD_TOOLBAR_BEFORE_ALOHA # 'hbs!app/views/aloha-toolbar'
  'i18n!app/nls/strings'
  'css!app'
], (jQuery, _, Backbone, Aloha, Models, Views, ALOHA_TOOLBAR, __) ->


  # **HACK:** to discourage people from using the global jQuery
  # and instead use the `requirejs` version.
  # This helps ensure plugins that extend jQuery (like bootstrap)
  # are properly listed as dependencies in requirejs' `define`
  @jQuery = @$ = ->
    console.warn 'You should add "jquery" to your dependencies in define() instead of using the global jQuery!'
    jQuery.apply @, arguments
  jQuery.extend(@jQuery, jQuery)

  # Clear the main gunk and add in the toolbar so Aloha can bind actions to it
  $main = jQuery('#main').empty() # FIXME: make it so the webserver doesn't send this
  # FIXME This is where the toolbar would have been defined if we didn't need the toolbar load hack.
  # Commented because of HACK_LOAD_TOOLBAR_BEFORE_ALOHA
  #$toolbar = jQuery(ALOHA_TOOLBAR {}).appendTo('body').find('div').hide()


  # # Bind Routes
  AppRouter = Backbone.Router.extend
    routes:
      '':       'index'
      'module/:uuid': 'module'
    # Display the workspace
    index: ->
      # List the workspace
      # TODO: This should be a Backbone.Collection fetch
      workspace = new Models.Workspace()
      workspace.fetch()
      view = new Views.WorkspaceView {model: {items: workspace}}
      $main.html('')
      $main.html(view.$el)
      view.render()

      workspace.on 'change', ->
        view.render()


    # Create a new module or edit an existing one
    module: (id=null) ->
      if id
        module = new Models.Module(id: id, url: "/module/#{id}/metadata/")
        module.fetch()
      else
        module = new Models.Module()

      # ## Bind UI Popups
      # This section generates the UI menus and buttons
      #
      # `__()` is a i18n function that looks up a localized string
      jQuery('#metadata-link').off 'click'
      jQuery('#roles-link').off 'click'

      jQuery('#metadata-link').on 'click', (evt) ->
        evt.preventDefault()
        modal = new Views.ModalWrapper(new Views.MetadataEditView(model: module), __('Edit Metadata'))
        modal.show()

      jQuery('#roles-link').on 'click', (evt) ->
        evt.preventDefault()
        modal = new Views.ModalWrapper(new Views.RolesEditView(model: module), __('Edit Roles'))
        modal.show()


      # show the toolbar and start up an editor
      module.on 'change', ->
        body = """
          <h1>Module body</h1>
          <p>This is sample body text for module #{id}.</p>
          <p>It'll eventually get loaded dynamically</p>
        """
        $main.html(body) # main.html(module.get('body'))
        $toolbar.show()

        # ## Start Aloha
        # Once Aloha has finished loading, enable it on the document and let MathJax know it can start rendering
        Aloha.ready ->
          $main.aloha().focus()

          # Wait until Aloha is started before loading MathJax
          # Also, wrap all math in a span/div. MathJax replaces the MathJax element
          # losing all jQuery data attached to it (like popover data, the original Math Formula, etc)
          # Add `aloha-cleanme` so this span is unwrapped when serialized to XHTML
          $main.find('math').wrap '<span class="math-element aloha-cleanme"></span>'
          MathJax.Hub.Configured()


  appRouter = new AppRouter()
  x = Backbone.history.start()

  # All navigation that is relative should be passed through the navigate
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
