function Landing({ onLaunch }) {
  return (
    <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center text-center">

      <p className="text-cyan-400 uppercase tracking-[8px] mb-6">
        MSME Growth OS
      </p>

      <h1 className="text-7xl font-black text-white leading-tight">
        The World's First
        <br />
        <span className="text-cyan-400">
          Autonomous AI CEO
        </span>
      </h1>

      <p className="text-slate-400 text-xl mt-8 max-w-3xl">
        An intelligent multi-agent operating system that autonomously manages
        Inventory, Finance, CRM, Compliance and Business Growth.
      </p>

      <button
        onClick={onLaunch}
        className="mt-14 px-10 py-5 bg-cyan-500 hover:bg-cyan-400 rounded-2xl text-black font-bold text-xl transition duration-300"
      >
        Launch AI CEO →
      </button>

    </div>
  );
}

export default Landing;