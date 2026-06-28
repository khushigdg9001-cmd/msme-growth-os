import { Download, Sparkles } from "lucide-react";
import { useState } from "react";
import { generateFollowUpGeneratorPDF } from "../utils/pdfGenerator";

function FollowUpGenerator({ crm }) {

  const [loading, setLoading] = useState(false);

  const generateFollowUp = () => {

    setLoading(true);

    setTimeout(() => {

      generateFollowUpGeneratorPDF(crm);

      setLoading(false);

    }, 1200);

  };

  return (

    <div className="mt-8 bg-slate-900 rounded-2xl border border-cyan-500/20 overflow-hidden">

      <div className="p-8">

        <div className="flex items-center gap-4">

          <div className="bg-cyan-500/20 p-4 rounded-2xl">

            <Sparkles
              className="text-cyan-400"
              size={34}
            />

          </div>

          <div>

            <h2 className="text-3xl font-bold text-white">
              AI Follow-up Generator
            </h2>

            <p className="text-slate-400 mt-2">
              Generate personalized customer follow-up reports powered by AI.
            </p>

          </div>

        </div>

        <div className="mt-8 rounded-2xl bg-slate-800 border border-slate-700 p-6">

          <h3 className="text-cyan-400 font-bold text-xl">
            AI Preview
          </h3>

          <p className="text-slate-300 mt-5 leading-8">

            Hello{" "}
            <span className="text-white font-semibold">
              {crm.customerList[0].name}
            </span>,

            <br /><br />

            Thank you for being one of our valued customers.

            <br /><br />

            We noticed that it's been some time since your last purchase.

            We'd love to invite you to explore our newest premium collection
            with exclusive loyalty discounts specially curated for you.

            <br /><br />

            Looking forward to serving you again.

            <br /><br />

            Regards,

            <br />

            <span className="text-cyan-400">
              MSME Growth OS Team
            </span>

          </p>

        </div>

        <div className="flex justify-end mt-8">

          <button
            onClick={generateFollowUp}
            disabled={loading}
            className="bg-cyan-500 hover:bg-cyan-400 disabled:bg-cyan-700 transition-all duration-300 px-8 py-4 rounded-xl font-bold text-black flex items-center gap-3"
          >

            <Download size={22} />

            {
              loading
                ? "Generating AI Follow-up..."
                : "Generate Follow-up Report"
            }

          </button>

        </div>

      </div>

    </div>

  );

}

export default FollowUpGenerator;