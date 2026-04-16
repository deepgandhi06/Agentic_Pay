
package com.example.dummycrypto.model;

import lombok.Data;
import java.time.Instant;
import java.util.UUID;

@Data
public class Transaction {
    private String txId = UUID.randomUUID().toString();
    private String fromAddress;
    private String toAddress;
    private String stablecoin;
    private double amount;
    private String status;
    private Instant createdAt = Instant.now();
}
