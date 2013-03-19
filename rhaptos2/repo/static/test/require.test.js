
// <!--
// Copyright (c) Rice University 2012-3
// This software is subject to
// the provisions of the GNU Affero General
// Public License Version 3 (AGPLv3).
// See LICENCE.txt for details.
// -->


(function() {

  require.config({
    baseUrl: '../',
    enforceDefine: true,
    paths: {
      jasmine: 'lib/jasmine/jasmine',
      'jasmine-html': 'lib/jasmine/jasmine-html',
      'jquery-mockjax': 'lib/jquery.mockjax'
    },
    shim: {
      jasmine: {
        exports: 'jasmine'
      },
      'jasmine-html': {
        deps: ['jasmine'],
        exports: 'jasmine'
      },
      'jquery-mockjax': {
        deps: ['jquery'],
        exports: 'jQuery'
      }
    },
    config: {
      i18n: {
        warn: true
      }
    }
  });

}).call(this);

