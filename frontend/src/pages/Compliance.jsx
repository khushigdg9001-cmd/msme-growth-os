import { useEffect, useState } from "react";

import Sidebar from "../components/Sidebar";
import ComplianceKPIs from "../components/ComplianceKPIs";
import ComplianceTable from "../components/ComplianceTable";
import ComplianceRecommendation from "../components/ComplianceRecommendation";
import ComplianceReport from "../components/ComplianceReport";

import { getCompliance } from "../api/compliance";

function Compliance() {

  const [compliance, setCompliance] = useState(null);

  useEffect(() => {

    async function loadCompliance() {

      try {

        const data = await getCompliance();

        console.log("Compliance API:", data);

        setCompliance(data);

      }

      catch (error) {

        console.error(error);

      }

    }

    loadCompliance();

  }, []);

  if (!compliance) {

    return (

      <div className="min-h-screen bg-slate-950 flex items-center justify-center">

        <h1 className="text-cyan-400 text-3xl font-bold">

          Loading Compliance Agent...

        </h1>

      </div>

    );

  }

  return (

    <div className="flex min-h-screen bg-slate-950">

      <Sidebar />

      <main className="flex-1 overflow-y-auto p-10">

        <div className="flex items-center justify-between mb-10">

          <div>

            <h1 className="text-5xl font-black text-cyan-400">

              Compliance Intelligence

            </h1>

            <p className="text-slate-400 mt-3">

              AI powered compliance monitoring, legal risk analysis and document management.

            </p>

          </div>

          <div className="text-right">

            <div className="flex items-center justify-end gap-2">

              <div className="h-3 w-3 rounded-full bg-green-400 animate-pulse"></div>

              <span className="text-green-400 font-semibold">

                LIVE

              </span>

            </div>

            <p className="text-slate-500 mt-2">

              Compliance Agent Active

            </p>

          </div>

        </div>

        <ComplianceKPIs compliance={compliance} />

        <ComplianceTable documents={compliance.documents} />        <ComplianceRecommendation
          recommendation={compliance.recommendation}
        />

        <ComplianceReport
          compliance={compliance}
        />

      </main>

    </div>

  );

}

export default Compliance;