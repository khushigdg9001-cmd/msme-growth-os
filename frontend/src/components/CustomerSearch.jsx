import { Search } from "lucide-react";

function CustomerSearch({

  search,

  setSearch,

}) {

  return (

    <div className="mt-8 bg-slate-900 rounded-2xl border border-cyan-500/20 p-5">

      <div className="flex items-center gap-3">

        <Search className="text-slate-400" />

        <input

          type="text"

          value={search}

          onChange={(e) =>

            setSearch(e.target.value)

          }

          placeholder="Search customer or company..."

          className="bg-transparent w-full outline-none text-white"

        />

      </div>

    </div>

  );

}

export default CustomerSearch;