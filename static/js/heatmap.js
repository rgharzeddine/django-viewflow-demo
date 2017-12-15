/*
 * While this is a working heat map with correct data, the charts are only
 * accessible with access to google, it's not possible to self-host them.
 * We may decide to leave it or use another library, however this example
 * serves a good enough purpose for demonstration.
 */

(function(){
    google.charts.load("current", {packages:["calendar"]});
    google.charts.setOnLoadCallback(drawChart);

    function convertTimeToDate(records){
        var converted = [];

        for(var i=0; i < records.length; i++){
            converted.push([new Date(records[i][0]), records[i][1]]);
        }

        return converted;
    }

    function buildRecord(parent, id, user, values){
        var element = '<div id="heat_' + id + '"></div>';
        parent.insertAdjacentHTML('beforeend', element);

        var dataTable = new google.visualization.DataTable();
        dataTable.addColumn({ type: 'date', id: 'day' });
        dataTable.addColumn({ type: 'number', id: 'hours' });
        dataTable.addRows(convertTimeToDate(values));
        var chart = new google.visualization.Calendar(
            document.getElementById('heat_' + id));
        var options = {
             title: user,
             colorAxis: { minValue: 0, maxValue: 16},
        };
        chart.draw(dataTable, options);
    }

    function drawChart() {
        var container = document.getElementById('birdseye');

        $.get(location.pathname)
            .done(function(data) {
                var index = 0;
                for(var entry in data){
                    if (data.hasOwnProperty(entry)) {
                        buildRecord(container, index++, entry, data[entry]);
                    }
                }
            });
    }
})();
