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

	  LOGGER.info("Completing Transaction");
	  String namaBarang = execution.getVariable("namaBarang").toString();
	  String namaPengirim = execution.getVariable("namaPengirim").toString();
	  String alamatPengirim = execution.getVariable("alamatPengirim").toString();
	  String teleponPengirim = execution.getVariable("teleponPengirim").toString();
	  String namaPenerima = execution.getVariable("namaPenerima").toString();
	  String alamatPenerima = execution.getVariable("alamatPenerima").toString();
	  String teleponPenerima = execution.getVariable("teleponPenerima").toString();
	  String jenisBarang = execution.getVariable("jenisBarang").toString();
	  Double beratBarang = Double.valueOf(execution.getVariable("beratBarang").toString()).doubleValue();
	  Double hargaBarang = Double.valueOf(execution.getVariable("hargaBarang").toString()).doubleValue();

	  String url = "http://localhost:4004/book/create";
		URL obj = new URL(url);
		HttpURLConnection con = (HttpURLConnection) obj.openConnection();

		//add reuqest header
		con.setRequestMethod("POST");
		con.setRequestProperty("User-Agent", USER_AGENT);
		con.setRequestProperty("Accept-Language", "en-US,en;q=0.5");

		String urlParameters = "nama=" + namaBarang + "&nama_pengirim=" + namaPengirim + "&alamat_pengirim=" + alamatPengirim + "&telepon_pengirim=" + teleponPengirim + "&nama_penerima=" + namaPenerima + "&alamat_penerima=" + alamatPenerima + "&telepon_penerima=" + teleponPenerima + "&jenis=" + jenisBarang  + "&keterangan=" + jenisBarang + "&berat=" + beratBarang.toString();
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