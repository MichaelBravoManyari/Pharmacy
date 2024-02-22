$(function () {
    var salesDetails = []

    $('#id_product_name').autocomplete({
        source: "/inventory/search_products/",
        autoFocus: true,
        minLength: 3,
        select: function (event, ui) {
            var values = ui.item.value.split('-');
            var productId = $.trim(values[0]);
            var productName = values[1];

            $.ajax({
                type: 'GET',
                url: '/inventory/get_product_details/' + productId + '/',  // Reemplaza con tu URL real
                success: function (productDetails) {
                    var dialogContent = `
              <p><strong>Nombre:</strong> ${productName} </p>
              <p><strong>Laboratorio:</strong> ${productDetails.lab} </p>
              <p><strong>Generico:</strong> ${productDetails.generic} </p>
              <p><strong>Presentación:</strong> ${productDetails.presentation} </p>
              <p><strong>Precio de venta:</strong> S/.${productDetails.selling_price} </p>
              <p><strong>Precio de venta unitario:</strong> S/.${productDetails.unit_selling_price} </p>
              <p><strong>Stock min:</strong> ${productDetails.min_stock} </p>
              <p><strong>Indicaciones:</strong> ${productDetails.indications} </p>
              <p><strong>Stock Disponible:</strong> ${productDetails.quantity} unidades</p>
              <label for="quantity">Cantidad:</label>
              <input type="number" id="quantity" name="quantity" min="1" max="${productDetails.quantity}" />
              <br>
              <span id="quantity-error-message" style="color: red;"></span>
            `;

                    $('#product-dialog')
                        .html(dialogContent)
                        .dialog({
                            modal: true,
                            buttons: [
                                {
                                    text: "Agregar",
                                    click: function () {
                                        {
                                            var quantity = $('#quantity').val();
                                            if (quantity <= productDetails.quantity && quantity > 0) {
                                                var price = productDetails.unit_selling_price;
                                                var total = quantity * price;
                                                total = total.toFixed(2);

                                                salesDetails.push({
                                                    name: productName,
                                                    quantity: quantity,
                                                    price: price,
                                                    total: total
                                                });

                                                updateSalesTable();
                                                $('#id_product_name').val('');
                                                $(this).dialog('close');
                                            } else {
                                                $('#quantity-error-message').text('Ingrese una cantidad adecuada');
                                            }
                                        }
                                    }
                                }
                            ],
                            open: function () { // Bind keydown event after dialog opens
                                $('#quantity').on('keydown', function (event) {
                                    if (event.which === 13) {
                                        if ($('#quantity').is(':focus')) {
                                            event.stopPropagation();
                                            $('#product-dialog').parent().find('.ui-dialog-buttonpane button:contains("Agregar")').click();
                                            console.log("si")
                                        }
                                    }
                                });
                            }
                        });
                },
                error: function (error) {
                    console.error('Error al obtener detalles del producto:', error);
                }
            });
        }
    });

    function updateSalesTable() {
        var tableBody = $('#sales-table tbody');
        tableBody.html('');

        for (var i = 0; i < salesDetails.length; i++) {
            var detail = salesDetails[i];
            var row = `
          <tr>
            <td>${detail.name}</td>
            <td>${detail.quantity}</td>
            <td>S/.${detail.price}</td>
            <td>S/.${detail.total}</td>
          </tr>
        `;
            tableBody.append(row);
        }
    }
});
