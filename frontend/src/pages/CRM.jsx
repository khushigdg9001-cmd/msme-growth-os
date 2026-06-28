import { useEffect, useState } from "react";

import Sidebar from "../components/Sidebar";
import CustomerKPIs from "../components/CustomerKPIs";
import CustomerSearch from "../components/CustomerSearch";
import CustomerTable from "../components/CustomerTable";
import CRMRecommendation from "../components/CRMRecommendation";
import FollowUpGenerator from "../components/FollowUpGenerator";

import { getCRM } from "../api/crm";

function CRM() {

  const [crm, setCRM] = useState(null);

  const [search, setSearch] = useState("");

  useEffect(() => {

    async function loadCRM() {

      try {

        const data = await getCRM();

        console.log("CRM API :", data);

        setCRM(data);

      }

      catch (error) {

        console.error(error);

      }

    }

    loadCRM();

  }, []);

  if (!crm) {

    return (

      <div className="min-h-screen bg-slate-950 flex items-center justify-center">

        <h1 className="text-cyan-400 text-3xl font-bold">

          Loading CRM Agent...

        </h1>

      </div>

    );

  }

  const filteredCustomers = crm.customerList.filter((customer) =>

    customer.name.toLowerCase().includes(search.toLowerCase()) ||

    customer.company.toLowerCase().includes(search.toLowerCase())

  );

  return (

    <div className="flex min-h-screen bg-slate-950">

      <Sidebar />

      <main className="flex-1 overflow-y-auto p-10">

        {/* Header */}

        <div className="flex items-center justify-between mb-10">

          <div>

            <h1 className="text-5xl font-black text-cyan-400">

              CRM Intelligence

            </h1>

            <p className="text-slate-400 mt-3">

              AI powered customer relationship management,

              customer analytics and intelligent follow-up automation.

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

              CRM Agent Active

            </p>

          </div>

        </div>

        <CustomerKPIs crm={crm} />

        <CustomerSearch

          search={search}

          setSearch={setSearch}

        />

        <CustomerTable

          customers={filteredCustomers}

        />        <CRMRecommendation
          recommendation={crm.recommendation}
        />

        <FollowUpGenerator
          crm={crm}
        />

      </main>

    </div>

  );

}

export default CRM;

