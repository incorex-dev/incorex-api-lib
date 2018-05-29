var incorex = require("./incorex");
// YOUR_API_KEY - TODO replace with your api key from profile page
// YOUR_API_SECRET - TODO replace with your api secret from profile page
incorex.init_incorex({key:'YOUR_API_KEY', secret:'YOUR_API_SECRET'});

//request version
incorex.api_query("user_info", { }, function(result){
    console.log(result);

    incorex.api_query("user_trades", { "pair":"BTC_USD", "limit":1, "offset":0 }, function(result){
        console.log(result);
    });
});

//http nodejs version
incorex.api_query2("user_info", { }, function(result){
    console.log(result);

    incorex.api_query2("user_trades", { "pair":"BTC_USD", "limit":2, "offset":0 }, function(result){
        console.log(result);
    });
});
