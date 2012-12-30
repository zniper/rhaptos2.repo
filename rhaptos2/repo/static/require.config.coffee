# Configure paths to all the JS libs
require.config

  # Since `master.html` is served from `/` we need to set the base to the static dir
  # This should probably become `/static/`
  baseUrl: 'static/'
  urlArgs: '' # If you want to force a reload every time use this: `cb=#{Math.random()}` (you lose JS breakpoints though)

  # # Configure Library Locations
  paths:
    i18n: 'i18n-custom'
    text: 'lib/require-text/text'
    json: 'lib/requirejs-plugins/json'

    # ## Core Libraries
    jquery: 'lib/jquery-1.8.3'
    underscore: 'lib/underscore-1.4.3'
    backbone: 'lib/backbone-0.9.9'

    # ## UI libraries
    'aloha': '../cdn/aloha/src/lib/aloha' # FIXME: Remove the '/cdn/' when aloha is moved into static/
    bootstrap: 'lib/bootstrap/js/bootstrap'
    select2: 'lib/select2/select2'
    spin: 'lib/spin'

    # ## Handlebars modules
    # The requirejs plugin to support handlebars has several dependencies
    # that need to be loaded
    hbs: 'lib/require-handlebars-plugin/hbs'
    handlebars: 'lib/require-handlebars-plugin/Handlebars'
    i18nprecompile: 'lib/require-handlebars-plugin/hbs/i18nprecompile'
    json2: 'lib/require-handlebars-plugin/hbs/json2'

  # # Shims
  # To support libraries that were not written for requirejs
  # configure a shim around them that mimics a `define` call.
  # List the dependencies and what global object is available
  # when the library is done loading (for jQuery plugins this can be `jQuery`)
  shim:

    # ## Core Libraries
    jquery:
      exports: 'jQuery'
      init: -> # this.jQuery.noConflict(true)

    underscore:
      exports: '_'

    backbone:
      deps: ['underscore', 'jquery']
      exports: 'Backbone'

    'backbone.layoutmanager':
      deps: ['underscore', 'backbone']
      exports: 'Backbone'

    'backbone.marionette':
      deps: ['underscore', 'backbone']
      exports: 'Backbone'
      init: -> ret = @Backbone; delete @Backbone; delete @_; ret

    # ## UI Libraries
    bootstrap:
      deps: ['jquery'] # For some reason we can't add use 'css!lib/bootstrap/css/bootstrap'
      exports: 'jQuery'

    select2:
      deps: ['jquery', 'css!./select2']
      exports: 'Select2'
      init: -> ret = @Select2; delete @Select2; ret

    aloha:
      deps: ['jquery', 'css!../cdn/aloha/src/css/aloha']
      exports: 'Aloha'

  # Maps prefixes (like `less!path/to/less-file`) to use the LESS CSS plugin
  map:
    '*':
      text: 'lib/require-text'
      css: 'lib/require-css/css'
      less: 'lib/require-less/less'
      json: 'lib/requirejs-plugins/src/json'

  # ## module Configuration
  # This configures `requirejs` plugins and modules.
  # Modules can get to the configuration by including the `module` dependency
  # and then calling `module.config()`
  hbs:
    disableI18n: true

# requirejs special-cases jQuery and allows it to be a global (doesn't call the init code below to clean up the global vars)
# To stop it from doing that, we need to delete this property
#
# unlike the other jQuery plugins bootstrap depends on a global '$' instead of 'jQuery'
#
#`delete define.amd.jQuery`
