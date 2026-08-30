import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { RandomDogView } from "@/app/components/random-dog-view.client";
import { getRandomDog, saveDog } from "@/app/lib/dogs-api";


jest.mock("@/app/lib/dogs-api", () => ({
  getRandomDog: jest.fn(),
  saveDog: jest.fn(),
}));

const mockedGetRandomDog = getRandomDog as jest.Mock;
const mockedSaveDog = saveDog as jest.Mock;

describe("RandomDogView", () => {
  it("shows the dog image once it loads", async () => {
    mockedGetRandomDog.mockResolvedValue({ url: "http://localhost:8000/api/v1/dogs/random/dog.jpg" });

    render(<RandomDogView />);

    expect(screen.getAllByRole("status", { name: "Loading" }).length).toBeGreaterThan(0);

    const image = await screen.findByRole("img", { name: "Un perro aleatorio" });
    expect(image).toHaveAttribute("src", "http://localhost:8000/api/v1/dogs/random/dog.jpg");
  });

  it("shows an error message when the fetch fails", async () => {
    mockedGetRandomDog.mockRejectedValue(new Error("network error"));

    render(<RandomDogView />);

    expect(
      await screen.findByText("Ocurrió un error al buscar un perro. Intentá de nuevo."),
    ).toBeInTheDocument();
  });

  it("saves the dog when clicking the save button", async () => {
    mockedGetRandomDog.mockResolvedValue({ url: "http://localhost:8000/api/v1/dogs/random/dog.jpg" });
    mockedSaveDog.mockResolvedValue({
      id: 1,
      category: "labrador",
      url: "http://localhost:8000/api/v1/dogs/random/dog.jpg",
    });

    render(<RandomDogView />);
    await screen.findByRole("img", { name: "Un perro aleatorio" });

    fireEvent.click(screen.getByRole("button", { name: "Guardar este perro" }));

    await waitFor(() => {
      expect(mockedSaveDog).toHaveBeenCalledWith("http://localhost:8000/api/v1/dogs/random/dog.jpg");
    });
    expect(
      await screen.findByText("¡Perro guardado! Revisá la pestaña 'Perros Guardados'."),
    ).toBeInTheDocument();
  });
});
