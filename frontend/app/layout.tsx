import Link from "next/link";
import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = {
  title: "VisitDock — Appointments",
  description: "Fictional clinic appointment workspace",
};
export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <a className="skip" href="#main">
          Skip to appointments
        </a>
        <header className="topbar">
          <Link className="brand" href="/">
            VisitDock<span> / RECEPTION</span>
          </Link>
          <nav aria-label="Main">
            <Link href="/" aria-current="page">
              Appointments
            </Link>
          </nav>
          <span className="demo">Fictional data only</span>
        </header>
        {children}
        <footer>
          VisitDock · Every appointment in its place.
          <span>Demonstration workspace</span>
        </footer>
      </body>
    </html>
  );
}
