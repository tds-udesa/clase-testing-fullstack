"use client";

import { useEffect, useState } from "react";
import { Alert, AlertTitle } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { Spinner } from "@/components/ui/spinner";
import { getSavedDogs, type SavedDog } from "@/app/lib/dogs-api";


export function SavedDogsList() {
  const [dogs, setDogs] = useState<SavedDog[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadSavedDogs() {
      try {
        const savedDogs = await getSavedDogs();
        setDogs(savedDogs);
      } catch {
        setError("Ocurrió un error al cargar tus perros guardados.");
      } finally {
        setIsLoading(false);
      }
    }

    loadSavedDogs();
  }, []);

  if (isLoading) {
    return (
      <div className="flex flex-col items-center py-8">
        <Spinner className="size-8" />
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="destructive" className="mx-auto mt-8 max-w-md">
        <AlertTitle>{error}</AlertTitle>
      </Alert>
    );
  }

  if (dogs.length === 0) {
    return (
      <p className="py-8 text-center text-muted-foreground">
        Todavía no guardaste ningún perro. ¡Guardá uno desde la pestaña Perro
        Aleatorio!
      </p>
    );
  }

  return (
    <div className="grid grid-cols-4 gap-3 p-4 sm:grid-cols-4 md:grid-cols-4">
      {dogs.map((dog) => (
        <Card key={dog.id} className="overflow-hidden py-0">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={dog.url}
            alt={dog.category}
            className="h-[300px] w-full object-fit"
          />
          <CardContent className="py-4">
            <Badge>{dog.category}</Badge>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
