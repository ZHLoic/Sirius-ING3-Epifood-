package fr.upec.episen.sirius.repository;

import fr.upec.episen.sirius.model.Order;
import org.springframework.data.jpa.repository.JpaRepository;

public interface OrderRepository extends JpaRepository<Order, Long> {
}