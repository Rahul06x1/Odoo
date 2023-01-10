/** @odoo-module **/
import SystrayMenu from 'web.SystrayMenu';
import Widget from 'web.Widget';
var ExampleWidget = Widget.extend({
   template: 'QRCodeSystray',
   events: {
       'click #generate_qr_code': '_onClick',
   },

    _onClick: function () {
            this.do_action({
                type: 'ir.actions.act_window',
                res_model: 'qr.code.generator.wizard',
                view_mode: 'form',
                view_type: 'form',
                views: [[false, 'form']],
                target: 'new',
            });
        },
    });
SystrayMenu.Items.push(ExampleWidget);
export default ExampleWidget;