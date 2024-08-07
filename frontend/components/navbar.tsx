import branding from '@/branding/branding.json';
import Image from 'next/image';
import Link from 'next/link';
import NavbarLinks from './navbar-links';

export default function Navbar() {
  return (
    <header className="sticky top-0 h-16 flex items-center gap-4 border-b bg-background px-4 z-20">
      <nav className="flex gap-6 w-full flex-row font-medium items-center text-sm justify-between">
        <div className="flex gap-4 flex-row items-center">
          <Link
            href="/"
            className="flex items-center gap-2 text-lg font-semibold md:text-base"
          >
            <Image src={branding.logo_url} alt="Logo" width={44} height={44} />
          </Link>
          <NavbarLinks />
        </div>
      </nav>
    </header>
  );
}
