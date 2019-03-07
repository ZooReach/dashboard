$(document).ready(function(){
    $("#expert-table-div").hide();
    $("select").change(function(){
        var selected_species = $(this).find("option:selected").attr("value");
        $("#expert-table-div").show();   
        });
    })
