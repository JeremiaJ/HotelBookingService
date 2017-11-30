package com.camunda.bpm.ppls.hotelpayment;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.logging.Logger;
import org.camunda.bpm.engine.delegate.DelegateExecution;
import org.camunda.bpm.engine.delegate.JavaDelegate;
import org.json.JSONObject;

public class PaymentProcess implements JavaDelegate {
	
	public void execute(DelegateExecution execution) throws Exception {
		final Logger LOGGER = Logger.getLogger("PAYMENT-PROCESS");
		final String USER_AGENT = "Mozilla/5.0";
			
		LOGGER.info("Booking Hotel");
		String book_id = execution.getVariable("book_id").toString();

		String url = "http://localhost:5000/transaction/pay";
//		String url = "http://167.205.35.162:5000/transaction/pay";
		URL obj = new URL(url);
		HttpURLConnection con = (HttpURLConnection) obj.openConnection();

		//add request header
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

	    //print result
		LOGGER.info(response.toString());

//	    JSONObject jsonObject = new JSONObject(response.toString());
//	    String transaction_id = jsonObject.getString("transaction_id");
//	    int total_price = jsonObject.getInt("total_price");

//	    ==========================
//	    send to payment gateway
//	    ==========================

//	    String url2 = "http://167.205.35.199:8080/engine-rest/process-definition/key/Process_1/submit-form";
//		URL obj2 = new URL(url2);
//		HttpURLConnection con2 = (HttpURLConnection) obj2.openConnection();
//
//		//add request header
//		con2.setRequestMethod("POST");
//		con2.setRequestProperty("User-Agent", USER_AGENT);
//		con2.setRequestProperty("Accept-Language", "en-US,en;q=0.5");
//
//		String urlParameters2 = "transaction_id=" + transaction_id + "&total_price" + total_price;
//		// Send post request
//		con2.setDoOutput(true);
//		DataOutputStream wr2 = new DataOutputStream(con2.getOutputStream());
//		wr2.writeBytes(urlParameters2);
//		wr2.flush();
//		wr2.close();
//
//		int responseCode2 = con2.getResponseCode();
//		LOGGER.info("\nSending 'POST' request to URL : " + url2);
//		LOGGER.info("Post parameters : " + urlParameters2);
//		LOGGER.info("Response Code : " + responseCode2);
//
//		BufferedReader in2 = new BufferedReader(
//		        new InputStreamReader(con2.getInputStream()));
//		String inputLine2;
//		StringBuffer response2 = new StringBuffer();
//		
//
//		while ((inputLine2 = in2.readLine()) != null) {
//			response2.append(inputLine2);
//		}
//		in2.close();
//
//	    //print result
//		LOGGER.info(response2.toString());
		
//	    ==========================
//	    if transaction process failed to start
//	    ==========================
	    Integer responseCode2 = 200;
		execution.setVariable("ProcessStatus", responseCode2);
		LOGGER.info(responseCode2.toString());
	}
}