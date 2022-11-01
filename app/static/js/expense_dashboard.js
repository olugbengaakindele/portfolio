//this gets the user id as it has be used to name the start date picker

let current_user_id= document.getElementById('Start_Date').name;
let start_date= document.getElementById('Start_Date');
let end_date = document.getElementById('End_Date');
let income_card = document.querySelector("#Income");
let expense_card = document.querySelector("#Expense");
let savings_card = document.querySelector("#Savings");
let dollarUSLocale = Intl.NumberFormat('en-US',{style: "currency",currency: "USD",useGrouping: true, maximumSignificantDigits: 3})

let date_set = true

// Function to fill in the card summary
const card_func = function() {

    let income = 0;
    let expense = 0;
    let saving = 0;
    if (start_date.value > end_date.value){
        date_set = false
    }else if (start_date.value == null || end_date.value == null ){
        date_set = false   
    }else{
        
        route = 'http://127.0.0.1:5000/allexpense/'+ current_user_id
        console.log(route)
        fetch(route).then( function(response) {
            response.json().then(function(data){
                
                for (let cates of data.type ){
                    // console.log(cates.type)
                    // console.log(new Date(start_date.value).getDate() ,"-----", new Date(cates.expense_date).getDate())
                    if(cates.expense_date >= start_date.value && cates.expense_date <= end_date.value){
                        console.log(new Date(start_date.value).getDate() ,"-----", new Date(cates.expense_date).getDate())
                        if (cates.type == 'Expense'){
                            expense += cates.amount
                        }else if(cates.type == 'Income'){
                            income += cates.amount
                        }
                    }
                }
                income_card.textContent = "Income : "  + dollarUSLocale.format(income);
                expense_card.textContent = "Expense : "  + dollarUSLocale.format(expense);
                savings_card.textContent = "Savings : "  + dollarUSLocale.format(income - expense);
            })
        });
    }
 return true;
};

console.log(card_func() );
start_date.onchange = card_func;

end_date.onchange = card_func;