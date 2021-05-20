 $(document).ready(function() {
      new Dygraph(document.getElementById("div_g"),
           NoisyData, { errorBars : true });
      new Dygraph(document.getElementById("div_g2"),
           NoisyData,
           {
             errorBars : true,
             interactionModel: {}
           });
      var g3 = new Dygraph(document.getElementById("div_g3"),
           NoisyData, { errorBars : true, interactionModel : {
            'mousedown' : downV3,
            'mousemove' : moveV3,
            'mouseup' : upV3,
            'click' : clickV3,
            'dblclick' : dblClickV3,
            'mousewheel' : scrollV3
      }});
      document.getElementById("restore3").onclick = function() {
        restorePositioning(g3);
      };
      new Dygraph(document.getElementById("div_g4"),
           NoisyData, {
             errorBars : true,
             drawPoints : true,
             interactionModel : {
               'mousedown' : downV4,
               'mousemove' : moveV4,
               'mouseup' : upV4,
               'dblclick' : dblClickV4
             },
             underlayCallback : captureCanvas
          });
    }
);