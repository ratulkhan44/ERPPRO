var vm = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        voucher_no: '',
        voucher_date: '',
        reference: '',
        notes: '',
        journals: [{
            account: '',
            particular: '',
            people_for_from: '',
            people_by: '',
            debit: 0.00,
            credit: 0.00
        },
        {
            account: '',
            particular: '',
            people_for_from: '',
            people_by: '',
            debit: 0.00,
            credit: 0.00
        }]
    },
    methods: {

        addNewRow: function () {
            this.journals.push({
                account: '',
                particular: '',
                people_for_from: '',
                people_by: '',
                debit: 0.00,
                credit: 0.00
            });
        },
        deleteRow: function (index, journal) {
            var idx = this.journals.indexOf(journal);
            if (idx > 1) {
                this.journals.splice(idx, 1);
            }
        },


        submitForm: function () {
            for (i = 0; i < this.journals.length; i++) {
                axios({
                    method: "POST",
                    url: "http://127.0.0.1:8000/accountant/new-journal/", //django path name
                    headers: { 'X-CSRFTOKEN': '{{ csrf_token }}', 'Content-Type': 'application/json' },
                    data: { "voucher_no": this.voucher_no, "voucher_date": this.voucher_date, reference: this.reference, notes: this.notes, "account": this.journals[i].account, "particular": this.journals[i].particular, "people_for_from": this.journals[i].people_for_from, "people_by": this.journals[i].people_by, "debit": this.journals[i].debit, "credit": this.journals[i].credit },//data
                })
            }
            this.voucher_date = '',
                this.voucher_no = '',
                this.reference = '',
                this.notes = '',
                this.journals = [{
                    account: '',
                    particular: '',
                    people_for_from: '',
                    people_by: '',
                    debit: 0.00,
                    credit: 0.00
                }, {
                    account: '',
                    particular: '',
                    people_for_from: '',
                    people_by: '',
                    debit: 0.00,
                    credit: 0.00
                }]
        },



    },
    computed: {
        calculateDebitTotal: function () {
            return this.journals.reduce((total, journal) => {
                return total + Number(journal.debit);
            }, 0);
        },
        calculateCreditTotal: function (journal) {
            return this.journals.reduce((total, journal) => {
                return total + Number(journal.credit);
            }, 0);
        },
        calculateTotal: function () {
            return this.calculateDebitTotal - this.calculateCreditTotal
        }
    },


});


