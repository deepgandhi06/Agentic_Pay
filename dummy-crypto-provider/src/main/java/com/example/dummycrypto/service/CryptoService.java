package com.example.dummycrypto.service;

import okhttp3.OkHttpClient;
import org.springframework.stereotype.Service;
import org.web3j.abi.FunctionEncoder;
import org.web3j.abi.FunctionReturnDecoder;
import org.web3j.abi.TypeReference;
import org.web3j.abi.datatypes.Address;
import org.web3j.abi.datatypes.Bool;
import org.web3j.abi.datatypes.Function;
import org.web3j.abi.datatypes.Type;
import org.web3j.abi.datatypes.generated.Uint256;
import org.web3j.crypto.Credentials;
import org.web3j.protocol.Web3j;
import org.web3j.protocol.core.DefaultBlockParameterName;
import org.web3j.protocol.core.methods.request.Transaction;
import org.web3j.protocol.core.methods.response.EthCall;
import org.web3j.protocol.core.methods.response.EthSendTransaction;
import org.web3j.protocol.http.HttpService;
import org.web3j.tx.RawTransactionManager;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.List;
import java.util.concurrent.TimeUnit;

@Service
public class CryptoService {

    private final String rpcUrl = "https://eth-sepolia.g.alchemy.com/v2/ZZonf7h1galjK_R8KbBxp";
    private final String usdcContract = "0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238";
    private final long chainId = 11155111; // Sepolia

    private Web3j buildWeb3() {
        OkHttpClient okHttpClient = new OkHttpClient.Builder()
                .connectTimeout(60, TimeUnit.SECONDS)
                .readTimeout(60, TimeUnit.SECONDS)
                .writeTimeout(60, TimeUnit.SECONDS)
                .build();

        return Web3j.build(new HttpService(rpcUrl, okHttpClient, false));
    }

    public BigDecimal getUsdcBalance(String walletAddress) throws Exception {

        Web3j web3j = buildWeb3();

        Function function = new Function(
                "balanceOf",
                List.of(new Address(walletAddress)),
                List.of(new TypeReference<Uint256>() {})
        );

        String encodedFunction = FunctionEncoder.encode(function);

        EthCall response = web3j.ethCall(
                Transaction.createEthCallTransaction(
                        walletAddress,
                        usdcContract,
                        encodedFunction
                ),
                DefaultBlockParameterName.LATEST
        ).send();

        List<Type> decoded =
                FunctionReturnDecoder.decode(response.getValue(), function.getOutputParameters());

        if (decoded.isEmpty()) {
            throw new RuntimeException("Failed to fetch balance");
        }

        BigInteger rawBalance = (BigInteger) decoded.get(0).getValue();

        return new BigDecimal(rawBalance)
                .divide(BigDecimal.TEN.pow(6)); // USDC has 6 decimals
    }

    public TransferResponse transferUsdc(String privateKey,
                                         String receiver,
                                         BigDecimal amount) {

        try {

            Web3j web3j = buildWeb3();
            Credentials credentials = Credentials.create(privateKey);

            RawTransactionManager txManager =
                    new RawTransactionManager(web3j, credentials, chainId);

            BigInteger tokenAmount =
                    amount.multiply(BigDecimal.TEN.pow(6)).toBigInteger();

            Function function = new Function(
                    "transfer",
                    List.of(new Address(receiver), new Uint256(tokenAmount)),
                    List.of(new TypeReference<Bool>() {})
            );

            String encodedFunction = FunctionEncoder.encode(function);

            BigInteger gasPrice = web3j.ethGasPrice().send().getGasPrice();
            BigInteger gasLimit = BigInteger.valueOf(100000);

            EthSendTransaction tx = txManager.sendTransaction(
                    gasPrice,
                    gasLimit,
                    usdcContract,
                    encodedFunction,
                    BigInteger.ZERO
            );

            if (tx.hasError()) {
                return new TransferResponse(
                        "FAILED",
                        tx.getError().getMessage(),
                        null
                );
            }

            return new TransferResponse(
                    "SUCCESS",
                    "Transaction submitted successfully",
                    tx.getTransactionHash()
            );

        } catch (Exception e) {
            return new TransferResponse(
                    "ERROR",
                    e.getMessage(),
                    null
            );
        }
    }
}
