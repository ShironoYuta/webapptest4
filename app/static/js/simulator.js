let CHART;
$(() => {
    const data = [[0, 0],[1, 1], [2, 4], [3, 9]];
    CHART = Highcharts.chart('container', {
        chart:{
            type: 'scatter'
        },
        title: {
            text: 'Quadratic function'
        },
        series: [{
            data: data
        }],
    })
});
const submit = () => {
    const a = $('#a').val();
    const b = $('#b').val();
    const c = $('#c').val();

    const inputData = {a: a, b: b, c: c}
    $.ajax({
        url: './calculate',
        type: 'POST',
        data: JSON.stringify(inputData),
        contentType: 'application/json',
        dataType: 'json',
    }).done((data) => {
        const zipped_data = data['x'].map((x, i) => {
            return [x, data['y'][i]]
        });
        console.log(zipped_data);
        CHART.update({
            series:[{
                data: zipped_data
            }],
        })
    }).fail((data) => {
        console.log(data);
    });
}