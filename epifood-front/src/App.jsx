import { useOrders } from './hooks/useOrders';
import OrderList from './components/OrderList';
import './styles/app.css';

export default function App() {
  const orders = useOrders();
  const waitingOrders = orders.filter(o => o.status === 'WAITING');
  const prepOrders = orders.filter(o => o.status === 'PREP');
  const readyOrders = orders.filter(o => o.status === 'FINI');
  const historyOrders = orders.filter(o => o.status === 'DONE');

  return (
    <div className="app-container">
      <header>
        <div className="header-inner">
          <span className="header-logo">EPIFOOD</span>
          <h1>Dashboard Cuisine</h1>
          <span className="header-time">{new Date().toLocaleTimeString('fr-FR')}</span>
        </div>
      </header>

      <main className="columns">
        <div className="column column--waiting">
          <div className="column-header">
            <span className="column-icon"></span>
            <h2>En attente</h2>
            <span className="badge">{waitingOrders.length}</span>
          </div>
          <OrderList orders={waitingOrders} />
        </div>

        <div className="column column--prep">
          <div className="column-header">
            <span className="column-icon"></span>
            <h2>En préparation</h2>
            <span className="badge">{prepOrders.length}</span>
          </div>
          <OrderList orders={prepOrders} />
        </div>

        <div className="column column--ready">
          <div className="column-header">
            <span className="column-icon"></span>
            <h2>Prêtes</h2>
            <span className="badge">{readyOrders.length}</span>
          </div>
          <OrderList orders={readyOrders} />
        </div>

        <div className="column column--done">
          <div className="column-header">
            <span className="column-icon"></span>
            <h2>Historique</h2>
            <span className="badge">{historyOrders.length}</span>
          </div>
          <OrderList orders={historyOrders} />
        </div>
      </main>
    </div>
  );
}