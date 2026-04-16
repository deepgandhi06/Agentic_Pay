package com.example.dummycrypto.service;


public class TransferResponse {

    private String status;
    private String message;
    private String txHash;

    public TransferResponse(String status, String message, String txHash) {
        this.status = status;
        this.message = message;
        this.txHash = txHash;
    }

    public String getStatus() {
        return status;
    }

    public String getMessage() {
        return message;
    }

    public String getTxHash() {
        return txHash;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public void setTxHash(String txHash) {
        this.txHash = txHash;
    }
}

