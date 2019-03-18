$( function() { 
    $( "#species-autocomplete" ).autocomplete({ 
      source: function (request, response) {
          $.ajax({
                url: '/find-species',
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
                

          });
      }

    }); 

    $("#submit_search_data").click(function(){
        var search_key  = $('#species-autocomplete').val();
        var json_data = {}
        var url = `/api/${search_key}`;
        var res = d3.json(url);
            d3.json(url).then( function (json_data) {   
            var chart = c3.generate({
                size: {
                height: 400,
                width: 400
            },
            bindto :"#visual_report",
            data: {
                json: json_data['data'],
                    type : 'bar',
                    keys: {
                    x: 'category_level1',
                    value: ['count']
                }
            },
                axis: {
                        x: {
                            type: 'category'
                        }
                },
            bar: {
                width: {
                    ratio: 0.15
                }
            }
            });


            setTimeout(function () {
            chart.resize({height:400})
            }, 1000);

            }, function(error){
                document.getElementById("visual_report").innerHTML = "No Report Found";
            });

    });
  });