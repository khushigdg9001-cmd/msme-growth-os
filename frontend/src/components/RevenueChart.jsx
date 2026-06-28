function RevenueChart({ finance }) {

  if (!finance) {
    return null;
  }

  const months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
  ];

  const values = [
    150,
    170,
    195,
    210,
    225,
    finance.monthlyGrowth * 15,
  ];

  return (

    <div className="bg-slate-900 rounded-2xl border border-cyan-500/20 p-8 mb-8">

      <h2 className="text-3xl font-bold text-white">

        Revenue Analytics

      </h2>

      <p className="text-slate-400 mt-2">

        Monthly revenue trend predicted by Finance Agent

      </p>

      <div className="mt-8">

        <div className="flex items-end gap-5 h-72">

          {values.map((value, index) => (

            <div
              key={index}
              className="flex flex-col items-center flex-1"
            >

              <div
                className="w-full rounded-t-xl bg-cyan-400"
                style={{
                  height: `${value}px`,
                }}
              />

              <p className="mt-3 text-slate-400">

                {months[index]}

              </p>

            </div>

          ))}

        </div>

      </div>

    </div>

  );

}

export default RevenueChart;