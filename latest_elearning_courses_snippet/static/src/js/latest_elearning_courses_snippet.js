odoo.define('latest_elearning_courses_snippet.dynamic', function (require) {
//   var PublicWidget = require('web.public.widget');
//   var rpc = require('web.rpc');
//   var Dynamic = PublicWidget.Widget.extend({
//       selector: '.dynamic_snippet_blog',
//       start: function () {
//           var self = this;
//           rpc.query({
//               route: '/total_product_sold',
//               params: {},
//           }).then(function (result) {
//               self.$('#total_sold').text(result);
//           });
//       },
//   });
//   PublicWidget.registry.dynamic_snippet_blog = Dynamic;
//   return Dynamic;
//});
//---------------------------------------------------------------------------------------------------
//
//odoo.define('latest_elearning_courses_snippet.dynamic', function (require) {
//    'use strict';
//    console.log('ssssssssssssss1')
//
//
////   var PublicWidget = require('web.public.widget');
////   var rpc = require('web.rpc');
//    var ajax = require('web.ajax');
//    var PublicWidget = require('web.public.widget');
//   var DynamicSnippet = PublicWidget.Widget.extend({
//       selector: '.dynamic_snippet_blog',
//       start: function () {
//           var self = this;
//           console.log('ssssssssssssss2',this)
//           ajax.jsonRpc('/new_product','call',{}).then(function(res){
//            if(res){
//            console.log('ssssssssssssss3')
//                self.$el.find('#js_new_product').html(res);
////                self.$target.empty().append(res);
//            }
//           })
//       }
//   });
//   PublicWidget.registry.dynamic_snippet_blog = DynamicSnippet;
//   return DynamicSnippet;
//});

//=====================================================================================
var publicWidget = require('web.public.widget');

publicWidget.registry.latest_elearning_courses_snippet_DynamicSnippet = publicWidget.Widget.extend({
    selector: '.elearning_courses',
    start() {
        let elearning_coursesRow = this.el.querySelector('#elearning-courses-row')

        if (elearning_coursesRow){
            this._rpc({
                route: '/latest_courses/',
                params:{}
            }).then(data=>{
                let html = ``
                data.forEach(item=>{

                    html += `
                    <a href='/latest_courses/${item.id}'>
                    <div class="col-lg-3 mb-5">
                        <div class="d-flex align-items-center">
                         <div class="img-container mr-3 rounded">
                                <img class="event-image rounded" src="data:image/png;base64,${item.image_1920}"/>
                            </div>
                            <div>
                                <h5 class="mb-0">${item.name}</h5>
                            </div>
                        </div>
                    </div>
                    </a>`
                })
                elearning_coursesRow.innerHTML = html
            })
        }
    },
});

})

