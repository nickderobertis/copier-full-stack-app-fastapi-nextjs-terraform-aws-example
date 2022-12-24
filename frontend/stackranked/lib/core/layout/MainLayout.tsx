import { PropsWithChildren } from "react";
import Navbar from "../../nav-bar/NavBar";

export default function MainLayout({ children }: PropsWithChildren) {
  return (
    <>
      <Navbar />
      <main>{children}</main>
    </>
  );
}
