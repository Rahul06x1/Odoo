odoo.define('latest_elearning_courses_snippet.dynamic', function (require) {
var core = require('web.core');
var publicWidget = require('web.public.widget');
var QWeb = core.qweb;
var rpc = require('web.rpc');

var CourseCarousel = publicWidget.Widget.extend({
        selector: '.elearning_courses',
        willStart: async function(){
            await rpc.query({
                route: '/latest_courses/',
            }).then((data) =>{
                this.data = data;
            })
        },
        start: function(){
            var chunks = _.chunk(this.data,4)
            chunks[0].is_active = true
            this.$el.find('#all_courses').html(
            QWeb.render('latest_elearning_courses_snippet.course_carousel',{
                chunks
            })
            )
            },
        })
        publicWidget.registry.latest_elearning_courses_snippet_DynamicSnippet = CourseCarousel;
        return CourseCarousel
})


