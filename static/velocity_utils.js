var VU = {
    inlineSVG: function(svg_url, id, style, parent, exec_after){
        var xhr = new XMLHttpRequest;
        xhr.open('get', svg_url, true);
        xhr.onreadystatechange = function(){
            if (xhr.readyState != 4) return;
            var svg = xhr.responseXML.documentElement;
            svg = document.importNode(svg, true);
            if(id) svg.setAttribute('id', id);
            if(style) svg.setAttribute('style', style);
            parent.appendChild(svg);
            exec_after();
        };
        xhr.send();
    },
    moveTo: function(id, x, y, rotate, cb){
        if (!cb){ cb = function(){} }
        $('#' + id).velocity({ translateX: x + 'px', translateY: y + 'px',
                               rotateZ: rotate+'deg', translateZ: 0},
                             { duration:100 * Math.random(), delay: 0,
                               complete: cb});
    }
};