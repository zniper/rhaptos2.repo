// Copyright (c) Rice University 2012
// This software is subject to 
// the provisions of the GNU Lesser General
// Public License Version 2.1 (LGPL).
// See LICENCE.txt for details.  
//


    var REPOBASEURL = 'http://' + FROZONE.e2repoFQDN;
    var MODULEURL = 'http://' + FROZONE.e2repoFQDN + '/module/';
    var WORKSPACEURL = 'http://' + FROZONE.e2repoFQDN + '/workspace/';



    function logout(msg) {
        //log to a HTML area all messages

        var txt = $('#logarea').html();
        $('#logarea').html(txt + '<li> ' + msg);
        console.log(msg);
    }

    function get_username() {
        return $('#username').val();
    }

    function get_title() {
        var mname = $('#title').val();
        return mname;
    }

function save_validate() {
    var title = get_title();
    if (title = '') {
        jQuery.error('Must have a title');
    }
    return;
}

    function get_textarea_html5() {
        //retrieve, as JSON, the contents of the edit-area
        var txtarea = $('#editarea').html();
        return txtarea;
    }


    function load_textarea(title) {

        var request = $.ajax({
            url: MODULEURL + mhashid,

        xhrFields: {
            withCredentials: true
        }, 
            type: 'GET'
        });

        request.done(function(data) {
            logout(data + 'done a success');
            $('#editarea').html(data);
        });

        request.fail(function(jqXHR, textStatus, err) {
            logout('Request failed: ' + textStatus + ':' + err + ':' + jqXHR.status);
        });

        request.always(function(jqXHR, textStatus) {
            logout(textStatus);
        });
    }


function getLoadHistoryVer(uuid) {
    // ajax request to retrieve module and parse json and load into textarea
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: MODULEURL + uuid,
        xhrFields: {
            withCredentials: true
        },  //http://stackoverflow.com/questions/2870371/why-jquery-ajax-not-sending-session-cookie


        success: function(nodedoc) {
            var title = nodedoc['title'];
            var txtarea = nodedoc['content'];

            var aclrw = nodedoc['aclrw'];
            var contentrw = nodedoc['contentrw'];

            $('#title').val(title);
            $('#aclrw').val(aclrw);
            $('#contentrw').val(contentrw);
            $('#uuid').val(uuid);

            $('#editarea').html(txtarea);
        },

        error: function(jqXHR, textStatus, err) {
            logout('Request failed: ' + textStatus + ':' + err + ':' + jqXHR.status);
        },

        complete: function(jqXHR, textStatus, err) {
            logout('Complete: Request failed: ' + textStatus + ':' + err + ':' + jqXHR.status);
        }


    });
}


function getwhoami() {
    // ajax request
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: REPOBASEURL + '/whoami/',
        xhrFields: {
            withCredentials: true
        },
        //display who I am
        success: function(jsondoc) {

//            for (var i in jsondoc){
//               alert(i);
//            };
            var user_email = jsondoc['email'];
            var user_name = jsondoc['name'];
            $('#usernamedisplay').html(user_name + '-' + user_email);
        },

        error: function(jqXHR, textStatus, err) {
            logout('Request failed: ' + textStatus + ':' + err + ':' + jqXHR.status);
        }

    });
}




function buildHistory() {

    var jsond = "[";
    var htmlfrag = '<ul>';
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: WORKSPACEURL,
        xhrFields: {
            withCredentials: true
        },  //http://stackoverflow.com/questions/2870371/why-jquery-ajax-not-sending-session-cookie

        success: function(historyarr) {
            historyarr.sort();
            $.each(historyarr, function(i, elem) {
                var strelem = "'" + elem[0] + "'";
                htmlfrag += '<li><a class="nolink" href="#" onclick="getLoadHistoryVer(' + strelem + ');" >' + elem[1] + '</a>' + '<a class="nolink" href="#" onclick="delete_module(' + strelem + ');" >(Delete)</a>';
                jsond += '{"data": "' + elem[1] + '", "state": "closed"},';
            });

            x = jsond.length-1;
            y = jsond.substring(0,x);
            jsond = y + "]";     
            //jsond += ']"'; 

            good = '[{"state": "closed", "data": "yyyyy"}, {"state": "closed", "data": "ddd"}]'
            logout(jsond);
            logout(good);

            populate_tree(jsond);
            $('#workspaces').html(htmlfrag);
        }
    });
}

