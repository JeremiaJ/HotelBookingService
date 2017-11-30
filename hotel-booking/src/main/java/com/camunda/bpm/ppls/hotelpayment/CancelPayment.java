package com.camunda.bpm.ppls.hotelpayment;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.logging.Logger;

import org.camunda.bpm.engine.delegate.DelegateExecution;

public class CancelPayment {
	public void execute(DelegateExecution execution) throws Exception {
		final Logger LOGGER = Logger.getLogger("PAYMENT-PROCESS");
		final String USER_AGENT = "Mozilla/5.0";
			
		String url = "http://localhost:5000/transaction/fail/<transaction_id>";
//		String url = "http://167.205.35.162:5000/transaction/fail/<transaction_id>";
		URL obj = new URL(url);
		HttpURLConnection con = (HttpURLConnection) obj.openConnection();

		//add request header
		con.setRequestMethod("GET");
		con.setRequestProperty("User-Agent", USER_AGENT);
		con.setRequestProperty("Accept-Language", "en-US,en;q=0.5");

		// Send post request
		con.setDoOutput(true);
		DataOutputStream wr = new DataOutputStream(con.getOutputStream());
		wr.flush();
		wr.close();

		int responseCode3 = con.getResponseCode();
		LOGGER.info("\nSending 'GET' request to URL : " + url);
		LOGGER.info("Response Code : " + responseCode3);

		BufferedReader in = new BufferedReader(
		        new InputStreamReader(con.getInputStream()));
		String inputLine;
		StringBuffer response = new StringBuffer();
		

		while ((inputLine = in.readLine()) != null) {
			response.append(inputLine);
		}
		in.close();

	    //print result
		LOGGER.info(response.toString());
	}

}
