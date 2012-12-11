describe 'View :: RolesModal', ->
  beforeEach ->
    flag = false
    that = this


    require ['jquery', 'atc/tools'], ($, Tools) ->
      #that.view = new View({collection: that.todos});
      that.$ = $
      that.view = new Tools.RolesModal()
      that.mockData = language: null
      $('#sandbox').html that.view.render(that.mockData).el
      flag = true

    waitsFor ->
      flag


  afterEach ->
    #this.view.remove();

  describe 'Defaults', ->
    it 'should initially be hidden', ->
      expect(@view.$el.is(':visible')).toEqual false
