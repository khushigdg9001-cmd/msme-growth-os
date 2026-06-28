import { useEffect, useState } from "react";
import { getInventory } from "../api/inventory";

import Sidebar from "../components/Sidebar";
import InventoryKPIs from "../components/InventoryKPIs";
import SearchBar from "../components/SearchBar";
import InventoryTable from "../components/InventoryTable";
import RestockRecommendation from "../components/RestockRecommendation";
import PurchaseOrder from "../components/PurchaseOrder";

function Inventory() {
  const [inventory, setInventory] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    async function loadInventory() {
      try {
        const data = await getInventory();

        console.log("Inventory API Response:", data);

        setInventory(data);
      } catch (error) {
        console.error(error);
      }
    }

    loadInventory();
  }, []);

  const filteredInventory = inventory.filter((item) => {
  const query = search.toLowerCase();

  return (
    (item.product ?? "").toLowerCase().includes(query) ||
    (item.supplier ?? "").toLowerCase().includes(query) ||
    (item.status ?? "").toLowerCase().includes(query)
  );
});

  return (
    <div className="flex min-h-screen bg-slate-950">
      <Sidebar />

      <main className="flex-1 overflow-y-auto p-10">

        <div className="flex items-center justify-between mb-10">

          <div>
            <h1 className="text-5xl font-black text-cyan-400">
              Inventory Intelligence
            </h1>

            <p className="text-slate-400 mt-3">
              AI powered inventory monitoring,
              demand prediction and autonomous
              restocking.
            </p>
          </div>

          <div className="text-right">
            <div className="flex items-center justify-end gap-2">
              <div className="h-3 w-3 rounded-full bg-green-400 animate-pulse"></div>

              <span className="text-green-400 font-semibold">
                LIVE
              </span>
            </div>

            <p className="text-slate-500 text-sm mt-2">
              Last Sync • 2 sec ago
            </p>
          </div>

        </div>

        <InventoryKPIs
    products={inventory}
/>

<SearchBar
    search={search}
    setSearch={setSearch}
/>

{/* Inventory Intelligence */}

<div className="mt-10 bg-slate-900 rounded-3xl border border-cyan-500/20 overflow-hidden">

    <div className="px-8 py-7">

        <h2 className="text-3xl font-bold text-white">
            Inventory Intelligence
        </h2>

        <p className="text-slate-400 mt-2">
            Recent inventory movements, supplier activity and AI-powered stock monitoring.
        </p>

    </div>

    <InventoryTable
        products={filteredInventory}
    />

</div>

        <RestockRecommendation />

<div className="mt-8">

    <PurchaseOrder
        inventory={inventory}
    />

</div>
      </main>
    </div>
  );
}

export default Inventory;