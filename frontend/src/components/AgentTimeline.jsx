import { useMemo } from "react";

function AgentTimeline() {

  const activities = useMemo(() => {

    const now = new Date();

    const messages = [
      {
        agent: "Inventory Agent",
        message: "Detected 3 products below reorder level.",
        color: "bg-cyan-400",
        offset: 120,
      },
      {
        agent: "Finance Agent",
        message: "Approved ₹52,000 procurement budget.",
        color: "bg-green-400",
        offset: 90,
      },
      {
        agent: "CRM Agent",
        message: "Forecasted demand for 147 units.",
        color: "bg-yellow-400",
        offset: 60,
      },
      {
        agent: "Compliance Agent",
        message: "Verified supplier GST compliance.",
        color: "bg-purple-400",
        offset: 30,
      },
      {
        agent: "AI CEO",
        message: "Generated executive business strategy.",
        color: "bg-red-400",
        offset: 0,
      },
    ];

    return messages.map((item) => {

      const time = new Date(now.getTime() - item.offset * 1000);

      return {
        ...item,
        time: time.toLocaleTimeString("en-IN", {
          timeZone: "Asia/Kolkata",
          hour: "2-digit",
          minute: "2-digit",
          hour12: true,
        }),
      };

    });

  }, []);

  return (

    <div className="bg-slate-900 rounded-2xl border border-cyan-500/20 p-6 mb-8">

      <div className="flex justify-between items-center mb-6">

        <h2 className="text-3xl font-bold text-cyan-300">
          Live Agent Activity
        </h2>

        <span className="text-green-400 text-sm font-semibold flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></div>
          LIVE
        </span>

      </div>

      <div className="space-y-6">

        {activities.map((item, index) => (

          <div key={index} className="flex gap-4">

            <div
              className={`w-3 h-3 rounded-full mt-2 animate-pulse ${item.color}`}
            ></div>

            <div>

              <p className="text-xs text-slate-500">

                {item.time} IST

              </p>

              <h3 className="text-white font-semibold mt-1">

                {item.agent}

              </h3>

              <p className="text-slate-400">

                {item.message}

              </p>

            </div>

          </div>

        ))}

      </div>

    </div>

  );

}

export default AgentTimeline;