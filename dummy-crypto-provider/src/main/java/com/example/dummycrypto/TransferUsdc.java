package com.example.dummycrypto;

import org.web3j.protocol.Web3j;
import org.web3j.protocol.http.HttpService;
import org.web3j.crypto.Credentials;
import org.web3j.tx.RawTransactionManager;
import org.web3j.protocol.core.methods.response.EthSendTransaction;
import org.web3j.protocol.core.methods.response.TransactionReceipt;
import org.web3j.tx.response.PollingTransactionReceiptProcessor;
import org.web3j.abi.FunctionEncoder;
import org.web3j.abi.TypeReference;
import org.web3j.abi.datatypes.Address;
import org.web3j.abi.datatypes.Bool;
import org.web3j.abi.datatypes.Function;
import org.web3j.abi.datatypes.generated.Uint256;

import java.math.BigInteger;
import java.util.Arrays;
import java.util.Collections;

public class TransferUsdc {

    public static void main(String[] args) throws Exception {
        // ⚠️ In production, load these from ENV or a secure config
        String rpcUrl = "https://eth-sepolia.g.alchemy.com/v2/ZZonf7h1galjK_R8KbBxp";
        String privateKey = "91a1f34df823dc7aacfe4be0bec6d057930435cbb0c4f252fc0ef43726e81927";
        String receiverAddress = "0x16361fc0c1294b7e24F9A7f68245Da160D72b01D";

        // USDC (Sepolia) – verify this matches your target network
        String usdcContract = "0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238";

        Web3j web3j = Web3j.build(new HttpService(rpcUrl));
        Credentials credentials = Credentials.create(privateKey);

        long chainId = 11155111L; // Sepolia chain ID
        RawTransactionManager txManager = new RawTransactionManager(web3j, credentials, chainId);

        // === Amount: 20 USDC ===
        // USDC uses 6 decimals, so 20 USDC = 20 * 10^6 = 20_000_000
        BigInteger amountInBaseUnits = BigInteger.valueOf(5_000_000L);

        // Build ERC-20 transfer(recipient, amount)
        Function transferFn = new Function(
                "transfer",
                Arrays.asList(
                        new Address(receiverAddress),
                        new Uint256(amountInBaseUnits)
                ),
                Collections.singletonList(new TypeReference<Bool>() {})
        );

        String data = FunctionEncoder.encode(transferFn);

        // Gas (legacy mode)
        BigInteger gasLimit = BigInteger.valueOf(100_000L); // safe upper bound for ERC20 transfers
        BigInteger gasPrice = web3j.ethGasPrice().send().getGasPrice(); // legacy gasPrice

        // Send transaction (value MUST be zero for ERC-20 transfer)
        EthSendTransaction send = txManager.sendTransaction(
                gasPrice,
                gasLimit,
                usdcContract,
                data,
                BigInteger.ZERO
        );

        // ---- Error handling ----
        if (send == null) {
            System.out.println("RPC returned null response to sendTransaction.");
            return;
        }

        if (send.hasError()) {
            var err = send.getError();
            System.out.println("RPC error: " + err.getMessage());
            System.out.println("Error code: " + err.getCode()); // primitive int; not nullable
            if (err.getData() != null) {
                System.out.println("Error data: " + err.getData());
            }
            return; // Do not poll for a receipt when send failed
        }
        // ------------------------

        String txHash = send.getTransactionHash();
        System.out.println("Transaction Hash: " + txHash);

        if (txHash == null || txHash.isEmpty()) {
            System.out.println("No transaction hash returned; not polling for receipt.");
            return;
        }

        // Wait for receipt
        PollingTransactionReceiptProcessor receiptProcessor =
                new PollingTransactionReceiptProcessor(web3j, 3000, 60); // poll every 3s up to 3 minutes

        TransactionReceipt receipt = receiptProcessor.waitForTransactionReceipt(txHash);

        System.out.println("Transaction Status: " + receipt.getStatus());
        System.out.println("Block: " + receipt.getBlockNumber());
        System.out.println("Gas Used: " + receipt.getGasUsed());
    }
}
