import React from 'react';

export default function OrderList({ orders }) {
  if (!orders || orders.length === 0) {
    return <p className="empty">Aucune commande</p>;
  }

  return (
    <div className="order-list">
      {orders.map(order => (
        <div key={order.order_id} className={`order-card order-card--${order.status?.toLowerCase()}`}>
          <div className="order-card-header">
            <span className="order-id">#{order.order_id}</span>
            <span className={`order-status status--${order.status?.toLowerCase()}`}>{order.status}</span>
          </div>
          <div className="order-name">{order.name}</div>
          <div className="order-meta">
            <span className="order-category">{order.category}</span>
            <span className="order-sep">·</span>
            <span className="order-description">{order.description}</span>
          </div>
          {order.prep_time && (
            <div className="order-time">⏱ {Math.min(order.prep_time, 3)} min</div>
          )}
        </div>
      ))}
    </div>
  );
}