//title:Demo code for CRM validation

$(function () {
    'use strict';

    $('.custom-select2').select2({
        dropdownParent: $("#formModal")
    });

    $('.datepicker').datepicker({
        startDate: "11/05/2011",
        endDate: "11/05/2100"
    });
    $('.monthpicker').datepicker({
        format: "mm-yyyy",
        viewMode: "months",
        minViewMode: "months"
    });
    $("#addProject").validate({
        rules: {
            protitle: {
                required: true,
                minlength: 8
            },
            client: {
                required: true
            },
            summery: {
                required: true
            },
            startdate: {
                required: true
            },
            enddate: {
                required: true
            }
        }
    });
    
});
