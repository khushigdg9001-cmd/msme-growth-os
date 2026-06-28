import { useState } from "react";

function OneClickExecution() {

    const [executed, setExecuted] = useState(false);

    function executeBusiness() {

        setExecuted(true);

    }

    return (

        <div className="bg-slate-900 border border-cyan-500/20 rounded-2xl p-8">

            <div className="flex justify-between items-center">

                <div>

                    <h2 className="text-3xl font-bold text-cyan-400">

                        One Click Execution

                    </h2>

                    <p className="text-slate-400 mt-2">

                        Execute all AI CEO approved business actions instantly.

                    </p>

                </div>

                <div className="bg-cyan-500/20 px-4 py-2 rounded-full">

                    <span className="text-cyan-300 font-semibold">

                        AI CEO

                    </span>

                </div>

            </div>

            <div className="mt-8 space-y-4">

                <div className="flex justify-between bg-slate-800 rounded-xl p-4">

                    <span className="text-white">

                        📦 Generate Purchase Order

                    </span>

                    <span className={`${executed ? "text-green-400" : "text-slate-500"}`}>

                        {executed ? "Completed" : "Pending"}

                    </span>

                </div>

                <div className="flex justify-between bg-slate-800 rounded-xl p-4">

                    <span className="text-white">

                        💰 Approve Finance Budget

                    </span>

                    <span className={`${executed ? "text-green-400" : "text-slate-500"}`}>

                        {executed ? "Completed" : "Pending"}

                    </span>

                </div>

                <div className="flex justify-between bg-slate-800 rounded-xl p-4">

                    <span className="text-white">

                        👥 Launch CRM Campaign

                    </span>

                    <span className={`${executed ? "text-green-400" : "text-slate-500"}`}>

                        {executed ? "Completed" : "Pending"}

                    </span>

                </div>

                <div className="flex justify-between bg-slate-800 rounded-xl p-4">

                    <span className="text-white">

                        📑 Schedule Compliance Reminder

                    </span>

                    <span className={`${executed ? "text-green-400" : "text-slate-500"}`}>

                        {executed ? "Completed" : "Pending"}

                    </span>

                </div>

            </div>

            <button

                onClick={executeBusiness}

                className="mt-8 w-full bg-cyan-500 hover:bg-cyan-400 transition-all duration-300 text-black font-bold text-lg py-4 rounded-xl"

            >

                ⚡ Execute All Business Actions

            </button>

            {

                executed &&

                <div className="mt-6 bg-green-500/10 border border-green-500/30 rounded-xl p-5">

                    <h3 className="text-green-400 text-xl font-bold">

                        ✓ Execution Completed

                    </h3>

                    <p className="text-slate-300 mt-2">

                        Purchase Order generated successfully.

                        Finance budget approved.

                        CRM campaign scheduled.

                        Compliance reminder created.

                        AI CEO has completed all approved business actions.

                    </p>

                </div>

            }

        </div>

    );

}

export default OneClickExecution;