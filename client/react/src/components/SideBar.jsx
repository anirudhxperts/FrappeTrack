import { useState } from "react"
import { useAuthStore } from "../store/authStore"
import fav from '../assets/favicon.webp'
import { FaUser } from "react-icons/fa";
import { MdArtTrack } from "react-icons/md";
import { Link } from "react-router-dom";



const SideBar = ({ children }) => {
    const { user } = useAuthStore()
    const [sideBar, setSideBar] = useState(false)

    return (
        <>
            <button data-drawer-target="default-sidebar" data-drawer-toggle="default-sidebar" aria-controls="default-sidebar" type="button" className="text-heading bg-transparent box-border border border-transparent hover:bg-neutral-secondary-medium focus:ring-4 focus:ring-neutral-tertiary font-medium leading-5 rounded-base ms-3 mt-3 text-sm p-2 focus:outline-none inline-flex sm:hidden">
                <span className="sr-only">Open sidebar</span>
                <svg className="w-6 h-6" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
                    <path stroke="currentColor" stroke-linecap="round" stroke-width="2" d="M5 7h14M5 12h14M5 17h10" />
                </svg>
            </button>

            <aside id="default-sidebar" className="fixed top-0 left-0 z-40 w-64 h-full transition-transform -translate-x-full sm:translate-x-0" aria-label="Sidebar">
                <div className="h-full px-3 py-4 overflow-y-auto bg-neutral-primary-soft border-e border-default">
                    <ul className="space-y-2 font-medium">
                        <li>
                            <div className="relative flex flex-col justify-center mt-16 items-center">
                               <div>
                                 <img
                                    src={user.employee.image || fav}
                                    alt="Profile"
                                    className="w-22 h-22 rounded-full border-4 border-white shadow-lg object-cover bg-gray-200"
                                />
                               </div>
                                <span className="text-center font-semibold p-2">{user.name}</span>
                            </div>
                        </li>
                        <li className="w-full h-1 bg-gray-500"></li>
                        <li>
                            <Link to="/user-profile" className="flex items-center px-2 py-1.5 text-body rounded-base hover:bg-neutral-tertiary hover:text-fg-brand group">
                                <FaUser className="shrink-0 w-5 h-5 transition duration-75 group-hover:text-fg-brand" aria-hidden="true" width="24" height="24" />
                                <span className="ms-3">Profile</span>
                            </Link>
                        </li>
                        <li>
                             <Link to="/time-tracker" className="flex items-center px-2 py-1.5 text-body rounded-base hover:bg-neutral-tertiary hover:text-fg-brand group">
                                <MdArtTrack className="shrink-0 w-7 h-7 transition duration-75 group-hover:text-fg-brand" aria-hidden="true"   />
                                <span className="ms-3">Tracker</span>
                            </Link>
                        </li>
                      
                    </ul>
                </div>
            </aside>

            {children}
        </>
    )
}

export default SideBar