
const Tracker = () => {
    return (
        <div className=" bg-gray-100 flex items-center justify-center min-h-screen">

            <div className="bg-white p-5 w-full max-w-md rounded-2xl shadow-lg">

                <div className="text-center mb-5">
                    <h2 className="text-2xl font-bold text-gray-800">Welcome</h2>
                    <h2 id="username" className="text-2xl font-bold text-gray-800"></h2>
                </div>

                <div className="flex gap-2 mb-5">
                    <select
                        className="flex-1 h-9 rounded-lg border border-gray-300 px-3 text-sm bg-white shadow-sm focus:outline-none focus:border-gray-600">
                        <option value="">Project</option>
                    </select>

                    <select
                        className="flex-1 h-9 rounded-lg border border-gray-300 px-3 text-sm bg-white shadow-sm focus:outline-none focus:border-gray-600">
                        <option value="">Task</option>
                    </select>

                    <select
                        className="flex-1 h-9 rounded-lg border border-gray-300 px-3 text-sm bg-white shadow-sm focus:outline-none focus:border-gray-600">
                        <option value="">Timesheet</option>
                        <option value="">Create timesheet</option>
                    </select>
                </div>

                <div className="flex justify-around gap-3 mb-5">
                    <button
                        id="start"
                        className="w-20 h-20 rounded-full bg-green-200 border border-gray-700 font-bold shadow-md
               hover:-translate-y-0.5 hover:shadow-lg transition">
                        Start
                    </button>

                    <button
                        id="pause"
                        className="w-20 h-20 rounded-full bg-yellow-200 border border-gray-700 font-bold shadow-md
               hover:-translate-y-0.5 hover:shadow-lg transition">
                        Pause
                    </button>

                    <button
                        id="stop"
                        className="w-20 h-20 rounded-full bg-red-200 border border-gray-700 font-bold shadow-md
               hover:-translate-y-0.5 hover:shadow-lg transition">
                        Stop
                    </button>
                </div>

                <div
                    id="timer"
                    className="mb-5 bg-white p-4 text-3xl text-center rounded-xl shadow-inner font-mono">
                    00:00:00
                </div>

                <h4 className="block text-gray-700 font-medium mb-2">Screenshot Preview</h4>
                <div id="screenshots" className="flex flex-wrap gap-2">
                </div>

            </div>

        </div>
    )
}

export default Tracker