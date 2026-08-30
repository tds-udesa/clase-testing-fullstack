"use client";

import { useEffect, useState } from "react";
import { Alert, AlertTitle } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";
import { getRandomDog, saveDog } from "@/app/lib/dogs-api";

export function RandomDogView() {
  const [dogUrl, setDogUrl] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [isSaving, setIsSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState<string | null>(null);

  async function loadRandomDog() {
    setError(null);
    setSaveMessage(null);

    try {
      const dog = await getRandomDog();
      setDogUrl(dog.url);
    } catch {
      setError("Ocurrió un error al buscar un perro. Intentá de nuevo.");
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    const fetchData = async () => {
     await loadRandomDog();
    };
    fetchData();
  }, []);

  function handleGetAnotherDog() {
    setIsLoading(true);
    loadRandomDog();
  }

  async function handleSave() {
    if (!dogUrl) return;

    setIsSaving(true);
    setSaveMessage(null);

    try {
      await saveDog(dogUrl);
      setSaveMessage("¡Perro guardado! Revisá la pestaña 'Perros Guardados'.");
    } catch {
      setSaveMessage("No se pudo guardar el perro. Intentá de nuevo.");
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <div className="mx-auto flex max-w-md flex-col items-center gap-4 py-8">
      <p className="text-2xl font-bold">Perro Aleatorio</p>

      {isLoading && <Spinner className="size-8" />}

      {error && (
        <Alert variant="destructive">
          <AlertTitle>{error}</AlertTitle>
        </Alert>
      )}

      {!isLoading && !error && dogUrl && (
        <div>
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={dogUrl}
            alt="Un perro aleatorio"
            className="max-h-[400px] rounded-lg"
          />
        </div>
      )}

      {saveMessage && (
        <Alert>
          <AlertTitle>{saveMessage}</AlertTitle>
        </Alert>
      )}

      <div className="flex flex-row gap-4">
        <Button onClick={handleGetAnotherDog} disabled={isLoading} variant="outline">
          {isLoading && <Spinner />}
          Otro perro
        </Button>
        <Button onClick={handleSave} disabled={!dogUrl || isLoading || isSaving}>
          {isSaving && <Spinner />}
          Guardar este perro
        </Button>
      </div>
    </div>
  );
}
