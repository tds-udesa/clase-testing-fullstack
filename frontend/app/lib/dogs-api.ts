const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

export interface SavedDog {
  id: number;
  category: string;
  url: string;
}

export async function getRandomDog(): Promise<{ url: string }> {
  const response = await fetch(`${API_BASE_URL}/dogs/random`);

  if (!response.ok) {
    throw new Error("Could not fetch a random dog image");
  }

  return response.json();
}

export async function getSavedDogs(): Promise<SavedDog[]> {
  const response = await fetch(`${API_BASE_URL}/dogs/my-dogs`);

  if (!response.ok) {
    throw new Error("Could not fetch the saved dogs");
  }

  return response.json();
}

export async function saveDog(url: string): Promise<SavedDog> {
  const response = await fetch(`${API_BASE_URL}/dogs/save`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });

  if (!response.ok) {
    throw new Error("Could not save this dog");
  }

  return response.json();
}
