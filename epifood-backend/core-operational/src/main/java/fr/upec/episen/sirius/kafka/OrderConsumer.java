package fr.upec.episen.sirius.kafka;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import fr.upec.episen.sirius.model.Order;
import fr.upec.episen.sirius.service.OrderService;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

@Service
public class OrderConsumer {

    private final OrderService service;
    private final ObjectMapper mapper;

    public OrderConsumer(OrderService service) {
        this.service = service;
        this.mapper = new ObjectMapper();
        this.mapper.registerModule(new JavaTimeModule());
    }

    @KafkaListener(topics = "commandes", groupId = "core-group")
    public void consume(String payload) {
        System.out.println("Message reçu : " + payload);
        try {
            Order order = mapper.readValue(payload, Order.class);
            service.processOrder(order);
        } catch (Exception e) {
            System.err.println("Erreur désérialisation : " + e.getMessage());
        }
    }
}