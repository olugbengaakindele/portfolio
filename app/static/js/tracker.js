let type_filed = document.getElementById('item');
let cate_filed = document.getElementById('cate');

type_filed.onchange = function(){
    type = type_filed.value ;
    route = 'http://127.0.0.1:5000/expense/'+ type.toLowerCase()
    
    fetch(route).then( function(response) {
        response.json().then(function(data){
            let opt_htm = '';
            for (let cates of data.type ){
                opt_htm += '<option value="' + cates.category + '">'+ cates.category + '</option>';
            }
                cate_filed.innerHTML = opt_htm;
        })
    });

}