export default function StatusBadge({ status }) {
  const colors = {
    PREP: 'orange',
    FINI: 'green',
    TO_SEND: 'blue',
    DEFAULT: 'gray'
  };
  return (
    <span style={{
      backgroundColor: colors[status] || colors.DEFAULT,
      color: 'white',
      padding: '2px 6px',
      borderRadius: '4px',
      fontWeight: 'bold'
    }}>
      {status}
    </span>
  );
}