odoo.define('quiz_idle_timer.idle_time', function (require) {
'use strict';
var publicWidget = require('web.public.widget');
var SurveyFormWidget = require('survey.form');
//var core = require('web.core');
var ajax = require('web.ajax');
var pages = -1

SurveyFormWidget.include({

        init: function(){
            this._super.apply(this, arguments);
        },
        _idle_timer: function(option, _submitForm){
            var self = this

           ajax.jsonRpc('/survey/idle/timer', 'call', {
                        'token':this.options.surveyToken
                    }).then(function (values) {

                    if (values['idle_timer']){
                        var idle = 0
                        var idleTimeSet = values['idle_timer']*60
                        const myTimeout = setInterval(() => {
                            $('*').bind('mousemove keydown scroll click', function() {
                            idle = 0;
                            idleTimeSet = values['idle_timer']*60
                            })
                            idle += 1
                            idleTimeSet -= 1
                            if (idle==values['idle_timer']*60 && pages < values['pages']){
                                 self._submitForm({
                                            'skipValidation': true,
                                            'isFinish': !self.options.sessionInProgress
                                            });
                                pages += 1
                                idle = 0
                                idleTimeSet = values['idle_timer']*60

                            }
                    if (pages == values['pages']){
                        clearInterval(myTimeout);
                        $('.idletimer').text(" ");
                    }else{
                        $('.idletimer').text(idleTimeSet + " Seconds");
                    }
                    }
                    , 1000);
                    }
                    });

        },
        _initBreadcrumb: function(option, _submitForm){

            this._super.apply(this, arguments);
            this._idle_timer(option, _submitForm);
            pages += 1
        },

    });
});
