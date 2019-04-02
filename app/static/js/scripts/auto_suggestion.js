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

    function doesFileExist(urlToFile) {
  
        var xhr = new XMLHttpRequest();
        xhr.open('HEAD', urlToFile, false);
        xhr.send();
       
        if (xhr.status == "404") {
            return false;
        } else {
            return true;
        }
    }

    $("#submit_search_data").click(function(){
        var search_key  = $('#species-autocomplete').val();
        var json_data = {}
        var url = `/${search_key}`;
        var base_url = window.location.origin;
        $.ajax({
            url: url,
            dataType: "json",
            data : {search_key : $('#species-autocomplete').val()},
            success : function (data) {
                
                var source_file = 'static/'+data[0];
                if(doesFileExist(base_url+'/'+source_file)){
                    var reportContainer = document.getElementById("report-container");
                    reportContainer.innerHTML = "";
                    var visual_chart_element = document.createElement('div');
                    visual_chart_element.className = search_key;
                    reportContainer.appendChild(visual_chart_element);
                    var script = document.createElement('script');
                    script.src = source_file;
                    var description = document.createElement('div');
                    description.id = search_key;
                    description.innerHTML = "Chart depicts number of subcategories available";
                    reportContainer.appendChild(description);
                    
                    document.head.appendChild(script);
                }
                else{
                    
                    document.getElementById("report-container").innerHTML = "No Report Found";
                }
            },
            error: function(xhr, status, error){
                console.log("some error occurred");
            }
      });
    });
  });