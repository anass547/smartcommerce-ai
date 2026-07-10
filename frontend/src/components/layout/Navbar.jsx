import { Link } from "react-router-dom";

export default function Navbar() {
  const links = [
    { to: "/", label: "Dashboard" },
    { to: "/forecast", label: "Prévision" },
    { to: "/segments", label: "Segments" },
    { to: "/assistant", label: "Assistant" },
  ];

  return (
    <nav className="bg-slate-900 text-white px-6 py-4 flex items-center gap-6">
      <span className="font-bold text-lg">SmartCommerce AI</span>
      {links.map((link) => (
        <Link key={link.to} to={link.to} className="text-sm text-slate-200 hover:text-white">
          {link.label}
        </Link>
      ))}
    </nav>
  );
}
