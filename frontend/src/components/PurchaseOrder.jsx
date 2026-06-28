import { useState } from "react";
import { Download } from "lucide-react";
import { generatePurchaseOrderPDF } from "../utils/pdfGenerator";

function PurchaseOrder() {

  const [loading, setLoading] = useState(false);

  const generatePO = () => {

    setLoading(true);

    setTimeout(() => {

      generatePurchaseOrderPDF();

      setLoading(false);

    }, 1200);

  };

  return (

    <div className="mt-8 bg-slate-900 rounded-2xl border border-cyan-500/20 p-8">

      <div className="flex justify-between items-start">

        <div>

          <h2 className="text-3xl font-bold text-white">
            AI Purchase Order
          </h2>

          <p className="text-slate-400 mt-3">
            Generate AI-powered purchase orders based on inventory demand forecasting.
          </p>

        </div>

        <div className="bg-cyan-500/20 px-4 py-2 rounded-full">

          <span className="text-cyan-400 font-semibold">
            Supplier Ready
          </span>

        </div>

      </div>

      <div className="mt-8 bg-slate-800 rounded-2xl p-6">

        <h3 className="text-cyan-400 text-xl font-bold">
          Purchase Summary
        </h3>

        <div className="grid grid-cols-2 gap-6 mt-6">

          <div>

            <p className="text-slate-400">
              Supplier
            </p>

            <p className="text-white font-semibold mt-2">
              Metro Textile
            </p>

          </div>

          <div>

            <p className="text-slate-400">
              Product
            </p>

            <p className="text-white font-semibold mt-2">
              Black Oversized T-Shirt
            </p>

          </div>

          <div>

            <p className="text-slate-400">
              Quantity
            </p>

            <p className="text-white font-semibold mt-2">
              120 Units
            </p>

          </div>

          <div>

            <p className="text-slate-400">
              Estimated Cost
            </p>

            <p className="text-green-400 font-bold mt-2">
              ₹48,000
            </p>

          </div>

        </div>

      </div>

      <div className="flex justify-end mt-8">

        <button
          onClick={generatePO}
          disabled={loading}
          className="bg-cyan-500 hover:bg-cyan-400 disabled:bg-cyan-700 transition-all duration-300 px-8 py-4 rounded-xl font-bold text-black flex items-center gap-3"
        >

          <Download size={22} />

          {loading
            ? "Generating Purchase Order..."
            : "Generate Purchase Order"}

        </button>

      </div>

    </div>

  );

}

export default PurchaseOrder;