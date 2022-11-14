let type_filed = document.getElementById('item');
let cate_filed = document.getElementById('cate');
let body = document.getElementById("body")

const cate_change = function(){
    type = type_filed.value ;
    route = 'http://127.0.0.1:5000/expense/'+ type.toLowerCase()
    
    fetch(route).then( function(response) {
        response.json().then(function(data){
            let opt_htm = '';
            if ( (data.type).length == 0 ){
                opt_htm += '<option value="' + "opt_1"+ '">'+ "Go to settings to create categories" + '</option>';
            } else {
                for (let cates of data.type ){
                opt_htm += '<option value="' + cates.category + '">'+ cates.category + '</option>';
            }

            }
           
                cate_filed.innerHTML = opt_htm;
        })
    });

};

body.onload = cate_change
type_filed.onchange = cate_change