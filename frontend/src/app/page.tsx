export default function Home() {
  return (
    <div className="flex flex-1 flex-col items-center justify-center gap-4 bg-zinc-50 px-6 py-24 text-center dark:bg-black">
      <h1 className="text-4xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-50">
        ChipsTalk
      </h1>
      <p className="max-w-md text-lg text-zinc-600 dark:text-zinc-400">
        Suivi des prix de composants informatiques en temps réel, avec chat
        intégré.
      </p>
    </div>
  );
}
