package com.camunda.bpm.ppls.hotelpayment;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.logging.Logger;
import org.camunda.bpm.engine.delegate.DelegateExecution;
import org.camunda.bpm.engine.delegate.JavaDelegate;

public class PaymentProcess implements JavaDelegate {
	
  public void execute(DelegateExecution execution) throws Exception {
	  final Logger LOGGER = Logger.getLogger("PAYMENT-PROCESS");
	  final String USER_AGENT = "Mozilla/5.0";

	  LOGGER.info("Booking Hotel");
	  String book_id = execution.getVariable("book_id").toString();


//		String url = "http://localhost:5000/transaction/pay";
	    String url = "http://167.205.35.162:5000/transaction/pay";
		URL obj = new URL(url);
		HttpURLConnection con = (HttpURLConnection) obj.openConnection();

		//add reuqest header
		con.setRequestMethod("POST");
		con.setRequestProperty("User-Agent", USER_AGENT);
		con.setRequestProperty("Accept-Language", "en-US,en;q=0.5");

		String urlParameters = "book_id=" + book_id;
		// Send post request
		con.setDoOutput(true);
		DataOutputStream wr = new DataOutputStream(con.getOutputStream());
		wr.writeBytes(urlParameters);
		wr.flush();
		wr.close();
		
		int responseCode = con.getResponseCode();
		LOGGER.info("\nSending 'POST' request to URL : " + url);
		LOGGER.info("Post parameters : " + urlParameters);
		LOGGER.info("Response Code : " + responseCode);

		BufferedReader in = new BufferedReader(
		        new InputStreamReader(con.getInputStream()));
		String inputLine;
		StringBuffer response = new StringBuffer();

		while ((inputLine = in.readLine()) != null) {
			response.append(inputLine);
		}
		in.close();

		String[] parts = response.toString().split(",");
        String transaction_id = parts[0];
        LOGGER.info(transaction_id);
        execution.setVariable("transaction_id", transaction_id);
        String total_price = parts[1];
        execution.setVariable("total_price", total_price);
        LOGGER.info(total_price);
        
		//print result
		LOGGER.info(response.toString());
  }

}