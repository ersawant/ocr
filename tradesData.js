dy(function () { 

   #var keyValue = $('#tradesKey').html();  

   var url     = '/data'

   $("#table_4 th").css({

       "font-family": "Calibri",

        "font-size": "10pt",

        "background": "#D1E5FE  0 0 repeat-x",

        "border-color": "#FDFDFD #A4BED4 #A4BED4 #FDFDFD",

        "border-width": "1px",

        "border-style": "solid"

    })

            var dataTablesCols = [];

            var dataTablesColscust = [];

  

   for(var i in displayCols) {

        column = displayCols[i]   

        columnEntry = {"data": ""+column+""}

             dataTablesCols.push(columnEntry)

   }

  

   var oTable = $('#table_4').DataTable({

            sScrollX: "100%", 

    bProcessing: true,

    bServerSide: true,

    sPaginationType: "full_numbers",

    lengthMenu: [[25,50, 100, 150, 200], [25,50, 100, 150, 200]],

    bjQueryUI: true,

            bSortable: true,

    sAjaxSource: url,

    sServerMethod: 'POST',

    order:[[4,"asc"]],

            sType:"numeric",

    fnServerParams: function ( aoData ) {

      aoData.push( { "name": "key", "value": keyValue } );

    },

 

    columns: dataTablesCols,

            fnRowCallback: function( nRow, aData, iDisplayIndex, iDisplayIndexFull ) {

                                               

                        /* if(aData['Order Account Type Code']=="FIRM"){

                                               

                        $('td', nRow).css('background-color', '#f2dede' );

                        } */

                       

        $(nRow).css({"font-family": "Calibri", "font-size": "9pt", "border": "1px solid black"})     

    },

    initComplete: function() {

                       

        $('#table_4_filter input').unbind();

        $('#table_4_filter input').bind('keyup', function(e) {

            if(e.keyCode == 13) {

                oTable.search(this.value).draw();;

            }

        })}   

  });

 

});

 