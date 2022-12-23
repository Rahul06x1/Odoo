odoo.define('vehicle_rental.period_type', function (require) {
"use strict";
// Use an empty array to search for all the records
var domain = [];
// Use an empty array to read all the fields of the records
var fields = [];
var rpc = require('web.rpc');

    rpc.query({
    model: 'time.selection',
    method: 'search_read',
    args: [domain, fields],
}).then(function (data) {
$("#period_type").change(function(){
//    alert("sssssssssssrrrrrrrrrrrrr");
//    $('#time_amount').val($(this).val())
//    console.log(data,'dataaaaaaaaaaaaaaa');
    var current = data.filter((elem) => elem.id == $(this).val())
    $('#time_amount').val(current[0].time_amount)
//    console.log('ssssssssss', current)
    });
    });
    });
//    =================================================================================================================
//    rpc.query({
//    model: 'vehicle.rental.property',
//    method: 'search_read',
//    args: [domain, fields],
//}).then(function (data) {
//$("#vehicle").change(function(){
////    alert("sssssssssssrrrrrrrrrrrrr");
////    $('#time_amount').val($(this).val())
//    console.log(data,'dataaaaaaaaaaaaaaa');
//    var v_current = data.filter((elem) => elem.id == $(this).val())
////    $('#time_amount').val(current[0].time_amount)
//    c
//    console.log('ssssssssss', v_current)
//    });
//    });
//    });
//    $.each(data,function(index,value){
//    console.log(index);
//    console.log(value);
//    if ($(this).val() == index){
//    alert('asasaaaaaaaaaaaaaaaaaaaaaaaaaaaaaas');
//    console.log('sssssssssssssaaaaaaaaa');
//    }
//
////    console.log(index);
////    console.log(value);
//   console.log(index,  value);
//   console.log(index,  value.time_amount,'gg');
//   console.log(data.time_amount,'sssssssssssss');
//    });

//    $('#time_amount').val(89)
//    console.log(data);

//    });
//    });
//    });
//    alert("sssssssssssrrrrrrrrrrrrr");
//    $.each(data,function(index,value){
//   console.log(index,  value);
//   console.log(index,  value[0],'gg');
//});
//
//
//});
////        alert("sssssssssssrrrrrrrrrrrrr");
//      });
//      });
//
//
//
