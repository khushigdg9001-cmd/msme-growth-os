import { Brain, TrendingUp } from "lucide-react";

function FinanceRecommendation({ recommendation }) {

  return (

    <div className="mt-8 bg-slate-900 rounded-2xl border border-cyan-500/20 p-8">

      <div className="flex items-center gap-3 mb-6">

        <Brain
          className="text-cyan-400"
          size={34}
        />

        <h2 className="text-3xl font-bold text-white">

          AI Finance Recommendation

        </h2>

      </div>

      <div className="bg-slate-800 rounded-xl p-6">

        <h3 className="text-2xl font-bold text-cyan-400">

          {recommendation.title}

        </h3>

        <p className="text-slate-300 mt-4 leading-8">

          {recommendation.reason}

        </p>

        <div className="mt-6 flex items-center gap-3">

          <TrendingUp
            className="text-green-400"
            size={24}
          />

          <span className="text-green-400 font-semibold">

            Confidence :
            {" "}
            {recommendation.confidence}

          </span>

        </div>

      </div>

    </div>

  );

}

export default FinanceRecommendation;