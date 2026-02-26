package fr.upec.episen.sirius.kafka;


import fr.upec.episen.sirius.model.Order;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

@Service
public class OrderProducer {

    private final KafkaTemplate<String, Order> kafka;

    public OrderProducer(KafkaTemplate<String, Order> kafka) {
        this.kafka = kafka;
    }

    public void sendFinished(Order order) {
        kafka.send("commandes-finies", order);
    }
    public void sendPrep(Order order) {
    kafka.send("commandes-status", order);
    }
    public void sendDone(Order order) {
    kafka.send("commandes-status", order);
    }
}