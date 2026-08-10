import { NavLink } from "react-router-dom";

export default function Navbar() {
  const links = [
    { to: "/", label: "Dashboard" },
    { to: "/forecast", label: "Prévision" },
    { to: "/segments", label: "Segments" },
    { to: "/assistant", label: "Assistant" },
  ];

  return (
    <nav className="bg-slate-900 text-white px-6 py-4 flex items-center gap-6 shadow-md">
      <span className="font-bold text-lg mr-4">SmartCommerce AI</span>
      <div className="flex gap-2">
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            end={link.to === "/"}
            className={({ isActive }) =>
              `text-sm font-medium px-3 py-1.5 rounded-md transition-all duration-200 ${
                isActive
                  ? "bg-slate-800 text-white shadow-inner border border-slate-700/50"
                  : "text-slate-300 hover:text-white hover:bg-slate-800/50"
              }`
            }
          >
            {link.label}
          </NavLink>
        ))}
      </div>
    </nav>
  );
}

