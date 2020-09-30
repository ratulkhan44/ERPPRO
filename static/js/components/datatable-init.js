$(function () {
    'use strict';
    $(document).ready(function () {
        if($('#myTable').length){
            setDataTable();
        }
        
    });
    //datatable
    function setDataTable() {
        $(document).ready(function () {
            var table = $('#myTable').DataTable({
                searching: true,
                bLengthChange: true,
                destroy: true,
                info: true,
                responsive: true,
                "pagingType": "simple_numbers",
                dom: '<"row table-filter"<"col-sm-12"<"float-left"l><"float-sm-right"f><"clearfix">>>t<"row table-pagination"<"col-sm-12"<"text-center"ip>>>',
                language: {
                  paginate: {
                    previous: "<i class='icon-arrow-left'></i>",
                    next: "<i class='icon-arrow-right'></i>"
                  },
                    searchPlaceholder: 'Search...',
                    sSearch: '',
                    lengthMenu: '_MENU_ items/page',
                },
                columns: [
                    { className: "first-column" },
                    null,
                    null,
                    null,
                    null,
                    null
                ],
                drawCallback: function() {
                  $($(".dataTables_wrapper .pagination li:first-of-type"))
                    .find("a")
                    .addClass("prev");
                  $($(".dataTables_wrapper .pagination li:last-of-type"))
                    .find("a")
                    .addClass("next");

                  $(".dataTables_wrapper .pagination").addClass("pagination-sm");
                }
            });

            $(document).ready(function() {
                $('#example-responsive').DataTable();
            } );

            var table = $('#ajaxTable').DataTable({
                "ajax": 'assets/js/ajax/arrays.txt'
            });
            var table = $('#example').DataTable({
                dom: 'Bfrtip',
                lengthChange: false,
                buttons: ['copy', 'excel', 'pdf', 'colvis']
            })
            var table = $('#listProduct').DataTable({
                dom: 'Bfrtip',
                lengthChange: false,
                buttons: ['copy', 'excel', 'pdf', 'colvis']
            });
            var table = $('#yearlypay').DataTable({
                dom: 'Bfrtip',
                lengthChange: false,
                buttons: ['copy', 'excel', 'pdf', 'colvis']
            });
            table.buttons().container()
                .appendTo('#example_wrapper .col-md-6:eq(0)');
        });
    }
});

//Editable Table
if($('#mainTable').length){
    $('#mainTable').editableTableWidget().numericInputExample().find('td:first').focus();
}
