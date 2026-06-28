import { Search } from "lucide-react";

function SearchBar({ search, setSearch }) {
  return (
    <div className="mt-8 bg-slate-900 rounded-2xl p-5 border border-cyan-500/20">
      <div className="flex items-center gap-3">
        <Search className="text-slate-400" />

        <input
          type="text"
          placeholder="Search products, suppliers or status..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="bg-transparent w-full outline-none text-white placeholder:text-slate-500"
        />
      </div>
    </div>
  );
}

export default SearchBar;