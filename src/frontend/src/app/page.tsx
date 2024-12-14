import SideBar from "@/components/sidebar";

export default function Home() {
  return ( 
    <main className="bg-gradient-to-b from-[#e0d8ff] from-10% to-black to-90% flex min-h-screen flex-col items-center">
      <SideBar />
      <div className="w-full flex flex-col items-center justify-center">
        <h1 className="text-[#46404F] text-center w-full text-6xl font-extrabold mb-6">
          Home
        </h1>
      </div>
    </main>
  );
}
