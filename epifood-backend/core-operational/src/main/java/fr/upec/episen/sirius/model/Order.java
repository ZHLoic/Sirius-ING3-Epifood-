package fr.upec.episen.sirius.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "orders")
@JsonIgnoreProperties(ignoreUnknown = true)
public class Order {

    @Id
    private Long order_id;

    @Column(columnDefinition = "TEXT")
    private String category;

    @Column(columnDefinition = "TEXT")
    private String name;

    @Column(columnDefinition = "TEXT")
    private String description;

    private Double price;
    private LocalDateTime start_order_time;
    private Integer prep_time;
    private LocalDateTime end_time_prep;
    private String status;

    public Long getOrder_id() { return order_id; }
    public void setOrder_id(Long order_id) { this.order_id = order_id; }

    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public Double getPrice() { return price; }
    public void setPrice(Double price) { this.price = price; }

    public LocalDateTime getStart_order_time() { return start_order_time; }
    public void setStart_order_time(LocalDateTime start_order_time) { this.start_order_time = start_order_time; }

    public Integer getPrep_time() { return prep_time; }
    public void setPrep_time(Integer prep_time) { this.prep_time = prep_time; }

    public LocalDateTime getEnd_time_prep() { return end_time_prep; }
    public void setEnd_time_prep(LocalDateTime end_time_prep) { this.end_time_prep = end_time_prep; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
}