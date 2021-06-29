package com.ml.poc;

import com.microsoft.azure.functions.ExecutionContext;
import com.microsoft.azure.functions.annotation.Cardinality;
import com.microsoft.azure.functions.annotation.EventHubTrigger;
import com.microsoft.azure.functions.annotation.FunctionName;

public class Function {
    @FunctionName("fnappadpoc")
    public void fnappadpoc(
        @EventHubTrigger(
            name = "msg",
            eventHubName = "eh-syslogmsgs", // blank because the value is included in the connection string
            cardinality = Cardinality.ONE,
            connection = "EventHubConnectionString")
            String item,
            final ExecutionContext context) {

                context.getLogger().info("Event hub message received: " + item.toString());
            }
}