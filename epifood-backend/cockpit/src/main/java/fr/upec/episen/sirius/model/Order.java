package fr.upec.episen.sirius.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.databind.JsonNode;
@JsonIgnoreProperties(ignoreUnknown = true)
public class Order {

    private Long order_id;
    private String category;
    private String name;
    private String description;
    private Double price;
    private Integer prep_time;
    private JsonNode start_order_time;
    private JsonNode end_time_prep;
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

    public Integer getPrep_time() { return prep_time; }
    public void setPrep_time(Integer prep_time) { this.prep_time = prep_time; }

    public JsonNode getStart_order_time() { return start_order_time; }
    public void setStart_order_time(JsonNode start_order_time) { this.start_order_time = start_order_time; }

    public JsonNode getEnd_time_prep() { return end_time_prep; }
    public void setEnd_time_prep(JsonNode end_time_prep) { this.end_time_prep = end_time_prep; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
}