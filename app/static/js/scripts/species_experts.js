$(document).ready(function(){
    $("select").change(function(){
        var selected_species = $(this).find("option:selected").attr("value");
        $.ajax({
            url: '/find-experts',
            dataType: "json",
            data : {selected_key : selected_species},
            success : function (data) {
                if(data){
                    
                    var table_body = '<table class="table" id="expert-table">'+
                    '<thead class="thead-light">'+
                      '<tr>' +
                        '<th scope="col">Expert First Name</th>'+
                        '<th scope="col">Expert Last Name</th>'+
                        '<th scope="col">Email</th>'+
                        '<th scope="col">Affiliation</th>'+
                        '<th scope="col">Tags</th>'+
                        '<th scope="col">Work Done</th>'+
                     '</tr>'+
                    '</thead>'+
                    '<tbody>';
                    $.each(data, function(index, val) {
                        table_body +=  '<tr>';
                            table_body += '<td>';
                            table_body += val.first_name;
                            table_body += '</td>';
                            table_body += '<td>';
                            table_body += val.last_name;
                            table_body += '</td>';
                            table_body += '<td>';
                            table_body += val.email;
                            table_body += '</td>';
                            table_body += '<td>';
                            table_body += val.affiliation;
                            table_body += '</td>';
                            table_body += '<td>';
                            if(val.tags){
                                table_body += val.tags;
                            }    
                            else{
                                table_body += '';
                            }
                            table_body += '</td>';
                            table_body += '<td>';
                            if(val.author_work){
                                table_body += val.author_work;
                            }
                            else{
                                table_body += '';
                            }
                            
                            table_body += '</td>';
                        table_body +=  '</tr>';
                    })
                    table_body += '</tbody>'+'</table>';
                    
                    $('#expert-table-div').html(table_body);  
                }
                
            },
            error: function(xhr, status, error){
                alert("error");
            }
            

      })
    });
})
