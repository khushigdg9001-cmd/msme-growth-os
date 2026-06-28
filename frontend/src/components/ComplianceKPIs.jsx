import {
  ShieldCheck,
  FileCheck,
  AlertTriangle,
  FileWarning,
  BadgeCheck,
  Scale,
} from "lucide-react";

function ComplianceKPIs({ compliance }) {

  const cards = [

    {
      title: "Compliance Rate",
      value: `${compliance.complianceRate}%`,
      icon: ShieldCheck,
      color: "text-green-400",
    },

    {
      title: "GST Status",
      value: compliance.gstStatus,
      icon: FileCheck,
      color: "text-cyan-400",
    },

    {
      title: "Licenses",
      value: compliance.licenses,
      icon: BadgeCheck,
      color: "text-purple-400",
    },

    {
      title: "Expiring Soon",
      value: compliance.expiringSoon,
      icon: AlertTriangle,
      color: "text-yellow-400",
    },

    {
      title: "Pending Docs",
      value: compliance.pendingDocuments,
      icon: FileWarning,
      color: "text-orange-400",
    },

    {
      title: "Risk Level",
      value: compliance.riskScore,
      icon: Scale,
      color:
        compliance.riskScore === "Low"
          ? "text-green-400"
          : "text-red-400",
    },

  ];

  return (

    <div className="grid grid-cols-3 gap-6 mb-8">

      {cards.map((card) => {

        const Icon = card.icon;

        return (

          <div
            key={card.title}
            className="bg-slate-900 border border-cyan-500/20 rounded-2xl p-6"
          >

            <div className="flex justify-between items-center">

              <div>

                <p className="text-slate-400">

                  {card.title}

                </p>

                <h2 className={`text-3xl font-bold mt-2 ${card.color}`}>

                  {card.value}

                </h2>

              </div>

              <Icon
                size={34}
                className={card.color}
              />

            </div>

          </div>

        );

      })}

    </div>

  );

}

export default ComplianceKPIs;