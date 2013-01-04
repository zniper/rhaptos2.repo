define ['backbone'], (Backbone) ->
  models = {}

  # **FIXME:** The URL prefix to content and the workspace should be `/content` instead of `/module` and `/workspace`
  CONTENT_PREFIX = '/module' # Should be '/content'
  WORKSPACE_PREFIX = '/workspace/' # Should be '/content'

  # Default language for new content is the browser's language
  browserLanguage = (navigator.userLanguage or navigator.language or '').toLowerCase() if navigator

  # This model contains the following members:
  #
  # * `title` - a text title of the content
  # * `language` - the main language (eg `en-us`)
  # * `subjects` - an array of strings (eg `['Mathematics', 'Business']`)
  # * `keywords` - an array of keywords (eg `['constant', 'boltzmann constant']`)
  # * `authors` - an `Collection` of `User`s that are attributed as authors
  models.Content = Backbone.Model.extend
    defaults:
      language: browserLanguage
    url: -> "#{CONTENT_PREFIX}/#{@get 'id'}"
    validate: (attrs) ->
      return 'ERROR_EMPTY_BODY' if attrs.body and 0 == attrs.body.trim().length

  models.SearchResultItem = Backbone.Model.extend
    defaults:
      type: 'BUG_UNSPECIFIED_TYPE'
      title: 'BUG_UNSPECIFIED_TITLE'

  models.Workspace = Backbone.Collection.extend
    model: models.SearchResultItem
    url: WORKSPACE_PREFIX

  return models
