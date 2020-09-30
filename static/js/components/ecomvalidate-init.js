$(function () {
    'use street';
    /*create product section start*/
    function previewImages() {
        var $preview = $(".image-preview");
        if (this.files) $.each(this.files, readAndPreview);

        function readAndPreview(i, file) {
            if (!/\.(jpe?g|png|gif)$/i.test(file.name)) {
                return alert(file.name + " is not an image");
            } // else...
            var reader = new FileReader();
            $(reader).on("load", function () {
                $preview.append(
                    "<span class='upload-wrapper'><span class='upload-wrapper-delete'>X</span><img src='" +
                    this.result +
                    "'></span>"
                );
            });
            reader.readAsDataURL(file);
            $(document).on("click", ".upload-wrapper-delete", function (e) {
                $(this)
                    .parents(".upload-wrapper")
                    .remove();
                $(this).remove();
            });
        }
    }
    $("#product_image").on("change", previewImages);

    $("#addProduct").validate({
        rules: {
            productid: {
                required: true
            },
            product_sku: {
                required: true,
                minlength: 2
            },
            product_name: {
                required: true,
                range: [2, 23]
            },
            product_price: {
                required: true
            },
            selling_price: {
                required: true,
                number: true
            },
            discount_starts: {
                date: true
            },
            quantity: {
                required: true
            },
            barcode: {
                required: true
            },
            category: {
                required: true
            },
            product_image: {
                required: true,
                accept: "image/*"
            }
        }
    });
    $(".color-select2").select2();
    $(".size-select2").select2();
    $('.datepicker').datepicker({
        startDate: "11/05/2011",
        endDate: "11/05/2100"
    });
    /*create product section end*/
    /*create customer section start*/
    function previewImages() {
        var $preview = $(".image-preview");
        if (this.files) $.each(this.files, readAndPreview);

        function readAndPreview(i, file) {
            if (!/\.(jpe?g|png|gif)$/i.test(file.name)) {
                return alert(file.name + " is not an image");
            } // else...
            var reader = new FileReader();
            $(reader).on("load", function () {
                $preview.append(
                    "<span class='upload-wrapper'><span class='upload-wrapper-delete'>X</span><img src='" +
                    this.result +
                    "'></span>"
                );
            });
            reader.readAsDataURL(file);
            $(document).on("click", ".upload-wrapper-delete", function (e) {
                $(this)
                    .parents(".upload-wrapper")
                    .remove();
                $(this).remove();
            });
        }
    }
    $("#customer_image").on("change", previewImages);

    $("#addCustomer").validate({
        rules: {
            customername: {
                required: true,
                range: [2, 20]
            },
            customerid: {
                required: true
            },
            email: {
                required: true,
                email: true
            },
            contact: {
                required: true
            },
            dob: {
                date: true
            },
            customer_image: {
                required: true,
                accept: "image/*"
            }
        }
    });
    /*create customer section end*/
})
