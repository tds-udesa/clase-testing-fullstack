# Tests unitarios — guía rápida

Esta carpeta contiene los tests unitarios de componentes (Jest + React Testing Library).
Sirve como material de referencia para la clase: cada archivo muestra un patrón distinto.

## Convenciones

- **Ubicación**: todos los tests viven en `__tests__/`, en un solo nivel (sin subcarpetas
  que repliquen la estructura de `app/` o `components/` cuando hay pocos tests).
- **Nombre de archivo**: `<nombre-del-componente>.test.tsx`, calcado del archivo que testea
  (ej. `random-dog-view.client.tsx` → `random-dog-view.client.test.tsx`).
- **Estructura de cada test**: `describe("NombreDelComponente", () => { it("hace algo cuando...", () => { ... }) })`.
  El texto de cada `it` describe el comportamiento esperado, no la implementación.
- **Patrón Arrange-Act-Assert** dentro de cada `it`:
  1. Preparar mocks/datos.
  2. Renderizar o disparar la interacción.
  3. Afirmar (`expect`) el resultado visible en el DOM.
- **Qué mockear**: cualquier dependencia externa al componente que se está probando
  (llamadas a la API, hooks de Next.js como `usePathname`). El componente en sí nunca se mockea.
- Evitar `container.querySelector` o clases CSS como forma principal de encontrar elementos;
  preferir queries por rol/texto accesible (`getByRole`, `getByText`, `findByRole`), que es lo
  que ve un usuario real.

## `import { render, screen, fireEvent, waitFor } from "@testing-library/react"`

Estas son las cuatro herramientas más usadas de React Testing Library:

- **`render(<Componente />)`**: monta el componente en un DOM virtual (jsdom), como si el
  navegador lo hubiera renderizado. A partir de acá el componente "existe" para el test.
- **`screen`**: objeto con métodos para buscar elementos en ese DOM ya renderizado
  (`screen.getByRole(...)`, `screen.getByText(...)`, `screen.findByRole(...)`). Se usa `screen`
  en vez de guardar el resultado de `render` porque es más simple y es el estilo recomendado
  por la librería.
  - `getBy...` : busca ahora mismo: si no existe todavía, tira error. Sirve para lo que ya
    está en pantalla.
  - `findBy...` : es async (devuelve una `Promise`) y reintenta hasta que el elemento aparece
    o hasta un timeout. Sirve para cosas que aparecen después de un `await` o un fetch
    (por eso se usa `await screen.findByRole(...)` para esperar la imagen).
  - `queryBy...` : busca ahora mismo pero devuelve `null` si no existe, en vez de tirar error.
    Sirve para afirmar que algo **no** está en pantalla.
- **`fireEvent`**: simula eventos del usuario sobre un elemento, por ejemplo
  `fireEvent.click(boton)` simula un click. Es más "de bajo nivel" que otras librerías
  (como `user-event`), pero alcanza para casos simples como un click de botón.
- **`waitFor(callback)`**: espera (reintentando el callback) hasta que el `expect` de adentro
  deje de fallar o hasta un timeout. Se usa cuando algo async va a pasar pero no hay un
  elemento nuevo en pantalla que buscar con `findBy...` (por ejemplo, esperar a que se haya
  llamado una función mock: `await waitFor(() => expect(mockFn).toHaveBeenCalled())`).

## Mockear un módulo: `jest.mock(...)`

```ts
jest.mock("@/app/lib/dogs-api", () => ({
  getRandomDog: jest.fn(),
  saveDog: jest.fn(),
}));

const mockedGetRandomDog = getRandomDog as jest.Mock;
const mockedSaveDog = saveDog as jest.Mock;
```

¿Qué está pasando acá?

1. **`jest.mock("@/app/lib/dogs-api", () => ({...}))`** le dice a Jest: "cada vez que
   cualquier archivo importe algo de `@/app/lib/dogs-api`, no uses el archivo real —
   usá este objeto falso en su lugar". El segundo argumento es una función que devuelve
   el módulo falso (un objeto con las mismas funciones que exporta el módulo real).
   - Esto evita que el test haga una llamada de red real. El componente `RandomDogView`
     importa `getRandomDog` y `saveDog` de ese módulo sin saber que, durante el test,
     en realidad está recibiendo la versión falsa.
   - `jest.mock` se "hoistea" (Jest lo mueve) al principio del archivo automáticamente,
     por eso se puede escribir antes o después del `import` real sin problema.
2. **`jest.fn()`** crea una **función mock**: una función falsa que no hace nada por sí
   sola, pero que registra cómo fue llamada (con qué argumentos, cuántas veces) y a la
   que se le puede decir qué devolver, por ejemplo:
   - `mockedGetRandomDog.mockResolvedValue({ url: "..." })` → la próxima vez que se llame,
     devuelve una promesa que se resuelve con ese valor (simula un fetch exitoso).
   - `mockedGetRandomDog.mockRejectedValue(new Error("..."))` → simula que el fetch falla.
3. **`getRandomDog as jest.Mock`** es solamente una aclaración para TypeScript: como
   `getRandomDog` ahora es en realidad el `jest.fn()` de arriba (pero TypeScript todavía
   lo tipa como la función original), hacemos un cast a `jest.Mock` para poder usar
   métodos como `.mockResolvedValue(...)` sin que TypeScript se queje.
