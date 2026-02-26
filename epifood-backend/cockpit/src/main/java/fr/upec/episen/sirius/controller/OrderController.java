package fr.upec.episen.sirius.controller;

import org.springframework.web.bind.annotation.*;
import fr.upec.episen.sirius.model.Order;
import fr.upec.episen.sirius.service.OrderStore;


@RestController
@RequestMapping("/orders")
public class OrderController {

    private final OrderStore store;

    public OrderController(OrderStore store) {
        this.store = store;
    }

    @GetMapping
    public Object list() {
        return store.all();
    }

    @PostMapping("/{id}/prepare")
    public Order prepare(@PathVariable Long id) {
        return store.setStatus(id, "PREP");
    }

    @PostMapping("/{id}/ready")
    public Order ready(@PathVariable Long id) {
        return store.setStatus(id, "FINI");
    }

    @PostMapping("/{id}/send")
    public Order send(@PathVariable Long id) {
        return store.setStatus(id, "SENT");
    }
}