package mqtt_kafka_bridge;


import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;
import java.nio.charset.StandardCharsets;
import java.util.Properties;

public class MqttToKafkaBridge {

    // ===== MQTT =====
    private static final String MQTT_BROKER = "tcp://172.31.253.218:1883";
    private static final String MQTT_TOPIC = "commandes";
    private static final String MQTT_CLIENT_ID = "mqtt-kafka-bridge";

    // ===== KAFKA =====
    private static final String KAFKA_BOOTSTRAP = "localhost:9092";
    private static final String KAFKA_TOPIC = "commandes";

    public static void main(String[] args) throws Exception {

        // Kafka Producer
        Properties kafkaProps = new Properties();
        kafkaProps.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, KAFKA_BOOTSTRAP);
        kafkaProps.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG,
                "org.apache.kafka.common.serialization.StringSerializer");
        kafkaProps.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG,
                "org.apache.kafka.common.serialization.StringSerializer");

        KafkaProducer<String, String> producer = new KafkaProducer<>(kafkaProps);

        // MQTT Client
        MqttClient mqttClient = new MqttClient(
                MQTT_BROKER,
                MQTT_CLIENT_ID,
                new MemoryPersistence()        );

        MqttConnectOptions options = new MqttConnectOptions();
                options.setCleanSession(true);

        mqttClient.setCallback(new MqttCallback() {

            @Override
            public void connectionLost(Throwable cause) {
                System.err.println("MQTT connection lost: " + cause.getMessage());
            }

            @Override
            public void messageArrived(String topic, MqttMessage message) {
                String payload = new String(message.getPayload(), StandardCharsets.UTF_8);

                System.out.println("MQTT reçu: " + payload);

                ProducerRecord<String, String> record =
                        new ProducerRecord<>(KAFKA_TOPIC, payload);

                producer.send(record, (metadata, exception) -> {
                    if (exception != null) {
                        exception.printStackTrace();
                    } else {
                        System.out.println("Envoyé à Kafka (offset " + metadata.offset() + ")");
                    }
                });
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {}
        });

        mqttClient.connect(options);
        mqttClient.subscribe(MQTT_TOPIC);

        System.out.println("Bridge MQTT → Kafka actif");
    }
}
