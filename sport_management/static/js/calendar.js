window.onload = init;

function init() {
    // launching calendar function
    calendar_printer();
}

function calendar_printer() {

    if (sessionStorage.getItem('alert')) {
        var data = JSON.parse(sessionStorage.getItem('data'));
        if (data.error) {
            $('#danger-msg').html(data.msg);
            $('#danger-msg').parent().closest('div').css('display', 'block');
        } else if (data.warning) {
            $('#warning-msg').html(data.msg);
            $('#warning-msg').parent().closest('div').css('display', 'block');
        } else {
            $('#success-msg').html(data.msg);
            $('#success-msg').parent().closest('div').css('display', 'block');
        }
        sessionStorage.clear();
    }

    odoo.define('sport.my_js', function (require) {
        'use strict';
        // loading odoo ressources
        var rpc = require('web.rpc');
        var weContext = require('web_editor.context');
        var ajax = require('web.ajax');
        var usession = require('web.session');
        var activity_ids = [];
        var sessions = [];
        var session_ids = [];

        // we are loading all courses with odoo rpc api
        rpc.query({
            model: 'sport.activity',
            // method: 'search_read',
            method: 'search_activites',
            context: weContext.get(),
        }).then(function (data) {
            JSON.parse(data).forEach(function (activity_id) {
                $('#slt_course').append('<option value="' + activity_id.id + '">' + activity_id.name + '</option>');
                activity_id.session_ids.forEach(function (session_id) {
                    session_id.subscription_ids.forEach(function (subscription_id) {
                        if (subscription_id.client_id == usession.user_id) {
                            switch (subscription_id.state) {
                                case 'sub':
                                    session_id.color = '#35b0c6';
                                    session_id['state'] = 'sub';
                                    session_id['msg'] = 'Are you sure you want to <b>unsubscribe</b> for this activity ?';
                                    break;
                                case 'valid':
                                    session_id.color = 'green';
                                    session_id['state'] = 'valid';
                                    session_id['msg'] = 'This session has passed. You can\'t you unsubscribe.';
                                    break;
                                case 'canceled':
                                    session_id.color = 'gray';
                                    session_id['state'] = 'canceled';
                                    session_id['msg'] = 'Are you sure you want to <b>subscribe</b> for this activity ?';
                                    break;
                                case 'waiting':
                                    session_id.color = 'orange';
                                    session_id['state'] = 'waiting';
                                    session_id['msg'] = 'Are you sure you want to <b>unsubscribe</b> for this activity ?';
                                    break;
                                case 'absent':
                                    session_id.color = 'red';
                                    session_id['state'] = 'absent';
                                    session_id['msg'] = 'This session has passed. You can\'t you unsubscribe.';
                                    break;
                            }
                        }
                    });
                    session_ids.push(session_id);
                });
                activity_ids.push(activity_id);
            });

            // init calendar
            $('#calendar').fullCalendar({
                height: 650,
                themeSystem: 'bootstrap4',
                weekNumbers: true,
                locale: 'fr',
                header: {
                    left: 'prev,today,next',
                    center: 'title',
                    right: 'years,month,agendaWeek,agendaDay,listWeek'
                },
                editable: false,
                events: session_ids,
                timeFormat: 'HH:mm',
                eventClick: function (event) {

                    // Get informations of event (day, date, hours start and end
                    var tb_day_str = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
                    var activity = event.title;
                    var day = tb_day_str[event.start._d.getUTCDay()];
                    var hours_start = event.start._d.getUTCHours() + ':' + event.start._d.getUTCMinutes();
                    var hours_end = event.end._d.getUTCHours() + ':' + event.end._d.getUTCMinutes();
                    var msg = event.msg ? event.msg : 'Are you sure you want to <b>subscribe</b> for this activity ?';

                    // Exit function if event is outdated
                    if (Date.now() > event.start) {
                        return;
                    }

                    if (event.state != 'absent' | event.state != 'valid') {
                        console.log('test');
                        // Add message in dialog box.
                        $('#dialog-msg').html(msg);
                        $('#selected-activity').html(
                            '<b>activity : </b>' + activity + '<br /><b>On : </b>' + day + '<br /><b>At : </b>' + hours_start + ' - ' + hours_end
                        );
                        $('#dialog-confirm').dialog({
                            resizable: false,
                            height: 'auto',
                            width: 400,
                            modal: true,
                            buttons: {
                                'Yes': function () {
                                    ajax.jsonRpc('/sport/sessions/subscribe', 'call', {
                                        'user_id': usession.user_id,
                                        'session_id': event.id,
                                        'unsubscribe': false
                                    }).then(function (data) {
                                        sessionStorage.clear();
                                        sessionStorage.setItem('alert', true);
                                        sessionStorage.setItem('data', JSON.stringify(data));
                                    });
                                    $(this).dialog('close');
                                    location.reload();
                                },
                                Cancel: function () {
                                    $(this).dialog('close');
                                }
                            }
                        });
                    } else {
                        $('#danger-msg').html(event.msg);
                        $('#danger-msg').parent().closest('div').css('display', 'block');
                    }
                }
            });
        });
    });
}