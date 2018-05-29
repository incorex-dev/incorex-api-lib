var CryptoJS = require("crypto-js")
    http = require('https'),
    querystring = require('querystring'),
    request = require('request'),
    config = {
        url: 'https://api.incorex.com/v1/'
    };
    

function sign(message){
    return CryptoJS.HmacSHA512(message, config.secret).toString(CryptoJS.enc.hex);
}

exports.init_incorex = function (cfg) {
    config.key = cfg.key;
    config.secret = cfg.secret;
    config.nonce = Math.floor(new Date().getTime());
};

exports.api_query = function(method_name, data, callback){
    data.nonce = config.nonce++;
    var post_data = querystring.stringify(data);

    var options = {
      url: config.url + method_name,
      method: 'POST',
      headers: {
        'Key': config.key,
        'Sign': sign(post_data)
      },
      form:data
    };
    
    request(options, function (error, response, body) {
        if (!error && response.statusCode == 200) {
            callback(body);
        }else{
            callback(error);
        }
    });
};

exports.api_query2 = function(method_name, data, callback){
    data.nonce = config.nonce++;
    var post_data = querystring.stringify(data);

    var post_options = {
        host: 'api.incorex.com',
        port: '443',
        path: '/v1/' + method_name,
        method: 'POST',
        headers: {
            'Key': config.key,
            'Sign': sign(post_data),
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': Buffer.byteLength(post_data)
        }
    };
    var post_req = http.request(post_options, function(res) {
      res.setEncoding('utf8');
      res.on('data', function (chunk) {
          callback(chunk);
      });
    });

    post_req.write(post_data);
    post_req.end();
};



exports.test = function(){
    return config.key;
};