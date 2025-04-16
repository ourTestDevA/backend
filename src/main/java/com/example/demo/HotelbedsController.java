package com.example.demo;

import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.util.DefaultUriBuilderFactory;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.time.Instant;

@RestController
public class HotelbedsController {

    private final RestTemplate restTemplate;
    private final String apiKey = "HOTELBEDS_HOTEL_API_KEY";
    private final String secret = "HOTELBEDS_HOTEL_SECRET";

    public HotelbedsController() {
        this.restTemplate = new RestTemplate();
        this.restTemplate.setUriTemplateHandler(new DefaultUriBuilderFactory("https://api.test.hotelbeds.com/hotel-api/v1/hotels"));
    }

    @PostMapping("/hotelbeds-hotels-booking-hotel-availability")
    public ResponseEntity<String> checkHotelAvailability(@RequestBody String requestBody) {
        HttpHeaders headers = new HttpHeaders();
        headers.set("Accept", "application/json");
        headers.set("Accept-Encoding", "gzip");
        headers.set("Content-Type", "application/json");
        headers.set("Api-key", apiKey);
        headers.set("X-Signature", generateSignature());

        HttpEntity<String> entity = new HttpEntity<>(requestBody, headers);

        int attempts = 0;
        while (attempts < 3) {
            try {
                ResponseEntity<String> response = restTemplate.exchange("", HttpMethod.POST, entity, String.class);
                System.out.println("Request Body: " + requestBody);
                System.out.println("Response Body: " + response.getBody());
                return response;
            } catch (HttpClientErrorException e) {
                return ResponseEntity.status(e.getStatusCode()).body(e.getResponseBodyAsString());
            } catch (ResourceAccessException e) {
                attempts++;
                if (attempts >= 3) {
                    return ResponseEntity.status(504).body("Gateway Timeout");
                }
            }
        }
        return ResponseEntity.status(500).body("Internal Server Error");
    }

    private String generateSignature() {
        try {
            String toSign = apiKey + secret + Instant.now().getEpochSecond();
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(toSign.getBytes());
            StringBuilder hexString = new StringBuilder();
            for (byte b : hash) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) hexString.append('0');
                hexString.append(hex);
            }
            return hexString.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("Error generating signature", e);
        }
    }
}