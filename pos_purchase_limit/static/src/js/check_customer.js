odoo.define('pos_purchase_limit.POSValidateOverride', function(require) {

    'use strict';

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');

    const POSValidateOverride = PaymentScreen =>
        class extends PaymentScreen {
            /**
             * @override
             */
            async validateOrder(isForceValidate) {

                if (!this.currentOrder.get_partner()){
                                const { confirmed } = await this.showPopup('ConfirmPopup', {
                                    title: ('Select a Customer'),
                                    body: ('Select a Customer.'),
                                });
                                if (confirmed) {
                                this.selectPartner();
                                }
                                return false;
                            }

                if(this.currentOrder.partner){
                if (this.currentOrder.partner.purchase_limit_amount <= this.currentOrder.paymentlines[0].amount && this.currentOrder.partner.activate_purchase_limit == 1) {
                                const { confirmed } = await this.showPopup('ConfirmPopup', {
                                    title: ('Your purchase limit amount is '),
                                    body: (this.currentOrder.partner.purchase_limit_amount),
                                });
                                return false;
                            }
                            }
                            await super.validateOrder(isForceValidate);
            }
        };

    Registries.Component.extend(PaymentScreen, POSValidateOverride);

    return PaymentScreen;
    });