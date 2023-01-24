odoo.define('pos_calculator.Custom', function(require) {
'use strict';
  const { Gui } = require('point_of_sale.Gui');
  const PosComponent = require('point_of_sale.PosComponent');
  const { identifyError } = require('point_of_sale.utils');
  const ProductScreen = require('point_of_sale.ProductScreen');
  const { useListener } = require("@web/core/utils/hooks");
  const Registries = require('point_of_sale.Registries');
  const PaymentScreen = require('point_of_sale.PaymentScreen');
  class CalculatorButton extends PosComponent {
      setup() {
          super.setup();
          useListener('click', this.onClick);
      }
     async onClick() {
               const { confirmed} = await
                    this.showPopup('CalculatorPopup', {
                       startingValue: 0,
                        title: this.env._t('Calculator'),
   });
                 }
  }
CalculatorButton.template = 'CalculatorButton';
  ProductScreen.addControlButton({
      component: CalculatorButton,
      condition: function() {
          return this.env.pos;
      },
  });
  Registries.Component.add(CalculatorButton);
  return CalculatorButton;
});


