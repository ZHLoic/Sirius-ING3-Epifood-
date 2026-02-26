export async function sendOrderApi(id) {
  // appelle Cockpit Backend
  const res = await fetch(`http://172.31.253.89:5000/orders/${id}/send`, {
    method: 'POST',
  });
  if (!res.ok) throw new Error('Erreur envoi commande');
  return await res.json(); // { id, status: "SENT" }
}

export async function prepareOrderApi(id) {
  const res = await fetch(`http://172.31.253.89:5000/orders/${id}/prepare`, {
    method: 'POST',
  });
  if (!res.ok) throw new Error('Erreur préparation');
  return await res.json();
}