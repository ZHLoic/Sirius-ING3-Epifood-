package fr.upec.episen.sirius.service;

import org.springframework.stereotype.Component;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;
import fr.upec.episen.sirius.model.Order;

@Component
public class OrderStore {

    private final Map<Long, Order> orders = new HashMap<>();

    public void update(Order order) {
        orders.put(order.getOrder_id(), order);
    }

    public Collection<Order> all() {
        return orders.values();
    }

    public Order setStatus(Long id, String status) {
        Order order = orders.get(id);
        if (order != null) {
            order.setStatus(status);
        }
        return order;
    }
}