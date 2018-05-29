require 'net/https'
require "json"

module IncoreX
  class Error < StandardError
    attr_reader :object

    def initialize(object)
      @object = object
    end
  end

  class API
    class << self
      KEY = "YOUR_API_KEY"         # TODO replace with your api key from settings page
      SECRET = "YOUR_API_SECRET"   # TODO replace with your api secret from settings page

      def api_query(method, params = nil)
        raise ArgumentError unless method.is_a?(String) || method.is_a?(Symbol)

        params = {} if params.nil?
        params['nonce'] = nonce

        uri = URI.parse(['https://api.incorex.com/v1', method].join('/'))

        post_data = URI.encode_www_form(params)

        digest = OpenSSL::Digest.new('sha512')
        sign = OpenSSL::HMAC.hexdigest(digest, SECRET, post_data)

        headers = {
          'Sign' => sign,
          'Key'  => KEY
        }

        req = Net::HTTP::Post.new(uri.path, headers)
        req.body = post_data
        http = Net::HTTP.new(uri.host, uri.port)
        http.use_ssl = true if uri.scheme == 'https'
        response = http.request(req)

        unless response.code == '200'
          raise IncoreX::Error.new(__method__), ['http error:', response.code].join(' ')
        end

        result = response.body.to_s

        unless result.is_a?(String) && valid_json?(result)
          raise IncoreX::Error.new(__method__), "Invalid json"
        end

        JSON.load result
      end

      private

      def valid_json?(json)
        JSON.parse(json)
        true
      rescue
        false
      end

      def nonce
        Time.now.strftime("%s%6N")
      end
    end
  end
end



puts "%s" % IncoreX::API.api_query('user_info').inspect
puts "%s" % IncoreX::API.api_query('user_trades', pair: 'BTC_USD', limit: 100, offset: 0).inspect

# puts "%s" % IncoreX::API.api_query('trades', pair: 'BTC_USD').inspect
# puts "%s" % IncoreX::API.api_query('order_book', pair: 'BTC_USD', limit: 100).inspect
# puts "%s" % IncoreX::API.api_query('ticker').inspect
# puts "%s" % IncoreX::API.api_query('pair_settings').inspect
# puts "%s" % IncoreX::API.api_query('currency').inspect

# puts "%s" % IncoreX::API.api_query('user_info').inspect
# order_params = {
#      pair: 'BTC_USD',
#      quantity: 2,
#      price: 100,
#      type: 'sell'
#    }
# puts "%s" % IncoreX::API.api_query('order_create', order_params).inspect
# puts "%s" % IncoreX::API.api_query('order_cancel', order_id: 12345).inspect
# puts "%s" % IncoreX::API.api_query('user_open_orders').inspect
# puts "%s" % IncoreX::API.api_query('user_trades', pair: 'BTC_USD', limit: 100, offset: 0).inspect
# puts "%s" % IncoreX::API.api_query('user_cancelled_orders', limit: 100, offset: 0).inspect
# puts "%s" % IncoreX::API.api_query('order_trades', order_id: 12345).inspect
# puts "%s" % IncoreX::API.api_query('required_amount', pair: 'BTC_USD', quantity: 2).inspect
# puts "%s" % IncoreX::API.api_query('deposit_address').inspect
# puts "%s" % IncoreX::API.api_query('withdraw_get_txid', task_id: 123456).inspect
# puts "%s" % IncoreX::API.api_query('create_xvoucher', currency: 'USD', amount: 100.00).inspect
# puts "%s" % IncoreX::API.api_query('activate_xvoucher', code: '123456').inspect
# puts "%s" % IncoreX::API.api_query('wallet_history', date: 1525122000).inspect
