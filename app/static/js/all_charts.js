const ctx = document.getElementById('myChart')
const ctx2 = document.getElementById('myChart2');

new Chart(ctx, {
    type: 'line',
    data: {
    // labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
    labels: [ "2022-08-09", "2021-03-24", "2022-11-22", "2022-11-01" ],
    datasets: [{
        label: '# of Votes',
        data: [12, 19, 3, 5],
        borderWidth: 1
    }]
    },
    options: {
    scales: {
        y: {
        beginAtZero: true
        }
    }
    }
    
});

new Chart(ctx2, {
    type: 'pie',
    data: {
    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
    datasets: [{
        label: '# of Votes',
        data: [12, 19, 3, 5, 2, 3],
        borderWidth: 1
    }]
    },
    options: {
    scales: {
        y: {
        beginAtZero: true
        }
    }
    }
});