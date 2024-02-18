"use client";
import Link from "next/link";
import Image from "next/image";
import React, { useState } from "react";
import NavItem from "./navItem";
import "./navbar.css";
import { Sarabun } from "next/font/google";

const sarabun = Sarabun({ subsets: ["latin"], weight: "300" });

const MENU_LIST = [
  { text: "Home", href: "/" },
  { text: "Interview", href: "/interview" },
  { text: "Connect", href: "/connect" },
  { text: "About", href: "/about" },
  { text: "FAQs", href: "/faqs" },
];
const Navbar = () => {
  const [navActive, setNavActive] = useState(null);
  const [activeIdx, setActiveIdx] = useState(-1);

  return (
    <header className={sarabun.className}>
      <nav className={`nav`}>
        <Link href={"/"}>
          {/* <h1 className="logo">AI interview</h1> */}
          <Image src={"/logo.svg"} width="35" height="35" />
        </Link>
        <div
          onClick={() => setNavActive(!navActive)}
          className={`nav__menu-bar`}
        >
          <div></div>
          <div></div>
          <div></div>
        </div>
        <div className={`${navActive ? "active" : ""} nav__menu-list`}>
          {MENU_LIST.map((menu, idx) => (
            <div
              onClick={() => {
                setActiveIdx(idx);
                setNavActive(false);
              }}
              key={menu.text}
              style={{ display: "flex", gap: "60px" }}
            >
              <NavItem active={activeIdx === idx} {...menu} />
              <div> /</div>
            </div>
          ))}
        </div>
      </nav>
    </header>
  );
};

export default Navbar;
