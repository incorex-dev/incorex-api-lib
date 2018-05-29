import java.util.HashMap;

public class Main {

    public static void main(String[] args) {
        // YOUR_API_KEY - TODO replace with your api key from profile page
        // YOUR_API_SECRET - TODO replace with your api secret from profile page
        IncoreX incorex = new IncoreX("YOUR_API_KEY","YOUR_API_SECRET");
        String result = incorex.Request("user_info", null);
        System.out.println(result);
        String result2 = incorex.Request("user_trades", new HashMap<String, String>() {{
            put("pair", "BTC_USD");
            put("limit", "2");
            put("offset", "0");
        }});
        System.out.println(result2);
    }
}
