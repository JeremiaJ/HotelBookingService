package com.camunda.bpm.ppls.hotelpayment;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.logging.Logger;
import org.camunda.bpm.engine.delegate.DelegateExecution;
import org.camunda.bpm.engine.delegate.JavaDelegate;


public class StartGateaway implements JavaDelegate  {
	
  public void execute(DelegateExecution execution) throws Exception {
	final Logger LOGGER = Logger.getLogger("PAYMENT-PROCESS");
	final String USER_AGENT = "Mozilla/5.0";

    String transaction_id = execution.getVariable("transaction_id").toString();
    String total_price = execution.getVariable("total_price").toString();

	
    String url2 = "http://167.205.35.199:8080/engine-rest/process-definition/key/Process_1/submit-form";
	URL obj2 = new URL(url2);
	HttpURLConnection con2 = (HttpURLConnection) obj2.openConnection();

	//add request header
	con2.setRequestMethod("POST");
	con2.setRequestProperty("User-Agent", USER_AGENT);
	con2.setRequestProperty("Accept-Language", "en-US,en;q=0.5");
	con2.setRequestProperty("Content-Type", "application/json");

	String urlParameters2 = 
			"{" +
					"	\"variables\":{" +
					"	\"idSeller\": {\"value\":6,\"type\":\"Integer\"}," +
					"	\"jumlahPembayaran\":{\"value\":"+total_price+",\"type\":\"Integer\"}," +
					"	\"callbackSukses\":{\"value\":\""+"http://167.205.35.162:5000/transaction/success/"+transaction_id+"\", \"type\":\"String\"}," +
					"	\"callbackGagal\":{\"value\":\""+"http://167.205.35.162:5000/transaction/fail/"+transaction_id+"\",\"type\":\"String\"}" +
					"	}" +
					"}";
	// Send post request
	con2.setDoOutput(true);
	DataOutputStream wr2 = new DataOutputStream(con2.getOutputStream());
	wr2.writeBytes(urlParameters2);
	wr2.flush();
	wr2.close();
	Integer responseCode2 = con2.getResponseCode();
	LOGGER.info("\nSending 'POST' request to URL : " + url2);
	LOGGER.info("Post parameters : " + urlParameters2);
	LOGGER.info("Response Code : " + responseCode2);
	BufferedReader in2 = new BufferedReader(
	        new InputStreamReader(con2.getInputStream()));
	String inputLine2;
	StringBuffer response2 = new StringBuffer();

	while ((inputLine2 = in2.readLine()) != null) {
		response2.append(inputLine2);
	}
	in2.close();

    //print result
	LOGGER.info(response2.toString());
	execution.setVariable("process_status", responseCode2);
  }	
}
