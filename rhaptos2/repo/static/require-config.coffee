# Configure paths to all the JS libs
require.config

  # If set to true, an error will be thrown if a script loads that does not call define() or have a shim exports string value that can be checked. See Catching load failures in IE for more information.
  enforceDefine: true

  #urlArgs: "cb=#{Math.random()}" # Cache Buster
  paths:
    jquery: 'lib/jquery-1.8.3'
    underscore: 'lib/underscore-1.4.3'
    backbone: 'lib/backbone-0.9.2'

    # # Libraries used for testing
    jasmine: 'lib/jasmine/jasmine'
    'jasmine-html': 'lib/jasmine/jasmine-html'
    'jquery-mockjax': 'lib/jquery.mockjax'
    # Our unit tests
    spec: 'tests/spec'

    # # UI libraries
    'aloha': '../cdn/aloha/src/lib/aloha' # FIXME: Remove the '/cdn/' when aloha is moved into static/
    bootstrap: 'lib/bootstrap/js/bootstrap'
    mustache: 'lib/mustache'
    select2: 'lib/select2/select2'
    spin: 'lib/spin'

  shim:
    jquery:
      exports: 'jQuery'
      # init: -> this.jQuery.noConflict(true)
    bootstrap:
      deps: ['jquery']
      exports: 'jQuery'

    underscore:
      exports: '_'

    backbone:
      deps: ['underscore', 'jquery']
      exports: 'Backbone'
      init: -> ret = @Backbone; delete @Backbone; ret

    mustache:
      exports: 'Mustache'
      init: -> ret = @Mustache; delete @Mustache; ret

    select2:
      deps: ['jquery']
      exports: 'Select2'
      init: -> ret = @Select2; delete @Select2; ret

    'spec/routes':
      deps: ['jquery']
      init: -> true

    'aloha':
      deps: ['jquery']
      exports: 'Aloha'

    # # Modules used for testing (maybe they should be in a separate require-config)
    jasmine:
      exports: 'jasmine'

    'jasmine-html':
      deps: ['jasmine']
      exports: 'jasmine'

    'jquery-mockjax':
      deps: ['jquery']
      exports: 'jQuery'

# requirejs special-cases jQuery and allows it to be a global (doesn't call the init code below to clean up the global vars)
# To stop it from doing that, we need to delete this property
#
# unlike the other jQuery plugins bootstrap depends on a global '$' instead of 'jQuery'
#delete define.amd.jQuery
