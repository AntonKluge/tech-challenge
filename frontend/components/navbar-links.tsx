'use client';

import { cn } from '@/lib/utils';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Button } from './ui/button';

const LINKS = [
  {
    href: '/',
    label: 'Home',
  },
  {
    href: '/about',
    label: 'About',
  },
  {
    href: '/contact-us',
    label: 'Contact Us',
  },
];

export default function NavbarLinks() {
  const pathname = usePathname();

  return (
    <div className="hidden md:flex gap-2 flex-row items-center">
      {LINKS.map(({ href, label }) => (
        <Button key={href} variant="link" size="sm">
          <Link
            href={href}
            className={cn(
              'text-muted-foreground transition-colors hover:text-foreground',
              pathname.startsWith(href) && 'text-foreground'
            )}
          >
            {label}
          </Link>
        </Button>
      ))}
    </div>
  );
}
