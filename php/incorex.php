<?php
function api_query($api_name, array $req = array())
{
    $mt = explode(' ', microtime());
    $NONCE = $mt[1] . substr($mt[0], 2, 6);

    // API settings
    $key = "YOUR_API_KEY";       //TODO replace with your api key from profile page
    $secret = "YOUR_API_SECRET"; //TODO replace with your api secret from profile page

    $url = "https://api.incorex.com/v1/$api_name";

    $req['nonce'] = $NONCE;

    // generate the POST data string
    $post_data = http_build_query($req, '', '&');

    $sign = hash_hmac('sha512', $post_data, $secret);

    // generate the extra headers
    $headers = array(
        'Sign: ' . $sign,
        'Key: ' . $key,
    );

    // our curl handle (initialize if required)
    static $ch = null;
    if (is_null($ch)) {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/4.0 (compatible; PHP client; ' . php_uname('s') . '; PHP/' . phpversion() . ')');
    }
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $post_data);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);

    // run the query
    $res = curl_exec($ch);
    if ($res === false) throw new Exception('Could not get reply: ' . curl_error($ch));
   
    $dec = json_decode($res, true);
    if ($dec === null)
        throw new Exception('Invalid data received, please make sure connection is working and requested API exists');

    return $dec;
}

//Example
print_r(api_query("user_info"));
echo "<br>";
print_r(api_query("user_trades", array("pair" => "BTC_USD", "limit" => 100, "offset" => 0))); 

// $result = api_query("trades", array("pair" => "BTC_USD"));
// $result = api_query("order_book", array("pair" => "BTC_USD", "limit" => 100));
// $result = api_query("ticker", array());
// $result = api_query("pair_settings", array());
// $result = api_query("currency", array());

// $result = api_query("user_info", array());
// $result = api_query("order_create", array("pair" => "BTC_USD", "quantity" => 2, "price" => 100, "type" => "sell"));
// $result = api_query("order_cancel", array("order_id" => 123456));
// $result = api_query("user_open_orders", array());
// $result = api_query("user_trades", array("pair" => "BTC_USD", "limit" => 100, "offset" => 0));
// $result = api_query("user_cancelled_orders", array());
// $result = api_query("order_trades", array("order_id" => 123456));
// $result = api_query("required_amount", array("pair" => "BTC_USD", "quantity" => 2));
// $result = api_query("deposit_address", array());
// $result = api_query("withdraw_get_txid", array("task_id" => 123456));
// $result = api_query("create_xvoucher", array("currency" => "USD", "amount" => 100.00));
// $result = api_query("activate_xvoucher", array("code" => "123456"));
// $result = api_query("wallet_history", array("date" => 1525122000));
?>