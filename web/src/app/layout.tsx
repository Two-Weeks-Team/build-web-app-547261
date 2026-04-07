import type { Metadata } from "next";
import { DM_Sans, Space_Grotesk } from "next/font/google";
import "@/app/globals.css";

const bodyFont = DM_Sans({ subsets: ["latin"], weight: ["400", "500", "700"], variable: "--font-body" });
const displayFont = Space_Grotesk({ subsets: ["latin"], weight: ["500", "700"], variable: "--font-display" });

export const metadata: Metadata = {
  title: "IdeaSpark Studio",
  description: "Turn rough product ideas into execution-ready MVP briefs in one visible pass."
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className={`${bodyFont.variable} ${displayFont.variable} bg-background text-foreground`}>{children}</body>
    </html>
  );
}
