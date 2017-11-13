package com.camunda.bpm.ppls.hotelbooking;

import java.util.logging.Logger;
import org.camunda.bpm.engine.delegate.DelegateExecution;
import org.camunda.bpm.engine.delegate.JavaDelegate;

public class PaymentProcess implements JavaDelegate {

  private final static Logger LOGGER = Logger.getLogger("LOAN-REQUESTS");

  public void execute(DelegateExecution execution) throws Exception {
    LOGGER.info("Processing Payment request by '" + execution.getVariable("customerId") + "'...");
  }

}