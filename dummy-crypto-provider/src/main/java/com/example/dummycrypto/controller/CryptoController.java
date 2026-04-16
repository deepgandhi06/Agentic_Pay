
package com.example.dummycrypto.controller;

import com.example.dummycrypto.service.CryptoService;
import com.example.dummycrypto.service.TransferResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class CryptoController {

    @Autowired
    private CryptoService cryptoService;

    @GetMapping("/wallet/balance")
    public ResponseEntity<?> getBalance(@RequestParam String address) {
        try {
            BigDecimal balance = cryptoService.getUsdcBalance(address);

            return ResponseEntity.ok(
                    Map.of(
                            "status", "SUCCESS",
                            "balance", balance
                    )
            );

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of(
                            "status", "ERROR",
                            "message", e.getMessage()
                    ));
        }
    }

    @PostMapping("/transfer")
    public ResponseEntity<?> transfer(@RequestBody Map<String, String> body) {

        String privateKey = body.get("privateKey");
        String receiver = body.get("receiver");
        BigDecimal amount = new BigDecimal(body.get("amount"));

        TransferResponse response =
                cryptoService.transferUsdc(privateKey, receiver, amount);

        if ("SUCCESS".equals(response.getStatus())) {
            return ResponseEntity.ok(response);
        }

        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(response);
    }
}