function delete_module(filename) {
    $.ajax({
        type: 'DELETE',
        dataType: 'json',
        url: REPOBASEURL + '/module/' + filename,
        xhrFields: {
            withCredentials: true
        },  //http://stackoverflow.com/questions/2870371/why-jquery-ajax-not-sending-session-cookie

        success: function() {
            logout('deleted ' + filename);
            buildHistory();
        },

        error: function(jqXHR, textStatus, err) {
            logout('Request failed: ' + textStatus + ':' + err + ':' + jqXHR.status);
        }

    });

}

function showres(i, elem) {

    logout(i + ': ' + elem);
}


function serialise_form() {
    // return form1 as object/hasharrary
    var payload = new Object;
    payload['content'] = get_textarea_html5();
    payload['uuid'] = $('#uuid').val();

    payload['aclrw'] = $('#aclrw').val().split(',');

    payload['contentrw'] = $('#contentrw').val().split(',');
    payload['title'] = $('#title').val();

//        var json_text = JSON.stringify(payload, null, 2);
//        return json_text;

    return payload;

}

function newText(){
    $('#aclrw').val(whoami["userID"]);
    $('#contentrw').val(whoami["userID"]);
    $('#title').val('');
    $('#editartea').html('Enter your text here...');        
    alert("you are :" + whoami);
};

function saveText() {
         //constants

         save_validate();

         var requestmethod = 'POST';
         var payload = serialise_form();
         if (payload['uuid'] != '') {
             requestmethod = 'PUT';
         }

         var foo = '';
         for (var i in payload) {
             foo = '/n' + i + ' : ' + payload[i];
         }
         alert(requestmethod);
         alert(foo);

         var json_text = JSON.stringify(payload, null, 2);

         var request = $.ajax({
             url: MODULEURL,
                xhrFields: {
                 withCredentials: true
                },


             type: requestmethod,
             data: json_text,
             contentType: 'application/json; charset=utf-8',
             dataType: 'json'
         });

         request.done(function(data) {
             //$("#responsearea").html(data);
             $.each(data, showres);
             buildHistory();
         });

         request.fail(function(jqXHR, textStatus, err) {
             logout('Request failed: ' + textStatus + ':' + err + ':' + jqXHR.status);
         });

         request.always(function(jqXHR, textStatus) {
             logout(textStatus);
         });

    }

function opendialog(dia) {

   $(dia).dialog('open');

}

function test() {

    //alert(whoami.identity_url + "/n" +
    //      whoami.name + "/n" +
    //      whoami.email);
    var s = '#dialog';
    $(s).dialog('open');

}


function start_aloha() {

    $('#editarea').aloha();
    logout('started aloha');
}

function start_tree() {

var data = [
 {
 'data' : 'weekly',
 'attr': {'rel': 'directory'}
 }];

    $('#coltree').jstree({
            json_data: {data: data},
            plugins: ['themes', 'json_data', 'ui', 'crrm', 'hotkeys'],
            core: { }

                         });
}

function populate_tree(jsonstr) {

    logout(jsonstr);
    x = $.parseJSON(jsonstr);

    var jsTreeSettings = $('#coltree').jstree('get_settings');
    jsTreeSettings.json_data.data = x; //$.parseJSON(jsonstr);
    $.jstree._reference('coltree')._set_settings(jsTreeSettings);

    // Refresh whole our tree (-1 means root of tree)
    $.jstree._reference('coltree').refresh(-1);
}




$(document).ready(function() {

    start_aloha();

    //mark dialog areas as dialog but not shown
    var dialogs = ['#dialog_files', '#dialog_metadata',
                   '#dialog_roles', '#dialog_links',
                   '#dialog_links', '#dialog_preview',
                   '#dialog_publish'];
    $.each(dialogs, function(i, v) {
//        alert(i + ":" + v);
        $(v).dialog({ autoOpen: false });
    });


    //bind various clicks
    $('#testclick').click(function(e) {test();
                                      e.preventDefault()});


    $('#clickLoadTextArea').click(function(e) {load_textarea();
                                              e.preventDefault()});



    logout('AJAX will fire at ' + MODULEURL);

    getwhoami();


    start_tree();
//    var d = '{"data": "title",' +
//            '"state": "closed"}';

//    populate_tree(d);

    buildHistory();

    //nolink are links that do some jquery function, but should not be links
    $('a.nolink').click(function(event) {
        logout('click-preventDefault');
        event.preventDefault();




    });

    $('#savemodule').click(function(event) {
                         saveText();
                         event.preventDefault();
                       }
                      );



    $('#newmodule').click(function(event) {
                         newText();
                         event.preventDefault();
                       }
                      );


});
