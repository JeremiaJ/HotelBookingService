package com.camunda.bpm.ppls.hotelbooking;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

import java.util.logging.Logger;
import org.camunda.bpm.engine.delegate.DelegateExecution;
import org.camunda.bpm.engine.delegate.JavaDelegate;

public class BookHotel implements JavaDelegate {

  public void execute(DelegateExecution execution) throws Exception {
	  final Logger LOGGER = Logger.getLogger("HOTEL-BOOKING");
	  final String USER_AGENT = "Mozilla/5.0";

	  LOGGER.info("Booking Hotel");
	  String customer_id = execution.getVariable("customer_id").toString();
	  String type = execution.getVariable("type").toString();
	  Integer amount = Integer.valueOf(execution.getVariable("amount").toString());
	  String worker_id = execution.getVariable("worker_id").toString();

	  String url = "http://167.205.35.162:5000/book/create";
		URL obj = new URL(url);
		HttpURLConnection con = (HttpURLConnection) obj.openConnection();

		//add reuqest header
		con.setRequestMethod("POST");
		con.setRequestProperty("User-Agent", USER_AGENT);
		con.setRequestProperty("Accept-Language", "en-US,en;q=0.5");

		String urlParameters = "customer_id=" + customer_id + "&type=" + type + "&amount=" + amount.toString() + "&worker_id=" + worker_id;
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
  }

}