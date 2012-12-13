// Generated by CoffeeScript 1.3.3
(function() {

  define(['backbone', 'jquery', 'mustache', 'atc/templates', 'atc/lang', 'bootstrap', 'tagit'], function(Backbone, jQuery, Mustache, Templates, Languages) {
    var KEYWORDS_URL, LANGUAGES, METADATA_SUBJECTS, MODAL_SPINNER_OPTIONS, Metadata, MetadataEditView, ModalWrapper, RolesEditView, USERS_URL, initTagit, languageCode, value, _ref;
    this.jQuery = this.$ = function() {
      console.warn('You should add "jquery" to your dependencies in define instead of using the global jQuery!');
      return jQuery.apply(this, arguments);
    };
    KEYWORDS_URL = '/keywords';
    USERS_URL = '/users';
    METADATA_SUBJECTS = ["Arts", "Mathematics and Statistics", "Business", "Science and Technology", "Humanities", "Social Sciences"];
    MODAL_SPINNER_OPTIONS = {
      lines: 13,
      length: 16,
      width: 6,
      radius: 27,
      corners: 1,
      rotate: 0,
      color: '#444',
      speed: 0.9,
      trail: 69,
      shadow: false,
      hwaccel: false,
      className: 'spinner',
      zIndex: 2e9,
      top: 'auto',
      left: '265px'
    };
    LANGUAGES = [
      {
        code: '',
        "native": '',
        english: ''
      }
    ];
    _ref = Languages.getLanguages();
    for (languageCode in _ref) {
      value = _ref[languageCode];
      value = jQuery.extend({}, value);
      jQuery.extend(value, {
        code: languageCode
      });
      LANGUAGES.push(value);
    }
    initTagit = function($el, tagsLookup) {
      var PLACEHOLDER;
      PLACEHOLDER = jQuery('<span></span>');
      $el.replaceWith(PLACEHOLDER);
      $el.appendTo('body');
      $el.tagit({
        tagSource: tagsLookup,
        sortable: true,
        minLength: 1,
        triggerKeys: ['enter', 'comma', 'tab'],
        initialTags: []
      });
      return PLACEHOLDER.replaceWith($el);
    };
    Metadata = Backbone.Model.extend({
      url: function() {
        return this.get('url');
      }
    });
    MetadataEditView = Backbone.View.extend({
      tagName: 'div',
      className: 'metadata',
      events: {
        'change select[name=language]': '_updateLanguageVariant'
      },
      _updateLanguage: function() {
        var lang, language;
        language = this.model.get('language') || '';
        lang = language.split('-')[0];
        this.$el.find("select[name=language] option[value=" + lang + "]").attr('selected', true);
        return this._updateLanguageVariant();
      },
      _updateLanguageVariant: function() {
        var $language, $variant, code, lang, language, template, variant, variants, _ref1, _ref2;
        $language = this.$el.find('select[name=language]');
        language = this.model.get('language') || '';
        _ref1 = language.split('-'), lang = _ref1[0], variant = _ref1[1];
        if ($language.val() !== lang) {
          lang = $language.val();
          variant = null;
        }
        $variant = this.$el.find('select[name=variantLanguage]');
        variants = [];
        _ref2 = Languages.getCombined();
        for (code in _ref2) {
          value = _ref2[code];
          if (code.slice(0, 2) === lang) {
            jQuery.extend(value, {
              code: code
            });
            variants.push(value);
          }
        }
        if (variants.length > 0) {
          template = '<option value="">None</option>{{#variants}}<option value="{{code}}">{{english}}</option>{{/variants}}';
          $variant.removeAttr('disabled').html(Mustache.to_html(template, {
            'variants': variants
          }));
          return $variant.find("option[value=" + language + "]").attr('selected', true);
        } else {
          return $variant.html('').attr('disabled', true);
        }
      },
      _updateSubjects: function() {
        var subject, _i, _len, _ref1, _results;
        this.$el.find("input[name=subjects]").attr('checked', false);
        _ref1 = this.model.get('subjects') || [];
        _results = [];
        for (_i = 0, _len = _ref1.length; _i < _len; _i++) {
          subject = _ref1[_i];
          _results.push(this.$el.find("input[name=subjects][value='" + subject + "']").attr('checked', true));
        }
        return _results;
      },
      render: function() {
        var $keywords, mustacheObj, tagLookup;
        mustacheObj = jQuery.extend({}, this.model.toJSON());
        mustacheObj._languages = LANGUAGES;
        mustacheObj._subjects = METADATA_SUBJECTS;
        this.$el.append(jQuery(Mustache.to_html(Templates.METADATA, mustacheObj)));
        this._updateLanguage();
        this._updateSubjects();
        $keywords = this.$el.find('#metadata-keywords');
        tagLookup = function(request, response) {
          return jQuery.ajax({
            type: 'GET',
            url: "" + KEYWORDS_URL + "/" + request.term + "*",
            contentType: 'application/json',
            dataType: 'json',
            success: function(data) {
              return response(data);
            }
          });
        };
        initTagit($keywords, tagLookup);
        this.delegateEvents();
        this.$el.find('input[name=title]').focus();
        return this;
      },
      attrsToSave: function() {
        var checkbox, keywords, kw, language, subjects, title, variant;
        title = this.$el.find('input[name=title]').val();
        language = this.$el.find('select[name=language]').val();
        variant = this.$el.find('select[name=variantLanguage]').val();
        if (variant) {
          language = variant;
        }
        subjects = (function() {
          var _i, _len, _ref1, _results;
          _ref1 = this.$el.find('input[name=subjects]:checked');
          _results = [];
          for (_i = 0, _len = _ref1.length; _i < _len; _i++) {
            checkbox = _ref1[_i];
            _results.push(jQuery(checkbox).val());
          }
          return _results;
        }).call(this);
        keywords = (function() {
          var _i, _len, _ref1, _results;
          _ref1 = this.$el.find('#metadata-keywords').tagit('tags');
          _results = [];
          for (_i = 0, _len = _ref1.length; _i < _len; _i++) {
            kw = _ref1[_i];
            _results.push(kw.value);
          }
          return _results;
        }).call(this);
        return {
          title: title,
          language: language,
          subjects: subjects,
          keywords: keywords
        };
      }
    });
    RolesEditView = Backbone.View.extend({
      tagName: 'div',
      className: 'roles',
      render: function() {
        var $authors, $copyrightHolders, mustacheObj, tagLookup;
        mustacheObj = jQuery.extend({}, this.model.toJSON());
        this.$el.append(jQuery(Mustache.to_html(Templates.ROLES, mustacheObj)));
        $authors = this.$el.find('.authors');
        $copyrightHolders = this.$el.find('.copyright-holders');
        tagLookup = function(request, response) {
          return jQuery.ajax({
            type: 'GET',
            url: "" + USERS_URL + "/" + request.term + "*",
            contentType: 'application/json',
            dataType: 'json',
            success: function(data) {
              return response(data);
            }
          });
        };
        initTagit($authors, tagLookup);
        initTagit($copyrightHolders, tagLookup);
        this.delegateEvents();
        return this;
      },
      attrsToSave: function() {
        var authors, copyrightHolders, kw;
        authors = (function() {
          var _i, _len, _ref1, _results;
          _ref1 = this.$el.find('.authors').tagit('tags');
          _results = [];
          for (_i = 0, _len = _ref1.length; _i < _len; _i++) {
            kw = _ref1[_i];
            _results.push(kw.value);
          }
          return _results;
        }).call(this);
        copyrightHolders = (function() {
          var _i, _len, _ref1, _results;
          _ref1 = this.$el.find('.copyright-holders').tagit('tags');
          _results = [];
          for (_i = 0, _len = _ref1.length; _i < _len; _i++) {
            kw = _ref1[_i];
            _results.push(kw.value);
          }
          return _results;
        }).call(this);
        return {
          authors: authors,
          copyrightHolders: copyrightHolders
        };
      }
    });
    ModalWrapper = (function() {

      function ModalWrapper(view, title) {
        var _this = this;
        this.view = view;
        this.$el = jQuery(Templates.MODAL_WRAPPER);
        if (title) {
          this.$el.find('#modal-header-label').append(title);
        }
        this.view.render();
        this.$el.find('.modal-body').html('').append(this.view.$el);
        this.$el.on('click', '.save', function(evt) {
          var attrs;
          evt.preventDefault();
          attrs = _this.view.attrsToSave();
          return _this.view.model.save(attrs, {
            success: function(res) {
              _this.view.model.trigger('sync');
              return _this.$el.modal('hide');
            },
            error: function(res) {
              return alert('Something went wrong when saving: ' + res);
            }
          });
        });
      }

      ModalWrapper.prototype.show = function() {
        return this.$el.modal({
          keyboard: true
        });
      };

      ModalWrapper.prototype.hide = function() {
        return this.$el.modal('hide');
      };

      return ModalWrapper;

    })();
    return {
      Metadata: Metadata,
      ModalWrapper: ModalWrapper,
      MetadataEditView: MetadataEditView,
      RolesEditView: RolesEditView
    };
  });

}).call(this);