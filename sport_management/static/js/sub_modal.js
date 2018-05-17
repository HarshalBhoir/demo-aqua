//file that manage the modal to cancel a subscription
odoo.define('sport.modal_unsub', function (require) {

    var rpc = require('web.rpc');
    var weContext = require('web_editor.context');
    var ajax = require('web.ajax');
    var usession = require('web.session');

    //triggered on click on cancel button
    $(document).on("click", ".cancel_sub", function () {
        var self = $(this);
        var sub_id = self.attr('id');
        console.log(sub_id);

        ajax.jsonRpc('/sport/sessions/subscribe', 'call', {
            'user_id': usession.user_id,
            'session_id': sub_id,
            'unsubscribe': false
        }).then(function (data) {
            console.log(data);
        });
    })

});
