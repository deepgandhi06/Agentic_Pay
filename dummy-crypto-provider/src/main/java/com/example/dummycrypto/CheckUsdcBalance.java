package com.example.dummycrypto;
import org.web3j.protocol.Web3j;
import org.web3j.protocol.http.HttpService;
import org.web3j.abi.FunctionEncoder;
import org.web3j.abi.datatypes.Function;
import org.web3j.abi.datatypes.Address;
import org.web3j.abi.datatypes.generated.Uint256;
import org.web3j.abi.TypeReference;
import org.web3j.protocol.core.methods.response.EthCall;
import org.web3j.protocol.core.DefaultBlockParameterName;
import org.web3j.protocol.core.methods.request.Transaction;
import org.web3j.abi.FunctionReturnDecoder;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class CheckUsdcBalance {
    //private key : 27e2a68422a1e1e9aa293f36b3ab5aa6a54eeefe50d8fbb98f0a7cf69563b778
    public static void main(String[] args) throws Exception {

        String rpcUrl = "https://eth-sepolia.g.alchemy.com/v2/ZZonf7h1galjK_R8KbBxp";
        String walletAddress = "0x16361fc0c1294b7e24F9A7f68245Da160D72b01D";

        String usdcContract ="0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238";

        Web3j web3j = Web3j.build(new HttpService(rpcUrl));

        Function function = new Function(
                "balanceOf",
                Arrays.asList(new Address(walletAddress)),
                Collections.singletonList(new TypeReference<Uint256>() {})
        );

        String encodedFunction = FunctionEncoder.encode(function);

        EthCall response = web3j.ethCall(
                Transaction.createEthCallTransaction(walletAddress, usdcContract, encodedFunction),
                DefaultBlockParameterName.LATEST
        ).send();

        List<org.web3j.abi.datatypes.Type> decoded =
                FunctionReturnDecoder.decode(response.getValue(), function.getOutputParameters());

        BigInteger rawBalance = (BigInteger) decoded.get(0).getValue();

        BigDecimal usdcBalance = new BigDecimal(rawBalance)
                .divide(BigDecimal.TEN.pow(6));

        System.out.println("USDC Balance: " + usdcBalance);
    }
}

