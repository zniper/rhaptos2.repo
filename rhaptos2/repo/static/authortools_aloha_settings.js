/**
 * Used to initialize the Aloha settings for this application.
 *
 * Author: Michael Mulich
 * Copyright (c) 2012 Rice University
 *
 * This software is subject to the provisions of the GNU Lesser General
 * Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
 */

Aloha = window.Aloha || {};

Aloha.settings = {
    // jQuery: window.jQuery,
    // logLevels: {'error': true, 'warn': true, 'info': false, 'debug': false},
    // errorhandling : true,
    plugins: {
        draganddropfiles: {
        //     config : {
        //         'drop': {
        //             'max_file_size': '200000',
        //             'upload': {
        //                 'config': {
        //                     'url': '/content/',
        //                     'extra_headers':{'Accept':'application/json'},
        //                     'additional_params': {"location":""},
        //                     'www_encoded': false,
        //                 },
        //             },
        //         },
        //     },
        // },
            upload: {
                config: {
                    method: "POST",
                    url: function() {
                        var url, uid;
                        id = serialise_form().uuid;
                        url = MODULEURL + id + '/upload';
                        return url;
                    },
                    callback: function(resp) {
                        Aloha.jQuery('#' + this.id).attr('src', resp);
                        console.log('Updated Image src as a result of upload');
                    },
                },
            },
        },
        block: {
            defaults : {
                '.default-block': {
                },
                'figure': {
                    'aloha-block-type': 'EditableImageBlock'
                },
            }
        }
    },
};
