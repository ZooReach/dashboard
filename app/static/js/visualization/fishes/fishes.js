 var json_data = {}
 d3.json("/api/fishes").then( function (json_data) {

    var chart = c3.generate({
      size: {
        height: 400,
        width: 400
    },
    bindto :".container-fluid",
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

document.getElementById("visual_description").innerHTML = "Chart depicts number of subcategories available"
});







