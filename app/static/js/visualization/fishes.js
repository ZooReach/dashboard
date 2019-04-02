var json_data = {}

d3.json("/api/fishes").then( function (json_data) {

    var chart = c3.generate({
        size: {
        height: 400,
        width: 400
    },
    bindto :".fishes",
    data: {
        json: json_data['data'],
        type : 'bar',
        keys: {
            x: 'category_level1',
            value: ['count']
        },
        onclick: function (d, i) { 
            console.log(d);
            var base_url = window.location.origin;
            window.open(
            base_url+'/visual/fishes',
            '_blank' 
        );
        },
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

document.getElementById("fishes").innerHTML = "Chart depicts number of subcategories available for fishes";

}, function(error){
         
         document.getElementById("report-container").innerHTML = "No Report Found";
});