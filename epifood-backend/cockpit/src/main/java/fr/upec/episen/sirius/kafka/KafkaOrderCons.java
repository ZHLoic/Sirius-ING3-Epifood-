package fr.upec.episen.sirius.kafka;

import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;

import fr.upec.episen.sirius.model.Order;
import fr.upec.episen.sirius.service.OrderStore;
import fr.upec.episen.sirius.websocket.OrderWebSocketHandler;

@Service
public class KafkaOrderCons {

    private final OrderStore store;
    private final OrderWebSocketHandler wsHandler;

    public KafkaOrderCons(OrderStore store, OrderWebSocketHandler wsHandler) {
        this.store = store;
        this.wsHandler = wsHandler;
    }

    @KafkaListener(topics = {"commandes-status", "commandes-finies"}, groupId = "cockpit-group")
    public void consume(String payload) {
        System.out.println("Cockpit reçu : " + payload);
        try {
            ObjectMapper mapper = new ObjectMapper();
            mapper.registerModule(new JavaTimeModule());
            Order order = mapper.readValue(payload, Order.class);
            store.update(order);
            wsHandler.sendToAll(order);
        } catch (Exception e) {
            System.err.println("Erreur: " + e.getMessage());
        }
    }
}