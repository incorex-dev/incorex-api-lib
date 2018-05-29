using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace IncoreXAPI
{
    class Program
    {
        static void Main(string[] args)
        {
            //Init
            var api = new IncoreXApi("YOUR_API_KEY", "YOUR_API_SECRET");

            //sync query
            var result = api.ApiQuery("user_info", new Dictionary<string, string>());
            Console.WriteLine("sync result");
            Console.WriteLine(result);
            var result2 = api.ApiQuery("user_trades", new Dictionary<string, string> { { "pair", "BTC_USD" }, { "limit", "100" }, { "offset", "0"} });
            Console.WriteLine("sync result2");
            Console.WriteLine(result2);


            //async query
            var task = api.ApiQueryAsync("user_info", new Dictionary<string, string> ());
            Console.WriteLine("async result3");
            Console.WriteLine(task.Result);

            Task.Factory.StartNew(async () =>
            {
                var result3 = await api.ApiQueryAsync("user_trades", new Dictionary<string, string> { { "pair", "BTC_USD" }, { "limit", "2" }, { "offset", "0" } });
                Console.WriteLine("async result4");
                Console.WriteLine(result3);
            });

            Console.ReadLine();
        }
    }
}
