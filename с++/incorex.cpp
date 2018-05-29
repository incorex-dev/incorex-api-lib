#include "incorex_api.hpp"
#include <iostream>

int main()
{
    // YOUR_API_KEY - TODO replace with your api key from profile page
    // YOUR_API_SECRET - TODO replace with your api secret from profile page
    incorex_api api("YOUR_API_KEY", "YOUR_API_SECRET");

    json_data response = api.call("user_info", "");
    std::clog << ">> user_info: " << response << "\n\n";
    
    response = api.call("user_trades", api.build({ "pair=BTC_USD", "limit=100", "offset=0" }));
    std::clog << ">> user_trades: " << response << "\n\n";
    
    return 0;
}

