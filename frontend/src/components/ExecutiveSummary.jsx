function ExecutiveSummary() {
  return (
    <div className="bg-slate-900 border border-cyan-500/20 rounded-2xl p-8">

      <div className="flex items-center justify-between mb-6">

        <h2 className="text-3xl font-bold text-cyan-400">
          Executive Summary
        </h2>

        <div className="px-4 py-2 rounded-full bg-cyan-500/20 text-cyan-300 text-sm font-semibold">
          AI CEO
        </div>

      </div>

      <p className="text-slate-300 leading-8 text-lg">

        Revenue has increased by
        <span className="text-green-400 font-bold"> 18%</span>
        while maintaining a healthy cash flow.

        <br /><br />

        Inventory analysis indicates that
        <span className="text-cyan-400 font-bold">
          {" "}Black Oversized Tee, White Hoodie and Premium Polo Shirt{" "}
        </span>
        require immediate replenishment based on forecasted demand.

        <br /><br />

        CRM has identified
        <span className="text-yellow-400 font-bold">
          {" "}27 premium customers{" "}
        </span>
        for a personalized retention campaign.

        <br /><br />

        Compliance review indicates that the
        <span className="text-purple-400 font-bold">
          {" "}Trade License{" "}
        </span>
        requires renewal within
        <span className="text-red-400 font-bold">
          {" "}18 days.
        </span>

        <br /><br />

        Overall business operations remain stable.
        AI CEO recommends immediate execution of all approved actions.

      </p>

    </div>
  );
}

export default ExecutiveSummary;