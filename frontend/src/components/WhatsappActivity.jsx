import { useEffect, useState } from "react";
import { getWhatsApp } from "../api/whatsapp";

function WhatsAppActivity() {

    const [messages, setMessages] = useState([]);

    useEffect(() => {

        async function load() {

            const data = await getWhatsApp();

            setMessages(data);

        }

        load();

    }, []);

    return (

        <div className="bg-slate-900 rounded-2xl border border-green-500/20 p-6 h-[820px] flex flex-col">

            <div className="flex justify-between items-center mb-6">

                <h2 className="text-3xl font-bold text-green-400">

                    WhatsApp Business Activity

                </h2>

                <span className="bg-green-500/20 px-3 py-1 rounded-full text-green-400 text-sm">

                    LIVE

                </span>

            </div>

            <div className="space-y-4 flex-1 overflow-y-auto pr-2">

    {messages.map((msg) => (

        <div
            key={msg.id}
            className="bg-[#202c33] rounded-xl p-4 border border-slate-700"
        >

                        <div className="flex justify-between">

                            <h3 className="font-bold text-white">

                                {msg.sender}

                            </h3>

                            <span className="text-xs text-slate-400">

                                {msg.time}

                            </span>

                        </div>

                        <p className="text-slate-300 mt-2">

                            {msg.message}

                        </p>

                    </div>

                ))}

            </div>

        </div>

    );

}

export default WhatsAppActivity;