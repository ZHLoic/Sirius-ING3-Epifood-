import StatusBadge from './StatusBadge';
import { sendOrderApi, prepareOrderApi } from '../hooks/useApi';

export default function OrderCard({ order }) {

  const handleForceSend = async () => {
    try {
      await sendOrderApi(order.order_id);
      alert(`Commande ${order.order_id} forcée !`);
    } catch (err) {
      alert('Erreur lors de l’envoi : ' + err.message);
    }
  };

  const handlePrepare = async () => {
    try {
      await prepareOrderApi(order.order_id);
      alert(`Commande ${order.order_id} en préparation !`);
    } catch (err) {
      alert('Erreur préparation : ' + err.message);
    }
  };

  return (
    <div className="order-card">
      <h3>{order.name}</h3>
      <p>{order.description}</p>
      <StatusBadge status={order.status} />

      {order.status === 'PREP' && (
        <button onClick={handlePrepare}>Préparer</button>
      )}
      {order.status === 'FINI' && (
        <button onClick={handleForceSend}>Forcer envoi</button>
      )}
    </div>
  );
}