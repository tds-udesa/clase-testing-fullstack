"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const TABS = [
  { href: "/", label: "Perro Aleatorio" },
  { href: "/saved", label: "Perros Guardados" },
];

export function NavTabs() {
  const pathname = usePathname();

  return (
    <div className="flex gap-2 border-b px-6">
      {TABS.map((tab) => {
        const isActive = pathname === tab.href;

        return (
          <Link
            key={tab.href}
            href={tab.href}
            className={cn(
              "border-b-2 px-4 py-3 text-sm font-normal border-transparent text-muted-foreground",
              isActive && "border-primary text-primary font-semibold",
            )}
          >
            {tab.label}
          </Link>
        );
      })}
    </div>
  );
}
