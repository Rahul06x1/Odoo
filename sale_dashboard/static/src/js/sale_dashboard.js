odoo.define('sale_dashboard.Dashboard', function (require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
const { loadBundle } = require("@web/core/assets");
var ajax = require('web.ajax');
//var field_utils = require('web.field_utils');
//var pyUtils = require('web.py_utils');
var session = require('web.session');
//var time = require('web.time');
var web_client = require('web.web_client');
var rpc = require('web.rpc');
var _t = core._t;
var QWeb = core.qweb;

var SaleDashBoard = AbstractAction.extend({
    template: 'SaleDashBoard',
    events: {
        'change #sale_report': 'onclick_sale_report',
        'change #invoice_report': 'onclick_invoice_report',
    },

    init: function(parent, context) {
        this._super(parent, context);
        this.dashboards_templates = ['SaleChart'];
    },



    start: function() {
        var self = this;
        this.set("title", 'Dashboard');
        return this._super().then(function() {
            self.render_dashboards();
            self.render_graphs();
            self.$el.parent().addClass('oe_background_grey');
        });
    },



    render_dashboards: function() {
        var self = this;
            _.each(this.dashboards_templates, function(template) {
                self.$('.o_pj_dashboard').append(QWeb.render(template, {widget: self}));
            });
    },

    render_graphs: function(){
        var self = this;
         self.render_top_customer_graph();
         self.render_top_selling_product_graph();
         self.render_least_selling_product_graph();
         self.render_by_sales_team_graph();
         self.render_by_sales_person_graph();
    },

    onclick_sale_report:function(events){
        var option = $(events.target).val();
       var self = this
        var ctx = self.$("#canvas_1");
            rpc.query({
                model: "sale.order",
                method: "get_sale_order_state",
                args: [option],
            }).then(function (arrays) {
          var data = {
            labels: arrays[1],
            datasets: [
              {
                label: arrays[2],
                data: arrays[0],
                backgroundColor: [
                  "rgba(255, 99, 132,1)",
                  "rgba(54, 162, 235,1)",
                  "rgba(75, 192, 192,1)",
                  "rgba(153, 102, 255,1)",
                  "rgba(10,20,30,1)"
                ],
                borderColor: [
                 "rgba(255, 99, 132, 0.2)",
                  "rgba(54, 162, 235, 0.2)",
                  "rgba(75, 192, 192, 0.2)",
                  "rgba(153, 102, 255, 0.2)",
                  "rgba(10,20,30,0.3)"
                ],
                borderWidth: 1
              },

            ]
          };

  //options
          var options = {
            responsive: true,
            title: {
              display: true,
              position: "top",
              text: "SALE ORDER",
              fontSize: 18,
              fontColor: "#111"
            },
            legend: {
              display: true,
              position: "bottom",
              labels: {
                fontColor: "#333",
                fontSize: 16
              }
            },
            scales: {
              yAxes: [{
                ticks: {
                  min: 0
                }
              }]
            }
          };

          //create Chart class object
          if (window.mySaleCharts != undefined)
          window.mySaleCharts.destroy();
          window.mySaleCharts = new Chart(ctx, {
            type: "bar",
            data: data,
            options: options
          });

        });
        },

        onclick_invoice_report:function(events){
        var option = $(events.target).val();
       var self = this
        var ctx = self.$("#canvas_2");
            rpc.query({
                model: "sale.order",
                method: "get_invoice_state",
                args: [option],
            }).then(function (arrays) {
          var data = {
            labels: arrays[1],
            datasets: [
              {
                label: arrays[2],
                data: arrays[0],
                backgroundColor: [
                  "rgba(255, 99, 132,1)",
                  "rgba(54, 162, 235,1)",
                  "rgba(75, 192, 192,1)",
                  "rgba(153, 102, 255,1)",
                  "rgba(10,20,30,1)"
                ],
                borderColor: [
                 "rgba(255, 99, 132, 0.2)",
                  "rgba(54, 162, 235, 0.2)",
                  "rgba(75, 192, 192, 0.2)",
                  "rgba(153, 102, 255, 0.2)",
                  "rgba(10,20,30,0.3)"
                ],
                borderWidth: 1
              },

            ]
          };

  //options
          var options = {
            responsive: true,
            title: {
              display: true,
              position: "top",
              text: "INVOICE ORDER",
              fontSize: 18,
              fontColor: "#111"
            },
            legend: {
              display: true,
              position: "bottom",
              labels: {
                fontColor: "#333",
                fontSize: 16
              }
            },
            scales: {
              yAxes: [{
                ticks: {
                  min: 0
                }
              }]
            }
          };

          //create Chart class object
          if (window.myInvoiceCharts != undefined)
          window.myInvoiceCharts.destroy();
          window.myInvoiceCharts = new Chart(ctx, {
            type: "bar",
            data: data,
            options: options
          });

        });
        },
    
    render_top_customer_graph:function(){
       var self = this
        var ctx = self.$(".top_customer");
            rpc.query({
                model: "sale.order",
                method: "get_the_top_customer",
            }).then(function (arrays) {


          var data = {
            labels: arrays[1],
            datasets: [
              {
                label: "",
                data: arrays[0],
                backgroundColor: [
                  "rgb(148, 22, 227)",
                  "rgba(54, 162, 235)",
                  "rgba(75, 192, 192)",
                  "rgba(153, 102, 255)",
                  "rgba(10,20,30)"
                ],
                borderColor: [
                 "rgba(255, 99, 132,)",
                  "rgba(54, 162, 235,)",
                  "rgba(75, 192, 192,)",
                  "rgba(153, 102, 255,)",
                  "rgba(10,20,30,)"
                ],
                borderWidth: 1
              },

            ]
          };

  //options
          var options = {
            responsive: true,
            title: {
              display: true,
              position: "top",
              text: " Top Customer",
              fontSize: 18,
              fontColor: "#111"
            },
            legend: {
              display: true,
              position: "bottom",
              labels: {
                fontColor: "#333",
                fontSize: 16
              }
            },
            scales: {
              yAxes: [{
                ticks: {
                  min: 0
                }
              }]
            }
          };

          //create Chart class object
          var chart = new Chart(ctx, {
            type: "bar",
            data: data,
            options: options
          });

        });
        },

        render_top_selling_product_graph:function(){
       var self = this
        var ctx = self.$(".top_selling_product");
            rpc.query({
                model: "sale.order",
                method: "get_the_top_selling_products",
            }).then(function (arrays) {


          var data = {
            labels: arrays[1],
            datasets: [
              {
                label: "Quantity",
                data: arrays[0],
                backgroundColor: [
                  "rgba(255, 99, 132,1)",
                  "rgba(54, 162, 235,1)",
                  "rgba(75, 192, 192,1)",
                  "rgba(153, 102, 255,1)",
                  "rgba(10,20,30,1)"
                ],
                borderColor: [
                 "rgba(255, 99, 132, 0.2)",
                  "rgba(54, 162, 235, 0.2)",
                  "rgba(75, 192, 192, 0.2)",
                  "rgba(153, 102, 255, 0.2)",
                  "rgba(10,20,30,0.3)"
                ],
                borderWidth: 1
              },

            ]
          };

  //options
          var options = {
            responsive: true,
            title: {
              display: true,
              position: "top",
              text: " Top Selling Products",
              fontSize: 18,
              fontColor: "#111"
            },
            legend: {
              display: true,
              position: "bottom",
              labels: {
                fontColor: "#333",
                fontSize: 16
              }
            },
            scales: {
              yAxes: [{
                ticks: {
                  min: 0
                }
              }]
            }
          };

          //create Chart class object
          var chart = new Chart(ctx, {
            type: "horizontalBar",
            data: data,
            options: options
          });

        });
        },

        render_least_selling_product_graph:function(){
       var self = this
        var ctx = self.$(".least_selling_product");
            rpc.query({
                model: "sale.order",
                method: "get_the_least_selling_products",
            }).then(function (arrays) {


          var data = {
            labels: arrays[1],
            datasets: [
              {
                label: "Quantity",
                data: arrays[0],
                backgroundColor: [
                  "rgba(255, 99, 132,1)",
                  "rgba(54, 162, 235,1)",
                  "rgba(75, 192, 192,1)",
                  "rgba(153, 102, 255,1)",
                  "rgba(10,20,30,1)"
                ],
                borderColor: [
                 "rgba(255, 99, 132, 0.2)",
                  "rgba(54, 162, 235, 0.2)",
                  "rgba(75, 192, 192, 0.2)",
                  "rgba(153, 102, 255, 0.2)",
                  "rgba(10,20,30,0.3)"
                ],
                borderWidth: 1
              },

            ]
          };

  //options
          var options = {
            responsive: true,
            title: {
              display: true,
              position: "top",
              text: " Least Selling Products",
              fontSize: 18,
              fontColor: "#111"
            },
            legend: {
              display: true,
              position: "bottom",
              labels: {
                fontColor: "#333",
                fontSize: 16
              }
            },
            scales: {
              yAxes: [{
                ticks: {
                  min: 0
                }
              }]
            }
          };

          //create Chart class object
          var chart = new Chart(ctx, {
            type: "horizontalBar",
            data: data,
            options: options
          });

        });
        },

        render_by_sales_team_graph:function(){
       var self = this
        var ctx = self.$(".sales_by_sales_team");
            rpc.query({
                model: "sale.order",
                method: "get_sales_by_sales_team",
            }).then(function (arrays) {


          var data = {
            labels: arrays[1],
            datasets: [
              {
                label: "Amount",
                data: arrays[0],
                backgroundColor: [
                  "rgba(255, 99, 132,1)",
                  "rgba(54, 162, 235,1)",
                  "rgba(75, 192, 192,1)",
                  "rgba(153, 102, 255,1)",
                  "rgba(10,20,30,1)"
                ],
                borderColor: [
                 "rgba(255, 99, 132, 0.2)",
                  "rgba(54, 162, 235, 0.2)",
                  "rgba(75, 192, 192, 0.2)",
                  "rgba(153, 102, 255, 0.2)",
                  "rgba(10,20,30,0.3)"
                ],
                borderWidth: 1
              },

            ]
          };

  //options
          var options = {
            responsive: true,
            title: {
              display: true,
              position: "top",
              text: " Sales by Sales Team",
              fontSize: 18,
              fontColor: "#111"
            },
            legend: {
              display: true,
              position: "bottom",
              labels: {
                fontColor: "#333",
                fontSize: 16
              }
            },
            scales: {
              yAxes: [{
                ticks: {
                  min: 0
                }
              }]
            }
          };

          //create Chart class object
          var chart = new Chart(ctx, {
            type: "horizontalBar",
            data: data,
            options: options
          });

        });
        },

        render_by_sales_person_graph:function(){
       var self = this
        var ctx = self.$(".sales_by_sales_person");
            rpc.query({
                model: "sale.order",
                method: "get_sales_by_sales_person",
            }).then(function (arrays) {


          var data = {
            labels: arrays[1],
            datasets: [
              {
                label: "Amount",
                data: arrays[0],
                backgroundColor: [
                  "rgba(255, 99, 132,1)",
                  "rgba(54, 162, 235,1)",
                  "rgba(75, 192, 192,1)",
                  "rgba(153, 102, 255,1)",
                  "rgba(10,20,30,1)"
                ],
                borderColor: [
                 "rgba(255, 99, 132, 0.2)",
                  "rgba(54, 162, 235, 0.2)",
                  "rgba(75, 192, 192, 0.2)",
                  "rgba(153, 102, 255, 0.2)",
                  "rgba(10,20,30,0.3)"
                ],
                borderWidth: 1
              },

            ]
          };

  //options
          var options = {
            responsive: true,
            title: {
              display: true,
              position: "top",
              text: " Sales by Sales Person",
              fontSize: 18,
              fontColor: "#111"
            },
            legend: {
              display: true,
              position: "bottom",
              labels: {
                fontColor: "#333",
                fontSize: 16
              }
            },
            scales: {
              yAxes: [{
                ticks: {
                  min: 0
                }
              }]
            }
          };

          //create Chart class object
          var chart = new Chart(ctx, {
            type: "horizontalBar",
            data: data,
            options: options
          });

        });
        },

        });


core.action_registry.add('sale_dashboard', SaleDashBoard);

return SaleDashBoard;

});
