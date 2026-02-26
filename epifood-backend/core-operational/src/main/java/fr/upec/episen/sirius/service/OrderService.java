package fr.upec.episen.sirius.service;

import fr.upec.episen.sirius.model.Order;
import fr.upec.episen.sirius.kafka.OrderProducer;
import fr.upec.episen.sirius.repository.OrderRepository;

import java.time.LocalDateTime;
import java.util.concurrent.Semaphore;

import org.springframework.stereotype.Service;

@Service
public class OrderService {

    private final OrderRepository repo;
    private final OrderProducer producer;
    private final Semaphore semaphore = new Semaphore(3);

    public OrderService(OrderRepository repo, OrderProducer producer) {
        this.repo = repo;
        this.producer = producer;
    }

public void processOrder(Order order) {
    new Thread(() -> {
        try {
            // envoie en WAITING avant d'acquérir le semaphore
            order.setStatus("WAITING");
            repo.save(order);
            producer.sendPrep(order);

            semaphore.acquire();

            order.setStart_order_time(LocalDateTime.now());
            order.setEnd_time_prep(LocalDateTime.now().plusMinutes(order.getPrep_time()));
            order.setStatus("PREP");
            repo.save(order);
            producer.sendPrep(order);

            Thread.sleep(order.getPrep_time() * 60 * 1000L);

            order.setStatus("FINI");
            repo.save(order);
            producer.sendFinished(order);

            int delai = (int) (Math.random() * 10 + 5) * 1000;
            Thread.sleep(delai);
            order.setStatus("DONE");
            repo.save(order);
            producer.sendDone(order);

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            semaphore.release();
        }
    }).start();
}
}