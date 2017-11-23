package com.camunda.bpm.ppls.confirmpayment;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.logging.Logger;
import org.camunda.bpm.engine.delegate.DelegateExecution;
import org.camunda.bpm.engine.delegate.JavaDelegate;

public class ConfirmPayment implements JavaDelegate{

	  public void execute(DelegateExecution execution) throws Exception {
		  final Logger LOGGER = Logger.getLogger("PRINT-RECEIPT");
		  final String USER_AGENT = "Mozilla/5.0";
	
		  LOGGER.info("Booking Hotel");
		  String book_id = execution.getVariable("book_id").toString();
	
		  String url = "http://localhost:5000/book/check/"+book_id;
			URL obj = new URL(url);
			HttpURLConnection con = (HttpURLConnection) obj.openConnection();
	
			//add reuqest header
			con.setRequestMethod("GET");
			con.setRequestProperty("User-Agent", USER_AGENT);
			con.setRequestProperty("Accept-Language", "en-US,en;q=0.5");
				
			int responseCode = con.getResponseCode();
			LOGGER.info("\nSending 'POST' request to URL : " + url);
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
