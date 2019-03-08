$( function() { 
    $( "#species-autocomplete" ).autocomplete({ 
      source: function (request, response) {
          $.ajax({
                url: '/find-experts',
                dataType: "json",
                data : {search_key : $('#species-autocomplete').val()},
                success : function (data) {
                    if(data){
                        response($.map(data, function(item){
                            return {label : item.name, value:item.name};
                        }));
                    }
                    
                },
                error: function(xhr, status, error){
                    alert("error");
                }
                

          })
      }

    }); 
  });