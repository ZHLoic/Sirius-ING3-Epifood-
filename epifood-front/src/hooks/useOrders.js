import { useState, useEffect } from 'react';

export function useOrders() {
  const [orders, setOrders] = useState([]);

  // charge les commandes existantes au démarrage
  useEffect(() => {
    fetch('http://172.31.252.204:5000/orders')
      .then(res => res.json())
      .then(data => setOrders(data));
  }, []);

  // écoute les mises à jour en temps réel
  useEffect(() => {
    const ws = new WebSocket('ws://172.31.252.204:5000/ws/orders');
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setOrders(prev => {
        const index = prev.findIndex(o => o.order_id === data.order_id);
        if (index > -1) {
          prev[index] = data;
          return [...prev];
        }
        return [data, ...prev];
      });
    };
    return () => {
      if (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING) {
        ws.close();
      }
    };
  }, []);

  return orders;
}