var sendWorkFlow;

$.getJSON( "diagrams/index_files/data.json", function(data) {

    var points = {};
    var instance;
    var endpoints = {};
    var colors = ['blue','red','green','yellow','pink','purple','orange','brown','gray','silver','aqua','navy','chocolate','magenta','black','turquoise'];
    var conns = [];
    var cols = assocColors();

    sendWorkFlow = function() {
        console.log('RUNNING ...');
        console.log(JSON.stringify(data, null, '\t'));
        $.ajax({
            url: 'http://localhost:5000/load',
            type: 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            async: false,
            success: function(msg) {
                console.log(msg);
            }
        });
    };

    function assocColors() {
        var exit = {};
        var fields = getUniqueFields();
        var cont = 0;
        for (var i in fields) {
            exit[fields[i]] = colors[cont++];
        }
        return exit;
    }

    function getUniqueFields() {
        var fields = {};
        for (var i in data['modules']) {
            var module = data['modules'][i];
            for (var j in module['fields']) {
                var field = module['fields'][j]
                var fieldName = field['name'];
                if (!fields[fieldName]) {
                    fields[fieldName] = true;
                }
            }
        }
        return Object.keys(fields);
    }

    function getWindowsNames() {
        var exit = [];
        for (var i in data['modules']) {
            var module = data['modules'][i];
            var moduleName = module['name'];
            exit.push(moduleName);
        }
        return exit;
    }

    function generateFlow() {
        console.log('RUNNING ...');
        for (var i in points) {
            for (var j in points[i]) {
                for (var k in points[i][j]) {
                    var element = points[i][j][k];
                    endpoints[element] = {
                        window: i,
                        variable: element.scope,
                        type: k
                    };
                }
            }
        }
        var allCons = instance.getAllConnections();
        for (var i in allCons) {
            var conn = allCons[i];
            var from = conn.endpoints[0];
            var to = conn.endpoints[1];
            conns.push({
                from: {
                    window: from.elementId,
                    variable: from.scope
                },
                to: {
                    window: to.elementId,
                    variable: to.scope
                }
            });
        }
        console.log(JSON.stringify(conns, null, '\t'));
    }

    (function () {

        jsPlumb.ready(function () {

            instance = jsPlumb.getInstance({
                DragOptions: { cursor: 'pointer', zIndex: 2000 },
                Container: "canvas"
            });

            var cons = {};

            for (var i in cols) {
                var color = cols[i];
                cons[i] = {
                    endpoint: [ "Dot", {radius: 14} ],
                    paintStyle: { fill: color },
                    isSource: true,
                    isTarget: true,
                    reattach: true,
                    scope: i,
                    connector: "Flowchart",
                    connectorStyle: {
                        strokeWidth: 5,
                        stroke: color
                    }
                }; 
            }
            
            setTimeout(function(){
                var leftPos = 1;

                for (var i in data['modules']) {
                    var module = data['modules'][i]
                    var moduleName = module['name'];
                    points[moduleName] = {};
                    for (var k in module['fields']) {
                        var field = module['fields'][k];
                        var fieldName = field['name'];
                        if (field['top']) {
                            console.log(moduleName + ' ' + fieldName);
                            points[moduleName][fieldName] = {
                                left: instance.addEndpoint(moduleName, { anchor: [0, field.top] }, cons[fieldName]),
                                right: instance.addEndpoint(moduleName, { anchor: [leftPos, field.top] }, cons[fieldName])
                            };
                        }
                    }
                }

                for (var i in data['connections']) {
                    var connection = data['connections'][i];
                    console.log(connection.from.window + ' ' + connection.from.variable + ' right > ' + connection.to.window + ' ' + connection.to.variable + ' left');
                    instance.connect({source:points[connection.from.window][connection.from.variable]['right'], target:points[connection.to.window][connection.to.variable]['left']});
                }

                instance.draggable(jsPlumb.getSelector(".drag-drop-demo .window"));

            }, 300);

            jsPlumb.fire("jsPlumbDemoLoaded", instance);
        });
    })();

});