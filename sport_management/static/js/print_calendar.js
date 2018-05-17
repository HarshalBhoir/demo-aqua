odoo.define('sport.print_calendar', function (require) {

    "use strict";
    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var framework = require('web.framework');
    var CalendarRenderer = require('web.CalendarRenderer');
    var CalendarController = require('web.CalendarController');
    var _t = core._t;


    CalendarRenderer.include({

        events: _.extend({}, CalendarRenderer.prototype.events, {
            'click .print_planning_btn': '_print_planning',
        }),

        _initSidebar: function () {
            var self = this;
            this._super.apply(this, arguments);
            this.$printBtn = $();
            if(this.model === "sport.session"){
                this.$printBtn = $('<button/>',{type:'button',html:_t("Print calendar")}).addClass('print_planning_btn').appendTo(self.$sidebar);
            }

        },

        _print_planning : function(){

            console.log("print calendar");
        }

    });

});