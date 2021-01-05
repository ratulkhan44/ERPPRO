$(function () {
    'use strict';
    var availableTags = [
                "Alibe",
                "Era Lara",
                "Jhon Doe",
                "Michael Scofield",
                "Hugh O",
                "Eamonn O",
                "Frank Lynch",
                "Alan  Mccarthy",
                "Matt  Lynch",
                "Betha",
                "Kevin Murphy",
                "NJ"
            ];
    $("#cusid").autocomplete({
        source: availableTags,
        select: function (event, ui) {
            // Set selection
            $('#cusid').val('Alibe'); // display the selected text
            $('#customer_name').val('Alibe'); // display the selected text
            $('#customer_id').val('865944586'); // display the selected text
            $('#product_name').attr('tabindex', 2).focus();
            return false;
        }
    });
    var availableTags = [
                "Skart Bello",
                "Woman Bag",
                "Fine Art",
                "Jewellery",
                "Women Walet",
                "Skart Bello",
                "Women Jeans",
                "Jewellery",
                "Baseball",
                "Men Retro",
                "Shoulder Woman Bag",
                "silver dainty necklace"
            ];
    $("#product_name").autocomplete({
        source: availableTags,
        select: function (event, ui) {
            // Set selection
            $('#product_name').val('Skart Bello'); // display the selected text
            $('#proname').val('Skart Bello'); // display the selected text
            $('#qty').attr('tabindex', 3).focus();
            // display the selected text
            $('#mrp').val('150'); // display the selected text
            $('#stock').val('200'); // display the selected text
            return false;
        }
    });
//Product value add
    $("#qty").on("keypress", function (e) {
        if (e.which == 13 || e.keycode == '13') {
            var qty = parseFloat($('#qty').val());
            var mrp = parseFloat($('#mrp').val());
            var pname = $('#proname').val();
            var totall = mrp * qty;
            console.log(mrp);
            // Filter the same product
            var newtr = '<tr class="premove"><td><input type="text" class="valid" name="pname[]" readonly="" value="' + pname + '" ></td><td><input type="text" class="qty" value=' + qty + ' name="qty[]" readonly=""></td><td><input type="text" class="totall" value=' + totall + ' name="total[]" readonly=""></td><td class="text-nowrap"><a href="#" id="tremove" class="tremove" data-total='+ totall +' data-original-title="Close"><i class="icon-close text-danger"></i></a></td></tr>';
            /*Append Table Row*/
            $('#posinfo').append(newtr);
            calc_total();
            $('#qty').val("");
            $('#mrp').val("");
            $('#stock').val("");
            $('#proname').val("");
            $('#product_name').val("").attr('tabindex', 2).focus();
        }
    });

    function calc_total() {
        var sum = 0;
        $(".totall").each(function () {
            sum += parseFloat($(this).val());
        });
        $('.grandtotal').val(sum.toFixed(2));
        var pay = 0;
        $(".totall").each(function () {
            pay += parseFloat($(this).val());
        });

        $('.payable').val(pay.toFixed(2));
    }
    $("#gdiscount").on("keyup", function () {
        var gtotal = $('.grandtotal').val();
        var discount = $("#gdiscount").val() / 100;
        var totalTax = $("#totalTax").val();
        var granddiscount = gtotal * discount;
        if (discount > 0) {
            var pvalue = parseFloat(gtotal - granddiscount);
            if (totalTax > 0) {
                pvalue += +totalTax;
            }
            $(".payable").val(Math.abs(pvalue).toFixed(2));
            var paid = parseFloat($('.pay').val());
            var returnval = paid - pvalue;
            if (returnval <= 0) {
                $(".due").val(Math.abs(returnval).toFixed(2));
                $(".return").val('0');
            } else if (returnval > 0) {
                $('.return').val(returnval.toFixed(2));
                $(".due").val('0');
            }
        }
    });
        $("#tax").on("keyup",function () {
            var rows = this.closest('#SalesFormConfirm div');
            var tax = $(rows).find(".tax");
            var gtotal = $('.grandtotal').val();
            var discount = $("#gdiscount").val();
            var finalTotal = gtotal - discount;
            var taxValue = parseInt($(tax).val());
            var totalTaxval = Math.abs(finalTotal*(taxValue/100));
            //console.log(totalTaxval);
            var pvalued = parseFloat(finalTotal*(taxValue/100)) + +finalTotal;
            var paid = parseFloat($('.pay').val());
            if (paid > 0) {
                var returnval = paid - pvalued;
                if (returnval <= 0) {
                $(".due").val(Math.abs(returnval).toFixed(2));
                $(".return").val('0');    
                } else if (returnval > 0) {
                $('.return').val(returnval.toFixed(2));    
                $(".due").val('0');
                }
            }
            $(".payable").val(Math.abs(pvalued).toFixed(2));
            $(".totalTax").val(Math.abs(totalTaxval).toFixed(2));
        });    
        $(".pay").on("keyup",function () { 
            var payval = $('.pay').val();
            var payablevalue = $('.payable').val();
            var returnval = payval - payablevalue;
                if (returnval <= 0) {
                $(".due").val(Math.abs(returnval).toFixed(2));
                $(".return").val('0');    
                } else if (returnval > 0) {
                $(".return").val(returnval.toFixed(2));    
                $(".due").val('0');
                }   
        });
        $(document).on('click', ".superpro", function(e) {
            e.preventDefault(e);
            var name = $(this).attr('data-name');
            var mrp = $(this).attr('data-mrp');
            var stock = $(this).attr('data-stock');
            $('#proname').val(name);
            $('#mrp').val(mrp);
            $('.stock').val(stock);
            $('#qty').attr('tabindex', 3).focus();
        });
    //Remove Table value
    $(document).ready(function() {
        $(document).on('click', '.tremove', function(e) {
            e.preventDefault();
            var rows = this.closest('#SalesFormConfirm tr');
            var total = parseFloat($(".grandtotal").val());
            var pay = parseFloat($(".payable").val());
            var t = parseFloat($(this).attr('data-total'));
            var atotal = parseFloat(total - t);
            var ptotal = parseFloat(pay - t);
            $('.grandtotal').val(atotal);
            $('.payable').val(ptotal.toFixed(2));
            $(this).closest('tr').remove();
        });
    });
});
