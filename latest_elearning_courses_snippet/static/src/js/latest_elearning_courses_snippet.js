odoo.define('latest_elearning_courses_snippet.dynamic', function (require) {
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

                    <div class="col-lg-3 mb-5">
                    <a href='/slides/${item.id}'>
                        <div class="d-flex align-items-center">
                        <div class='card'>
                         <div class="img-container mr-3 rounded">
                                <img class="event-image rounded" src="data:image/png;base64,${item.image_1920}"/>
                            </div>
                            <div>
                                <h5 class="mb-0">${item.name}</h5>
                            </div>
                            <div>
                                <h5 class="mb-0">${item.description}</h5>
                            </div>
                            <div>

                            </div>
                            </div>
                        </div>
                        </a>
                    </div>
                    `
                })
                elearning_coursesRow.innerHTML = html
            })
        }
    },
});

})

