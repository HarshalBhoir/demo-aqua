odoo.define('pos_discount_amount.pos.models.amount', function (require) {
"use strict";

var models = require('point_of_sale.models');
var utils = require('web.utils');
// var formats = require('web.formats');
var round_di = utils.round_decimals;
var round_pr = utils.round_precision;

// Extending order line
var _super_orderline = models.Orderline.prototype;
models.Orderline = models.Orderline.extend({
    initialize: function(attr, options) {
        _super_orderline.initialize.call(this, attr, options);
		this.pack=null;
		this.get_pack();
    },
	
	get_pack:function(){
		console.log(this);
		var params = {
			"args":[],
			"kwargs":{
				"context":{"lang":"fr_FR","tz":false,"uid":1},
				"domain":[["id","=",this.product.product_tmpl_id]],
				"fields":["is_pack","pack_ids"],
			},
			"method":"search_read",
			"model":"product.template"
		};
		var url = "http://localhost:8069/web/dataset/call_kw/product.template/search_read";
		console.log(this.pos._previousAttributes.rpc(url,params));
		var thise = this;
		var a = this.pos._previousAttributes.rpc(url,params).then(
			function(val) {
				thise.pack = val[0];
			});
	},
	
	get_product_name:function(id){		
		return this.pos.db.product_by_id[id].display_name;
	},
	
});
});

