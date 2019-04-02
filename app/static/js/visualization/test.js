var json_data = {}

d3.json("/api/test").then( function (json_data) {
  data = json_data['data']
  var chart = c3.generate({
    size: {
    height: 400,
    width: 400
  },
  bindto :".test",
  data: {
      json: json_data['data'],
      type : 'bar',
      keys: {
          x: 'name',
          value: ['count']
      },
      onclick: function (d, i) { 
        console.log(d);
        var base_url = window.location.origin;
        window.open(
        base_url+'/visual/test',
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
      },

  });
  document.getElementById("test").innerHTML = "Chart depicts number of categories available for species";
});
   