/** @odoo-module */
import { registry } from "@web/core/registry";
import { download } from "@web/core/network/download";
import framework from "web.framework";
import session from "web.session";

registry.category("ir.actions.report handlers").add("xlsx", async (action) => {
	if (action.report_type === 'xlsx') {
	    console.log('aaaaa');
    	framework.blockUI();
    	var def = $.Deferred();
    	session.get_file({
        	url: '/xlsx_reports',
        	data: action.data,
        	success: def.resolve.bind(def),
        	error: (error) => this.call('crash_manager', 'rpc_error', error),
        	complete: framework.unblockUI,
    	});
    	return def;
	}
});

//odoo.define('vehicle_rental.action_manager', function (require) {
//"use strict";
///**
// * The purpose of this file is to add the actions of type
// * 'ir_actions_xlsx_download' to the ActionManager.
// */
//var ActionManager = require('web.ActionManager');
//var framework = require('web.framework');
//var session = require('web.session');
//ActionManager.include({
//    _executexlsxReportDownloadAction: function (action) {
//        console.log('aaaaa')
//        framework.blockUI();
//        var def = $.Deferred();
//        session.get_file({
//            url: '/xlsx_reports',
//            data: action.data,
//            success: def.resolve.bind(def),
//            error: (error) => this.call('crash_manager', 'rpc_error', error),
//            complete: framework.unblockUI,
//        });
//        return def;
//    },
//    _handleAction: function (action, options) {
//        if (action.report_type === 'xlsx') {
//            return this._executexlsxReportDownloadAction(action, options);
//        }
//        return this._super.apply(this, arguments);
//
//},
//    });
//  });