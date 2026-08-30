import { render, screen } from "@testing-library/react";
import { NavTabs } from "@/app/components/nav-tabs.client";


jest.mock("next/navigation", () => ({
  usePathname: jest.fn(),
}));

import { usePathname } from "next/navigation";

const mockedUsePathname = usePathname as jest.Mock;

describe("NavTabs", () => {
  it("renders a link for each tab", () => {
    mockedUsePathname.mockReturnValue("/");

    render(<NavTabs />);

    expect(screen.getByRole("link", { name: "Perro Aleatorio" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Perros Guardados" })).toBeInTheDocument();
  });

  it("marks the tab matching the current path as active", () => {
    mockedUsePathname.mockReturnValue("/saved");

    render(<NavTabs />);

    const activeTab = screen.getByRole("link", { name: "Perros Guardados" });
    const inactiveTab = screen.getByRole("link", { name: "Perro Aleatorio" });

    expect(activeTab).toHaveClass("text-primary");
    expect(inactiveTab).not.toHaveClass("text-primary");
  });
});
