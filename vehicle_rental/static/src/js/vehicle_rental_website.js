odoo.define('vehicle_rental.period_type', function (require) {
"use strict";
var domain = [];
var fields = [];

var rpc = require('web.rpc');

    rpc.query({
    model: 'time.selection',
    method: 'search_read',
    args: [domain, fields],
}).then(function (data) {
$("#vehicle").change(function(){

                    var current = data.filter((elem) => elem.relation_id[0] == $(this).val())

                    $('#period_type').find('option').remove().end();
                    $('#time_amount').val(' ');
                    $.each(current, function(index) {
                        console.log(current);
                        $('#period_type').append('<option value='+current[index].id+' data-time_amount='+current[index].time_amount+'>'+current[index].selection_time+ '</option>');
                        console.log($('#period_type'),'sssssssssssaaaaa')

                            });
//                            }
        });
    });

    rpc.query({
                model: 'time.selection',
                method: 'search_read',
                args: [domain, fields],
                }).then(function (data) {
                $("#period_type").change(function(){
                console.log($('#period_type').find(":selected"));
                $('#time_amount').val($('#period_type').find(":selected").data('time_amount'));
            });
    });
    });



