function PendingPayments({ finance }) {
  return (
    <div className="bg-slate-900 rounded-2xl border border-cyan-500/20 p-8">

      <h2 className="text-2xl font-bold text-cyan-400">
        Pending Payments
      </h2>

      <p className="text-slate-400 mt-2">
        Outstanding customer invoices
      </p>

      <h1 className="text-5xl font-black text-yellow-400 mt-8">
        ₹{finance.pendingPayments.toLocaleString()}
      </h1>

      <p className="text-slate-500 mt-4">
        Awaiting customer settlements
      </p>

    </div>
  );
}

export default PendingPayments;