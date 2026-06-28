import { BrainCircuit } from "lucide-react";

function CRMRecommendation({ recommendation }) {

  return (

    <div className="mt-8 bg-slate-900 rounded-2xl border border-cyan-500/20 p-8">

      <div className="flex items-start gap-5">

        <div className="bg-cyan-500/20 p-4 rounded-2xl">

          <BrainCircuit

            className="text-cyan-400"

            size={34}

          />

        </div>

        <div className="flex-1">

          <h2 className="text-3xl font-bold text-white">

            AI CRM Recommendation

          </h2>

          <h3 className="text-cyan-400 text-xl mt-5 font-semibold">

            {recommendation.title}

          </h3>

          <p className="text-slate-300 mt-4 leading-7">

            {recommendation.reason}

          </p>

          <div className="mt-6 inline-flex px-4 py-2 rounded-full bg-green-500/20 text-green-400 font-semibold">

            Confidence : {recommendation.confidence}

          </div>

        </div>

      </div>

    </div>

  );

}

export default CRMRecommendation;